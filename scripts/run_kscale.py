"""k-scaling + cross-k transfer experiment (Phase-2 novelty).

Trains the permutation-equivariant set policy and the flat MLP policy at
k in {6, 12, 24} (capacity fixed C=1200, so wallet_size = C/k), then evaluates
each checkpoint:
  * matched:  train k == test k (both set and flat policies);
  * zero-shot transfer (SET policy only): train k_train -> test k_test, k_train
    != k_test, by loading the k-independent set weights into a network built at
    k_test. Flat policies have k-dependent parameter shapes and CANNOT be
    transferred; that is recorded in the aggregation as NOT_TRANSFERRABLE.

Each eval runs in its own exp sub-directory (collision-free). Aggregate the
resulting *_summary.csv files with scripts/aggregate_kscale.py.
"""
import argparse, csv, os, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KS = [6, 12, 24]
SEEDS = [123, 323, 532]
EPISODES = 2000
HIDDEN = 128


def run_dir(exp, m, k, s):
    return ROOT / "runs" / exp / f"{m}_C1200.0_k{k}_F3_s{s}"


def train_one(exp, m, k, s, threads):
    rd = run_dir(exp, m, k, s)
    ckpt = rd / "checkpoint.pt"
    if ckpt.exists():
        return ("SKIP", f"{m} k{k} s{s}", "ckpt exists")
    rd.mkdir(parents=True, exist_ok=True)
    bias = 2.0 if m.startswith("set_") else 0.0
    cmd = [sys.executable, "-m", "kwallet.cli", "train", "--method", m,
           "--C", "1200", "--k", str(k), "--F", "3", "--T", "1000",
           "--seed", str(s), "--episodes", str(EPISODES), "--rollout", "8",
           "--hidden", str(HIDDEN), "--embed", "32", "--noop-bias", str(bias),
           "--pool-train", "5000", "--pool-eval", "200", "--base-seed", "532",
           "--exp", exp]
    env = dict(os.environ, OMP_NUM_THREADS=str(threads),
               MKL_NUM_THREADS=str(threads))
    with open(rd / "train.log", "w") as lf:
        p = subprocess.run(cmd, cwd=str(ROOT), env=env, stdout=lf,
                           stderr=subprocess.STDOUT)
    return ("DONE" if p.returncode == 0 else "FAIL", f"{m} k{k} s{s}",
            f"rc={p.returncode}")


def eval_one(exp, m, k_train, k_test, s, threads):
    """Evaluate checkpoint trained at k_train on env at k_test."""
    sub = f"{exp}__{m}_kt{k_train}_s{s}__ke{k_test}"
    ckpt = run_dir(exp, m, k_train, s) / "checkpoint.pt"
    # marker written by this script after a successful eval
    marker = ROOT / "runs" / exp / "_evals" / f"{sub}.ok"
    if marker.exists():
        return ("SKIP", f"{m} k{k_train}->k{k_test} s{s}", "done")
    if not ckpt.exists():
        return ("WAIT", f"{m} k{k_train}->k{k_test} s{s}", "no ckpt")
    cmd = [sys.executable, "-m", "kwallet.cli", "evaluate", "--method", m,
           "--C", "1200", "--k", str(k_test), "--F", "3", "--T", "1000",
           "--seed", str(s), "--hidden", str(HIDDEN), "--embed", "32",
           "--workers", "1", "--eval-threads", str(threads),
           "--checkpoint", str(ckpt), "--pool-eval", "200",
           "--base-seed", "532", "--exp", sub]
    env = dict(os.environ, OMP_NUM_THREADS=str(threads),
               MKL_NUM_THREADS=str(threads))
    p = subprocess.run(cmd, cwd=str(ROOT), env=env,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if p.returncode == 0:
        marker.parent.mkdir(parents=True, exist_ok=True)
        marker.write_text(f"{m} kt{k_train} ke{k_test} s{s}\n")
        return ("DONE", f"{m} k{k_train}->k{k_test} s{s}", "ok")
    return ("FAIL", f"{m} k{k_train}->k{k_test} s{s}", f"rc={p.returncode}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--exp", default="kscale")
    ap.add_argument("--methods", default="set_sc_fac,sc_fac")
    ap.add_argument("--workers", type=int, default=2)
    ap.add_argument("--threads", type=int, default=9)
    args = ap.parse_args()
    methods = args.methods.split(",")
    t0 = time.time()
    trains = [(m, k, s) for m in methods for k in KS for s in SEEDS]
    print(f"training {len(trains)} runs, workers={args.workers}", flush=True)
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(train_one, args.exp, m, k, s, args.threads):
                (m, k, s) for (m, k, s) in trains}
        for f in as_completed(futs):
            st, name, note = f.result(); print(f"[train {st}] {name} {note}", flush=True)
    # eval plan: set policies -> all kt x ke; flat -> matched only
    evals = []
    for m in methods:
        for kt in KS:
            for s in SEEDS:
                for ke in KS:
                    if not m.startswith("set_") and ke != kt:
                        continue  # flat weights cannot transfer across k
                    evals.append((m, kt, ke, s))
    print(f"evaluating {len(evals)} (matched+transfer), workers={args.workers*2}", flush=True)
    rows = []
    with ThreadPoolExecutor(max_workers=args.workers * 2) as ex:
        futs = {ex.submit(eval_one, args.exp, m, kt, ke, s, args.threads):
                (m, kt, ke, s) for (m, kt, ke, s) in evals}
        for f in as_completed(futs):
            st, name, note = f.result(); m, kt, ke, s = futs[f]
            rows.append(dict(method=m, train_k=kt, test_k=ke, seed=s,
                             status=st, note=note))
            if st not in ("SKIP", "WAIT"):
                print(f"[eval {st}] {name} {note}", flush=True)
    man = ROOT / "experiments" / f"manifest_{args.exp}.csv"
    man.parent.mkdir(exist_ok=True)
    with open(man, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    print(f"manifest -> {man} ({time.time()-t0:.0f}s)", flush=True)


if __name__ == "__main__":
    sys.exit(main())
