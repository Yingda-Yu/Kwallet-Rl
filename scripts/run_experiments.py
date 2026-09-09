"""Resumable, parallel experiment driver for the K-Wallet matrix.

Builds the run plan (learned methods x C x seeds = training runs; FA/FWF =
eval-only), executes each as an isolated `kwallet.cli` subprocess with bounded
threads, and records a manifest. Skips runs whose artifacts already exist
(unless --force). Nothing is marked DONE unless the eval CSV is actually
produced.

Examples:
  python scripts/run_experiments.py --dry-run
  python scripts/run_experiments.py --tier pilot --workers 6 --threads 4
  python scripts/run_experiments.py --tier full  --workers 12 --threads 4
"""
import argparse
import csv
import json
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEEDS_MAIN = [123, 323, 532, 777, 999, 2027, 3407, 4501, 6101, 8888]
SEEDS_KSCALE = [123, 323, 532]
CS_MAIN = [800, 900, 1000, 1200]
LEARNED = ["ja_ppo", "ifac", "sc_fac"]
RULES = ["FA", "FWF"]


def specs_for(tier: str):
    """Return list of run dicts."""
    runs = []
    if tier == "smoke":
        Cs, seeds, eps = [1200], [123], 64
    elif tier == "pilot":
        Cs, seeds, eps = CS_MAIN, [123, 323], 800
    elif tier == "full":
        Cs, seeds, eps = CS_MAIN, SEEDS_MAIN, 3000
    else:
        raise ValueError(tier)
    for C in Cs:
        for m in LEARNED:
            for s in seeds:
                runs.append(dict(kind="learned", method=m, C=C, k=24, F=3,
                                 T=1000, seed=s, episodes=eps,
                                 hidden=256 if tier != "smoke" else 64,
                                 embed=32))
        for r in RULES:
            runs.append(dict(kind="rule", method=r, C=C, k=24, F=3, T=1000))
    return runs


def run_paths(exp, r):
    outdir = ROOT / "runs" / exp
    if r["kind"] == "learned":
        rd = outdir / f"{r['method']}_C{float(r['C'])}_k{r['k']}_F{r['F']}_s{r['seed']}"
        return rd, rd / "checkpoint.pt", outdir / (
            f"eval_{r['method']}_C{float(r['C'])}_k{r['k']}_F{r['F']}_s{r['seed']}.csv")
    else:
        return outdir, None, outdir / (
            f"eval_{r['method']}_C{float(r['C'])}_k{r['k']}_F{r['F']}.csv")


def build_commands(exp, r, threads):
    env = dict(os.environ)
    env["OMP_NUM_THREADS"] = str(threads)
    env["MKL_NUM_THREADS"] = str(threads)
    py = sys.executable
    common = ["--C", str(float(r["C"])), "--k", str(r["k"]), "--F", str(r["F"]),
              "--T", str(r["T"]), "--exp", exp, "--base-seed", "532",
              "--pool-eval", "200"]
    cmds = []
    if r["kind"] == "learned":
        rd, ckpt, evalcsv = run_paths(exp, r)
        train = [py, "-m", "kwallet.cli", "train", "--method", r["method"],
                 "--seed", str(r["seed"]), "--episodes", str(r["episodes"]),
                 "--rollout", "8", "--epochs", "10", "--mb", "512",
                 "--hidden", str(r["hidden"]), "--embed", str(r["embed"]),
                 "--device", "cpu", "--pool-train", "5000"] + common
        evalc = [py, "-m", "kwallet.cli", "evaluate", "--method", r["method"],
                 "--seed", str(r["seed"]), "--checkpoint", str(ckpt),
                 "--hidden", str(r["hidden"]), "--embed", str(r["embed"]),
                 "--device", "cpu"] + common
        cmds = [train, evalc]
    else:
        evalc = [py, "-m", "kwallet.cli", "evaluate", "--method", r["method"],
                 "--device", "cpu"] + common
        cmds = [evalc]
    return cmds, env


def run_one(exp, r, threads, force, logdir):
    rd, ckpt, evalcsv = run_paths(exp, r)
    if evalcsv.exists() and not force:
        return ("SKIPPED", str(evalcsv), "exists")
    cmds, env = build_commands(exp, r, threads)
    t0 = time.time()
    logpath = logdir / (evalcsv.stem + ".log")
    with open(logpath, "w") as lf:
        for cmd in cmds:
            lf.write("+ " + " ".join(cmd) + "\n")
            lf.flush()
            p = subprocess.run(cmd, cwd=str(ROOT), env=env, stdout=lf,
                               stderr=subprocess.STDOUT)
            if p.returncode != 0:
                return ("FAILED", str(logpath), f"rc={p.returncode}")
    status = "DONE" if evalcsv.exists() else "FAILED"
    return (status, str(evalcsv), f"{time.time()-t0:.0f}s")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tier", choices=["smoke", "pilot", "full"], default="smoke")
    ap.add_argument("--exp", default=None)
    ap.add_argument("--workers", type=int, default=1)
    ap.add_argument("--threads", type=int, default=8)
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--methods", default=None, help="comma filter on method")
    args = ap.parse_args()
    exp = args.exp or f"matrix_{args.tier}"
    runs = specs_for(args.tier)
    if args.methods:
        keep = set(args.methods.split(","))
        runs = [r for r in runs if r["method"] in keep]
    logdir = ROOT / "runs" / exp / "logs"
    logdir.mkdir(parents=True, exist_ok=True)
    manifest = ROOT / "experiments" / f"manifest_{exp}.csv"
    manifest.parent.mkdir(exist_ok=True)

    print(f"plan: {len(runs)} runs, tier={args.tier}, exp={exp}, "
          f"workers={args.workers}, threads/run={args.threads}")
    for r in runs:
        print(" ", r["kind"], r["method"], "C", r["C"],
              ("seed " + str(r["seed"]) if r["kind"] == "learned" else ""))
    if args.dry_run:
        return 0

    rows = []
    t0 = time.time()
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(run_one, exp, r, args.threads, args.force, logdir): r
                for r in runs}
        for fut in as_completed(futs):
            r = futs[fut]
            try:
                status, artifact, note = fut.result()
            except Exception as e:  # noqa: BLE001
                status, artifact, note = "FAILED", "", repr(e)
            row = dict(method=r["method"], C=r["C"], k=r["k"], F=r["F"],
                       seed=r.get("seed", ""), kind=r["kind"],
                       episodes=r.get("episodes", ""), status=status,
                       artifact=artifact, note=note,
                       elapsed_wall=round(time.time() - t0, 1))
            rows.append(row)
            print(f"[{status}] {r['method']} C{r['C']} "
                  f"{r.get('seed','')} -> {note}", flush=True)

    with open(manifest, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    ndone = sum(r["status"] == "DONE" for r in rows)
    nfail = sum(r["status"] == "FAILED" for r in rows)
    nskip = sum(r["status"] == "SKIPPED" for r in rows)
    print(f"\nmanifest -> {manifest}\nDONE={ndone} FAILED={nfail} SKIP={nskip}")
    return 1 if nfail else 0


if __name__ == "__main__":
    sys.exit(main())
