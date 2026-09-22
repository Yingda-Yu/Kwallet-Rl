"""Aggregate k-scaling / cross-k transfer results into transfer matrices.

Reads the per-eval exp sub-directories produced by scripts/run_kscale.py
(named ``<exp>__<method>_kt<train_k>_s<seed>__ke<test_k>``) and builds, for each
method, a train-k x test-k table of Money (mean over seeds). The diagonal is the
matched (train==test) performance; off-diagonal entries for the set policy are
zero-shot transfers; flat policies have no off-diagonal (k-dependent weights).
"""
import argparse, glob, re
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--exp", default="kscale")
    args = ap.parse_args()
    rows = []
    pat = re.compile(rf"{re.escape(args.exp)}__(.+)_kt(\d+)_s(\d+)__ke(\d+)$")
    for sub in sorted(glob.glob(str(ROOT / "runs" / f"{args.exp}__*"))):
        m = pat.search(Path(sub).name)
        if not m:
            continue
        method, kt, s, ke = m.group(1), int(m.group(2)), int(m.group(3)), int(m.group(4))
        sums = glob.glob(str(Path(sub) / "eval_*_summary.csv"))
        if not sums:
            continue
        d = pd.read_csv(sums[0]); r = d[d.group == "ALL"]
        if len(r) == 0:
            continue
        r = r.iloc[0]
        rows.append(dict(method=method, train_k=kt, test_k=ke, seed=s,
                         money=r.money_mean, accept=r.accepted_value_mean,
                         flush=r.charged_flushes_mean, drops=r.drop_count_mean))
    df = pd.DataFrame(rows)
    if df.empty:
        print("no results yet")
        return
    out = ROOT / "results" / "tables"; out.mkdir(parents=True, exist_ok=True)
    df.to_csv(out / f"{args.exp}_transfer_long.csv", index=False)
    print("=== transfer matrix: Money (mean over seeds) ===")
    for method in df.method.unique():
        sub = df[df.method == method]
        piv = sub.pivot_table(index="train_k", columns="test_k",
                              values="money", aggfunc="mean")
        print(f"\n{method}  (rows=train k, cols=deploy k):")
        print(piv.round(0).to_string())
        if (piv.index.values == piv.columns.values).all():
            diag = np.mean([piv.loc[k, k] for k in piv.index if k in piv.columns])
            off = [piv.loc[kt, ke] for kt in piv.index for ke in piv.columns
                   if kt != ke and not pd.isna(piv.loc[kt, ke])]
            if off:
                print(f"  matched(diag) mean={diag:.0f}  transfer(off-diag) mean={np.mean(off):.0f}"
                      f"  retention={100*np.mean(off)/diag:.1f}%")


if __name__ == "__main__":
    main()
