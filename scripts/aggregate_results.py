"""Aggregate per-run eval CSVs into the paper tables (main, regime, tau).

Reads runs/<exp>/eval_*.csv and emits results/tables/<exp>_*.csv plus
results/<exp>_claims.json with numbers, per-seed SEs and evidence labels.
Deterministic evaluation on the fixed test pools.
"""
import argparse
import glob
import json
import os
import re
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
REGIMES = ["US","TLS","LNS","TLNS","TPLS","PLS","UB","TLB","LNB","TLNB","TPLB","PLB"]
# Paper Table II REPORTED_ONLY Money values (do NOT overwrite with runs)
REPORTED = {
    "FA":   {800:2772.78, 900:4047.32, 1000:5402.43, 1200:8591.65},
    "FWF":  {800:2288.24, 900:3512.46, 1000:4802.56, 1200:7810.86},
    "ja_ppo":{800:3368.57,900:5636.16,1000:8332.27,1200:14443.01},
    "ifac": {800:3607.05, 900:6347.35, 1000:8786.44, 1200:14472.93},
    "sc_fac":{800:3999.25,900:6627.98,1000:9064.80,1200:14687.65},
}
METHOD_ORDER = ["FA","FWF","ja_ppo","ifac","sc_fac"]
FNAME = re.compile(r"eval_(?P<method>[a-zA-Z_]+)_C(?P<C>[0-9.]+)_k(?P<k>[0-9]+)_F(?P<F>[0-9]+)(?:_s(?P<seed>[0-9]+))?\.csv$")


def load_runs(exp):
    rows = []
    for f in glob.glob(str(ROOT / "runs" / exp / "eval_*.csv")):
        m = FNAME.search(os.path.basename(f))
        if not m or "_summary" in f or "_tau" in f:
            continue
        d = m.groupdict()
        df = pd.read_csv(f)
        rows.append(dict(method=d["method"], C=float(d["C"]),
                         seed=int(d["seed"]) if d["seed"] else None,
                         df=df))
    return rows


def main_table(exp, out):
    runs = load_runs(exp)
    records = []
    for r in runs:
        df = r["df"]
        per_ep = df["money"].mean()
        records.append(dict(method=r["method"], C=r["C"],
                            seed=r["seed"] if r["seed"] is not None else "rule",
                            money=per_ep,
                            accept=df["accepted_value"].mean(),
                            flush=df["charged_flushes"].mean(),
                            drop=df["drop_count"].mean()))
    long = pd.DataFrame(records)
    # aggregate across seeds
    agg = (long.groupby(["method","C"])
           .agg(money_mean=("money","mean"),
                money_se=("money", lambda v: v.std(ddof=1)/np.sqrt(len(v)) if len(v)>1 else 0.0),
                n_seeds=("money","count"),
                accept_mean=("accept","mean"),
                flush_mean=("flush","mean"))
           .reset_index())
    agg["reported"] = [REPORTED.get(m,{}).get(int(round(c)), np.nan)
                       for m,c in zip(agg.method, agg.C)]
    agg["m_order"] = agg.method.map({m:i for i,m in enumerate(METHOD_ORDER)}).fillna(99)
    agg = agg.sort_values(["C","m_order"]).drop(columns="m_order")
    out.mkdir(parents=True, exist_ok=True)
    long.to_csv(out / f"{exp}_main_long.csv", index=False)
    agg.to_csv(out / f"{exp}_main_table.csv", index=False)
    print(agg.to_string(index=False))

    # per-regime: for SC vs JA, mean per regime at each C
    reg_rows = []
    for r in runs:
        if r["method"] not in ("sc_fac","ja_ppo","ifac"):
            continue
        for regime, g in r["df"].groupby("regime"):
            reg_rows.append(dict(method=r["method"], C=r["C"],
                                 seed=r["seed"], regime=regime, money=g["money"].mean()))
    reg = pd.DataFrame(reg_rows)
    if len(reg):
        regagg = reg.groupby(["method","C","regime"]).money.mean().reset_index()
        regagg.to_csv(out / f"{exp}_regime_money.csv", index=False)

    # tau post-hoc: aggregate the per-run tau files
    tau_rows = []
    for f in glob.glob(str(ROOT / "runs" / exp / "eval_*_tau_posthoc.csv")):
        m = FNAME.search(os.path.basename(f).replace("_tau_posthoc",""))
        d = m.groupdict() if m else {}
        t = pd.read_csv(f)
        t["method"]=d.get("method"); t["C"]=float(d["C"]) if d.get("C") else None
        t["seed"]=d.get("seed")
        tau_rows.append(t)
    if tau_rows:
        tau = pd.concat(tau_rows).groupby(["method","C","tau"]).money_mean.mean().reset_index()
        tau.to_csv(out / f"{exp}_tau_posthoc.csv", index=False)

    claims = {"exp": exp,
              "evidence_note": ("REPORTED = paper Table II (not regenerated); "
                                "money_mean = REIMPLEMENTED deterministic eval on "
                                "ported 12-regime test pools"),
              "reported_table_II": REPORTED}
    with open(out.parent / f"{exp}_claims.json","w") as f:
        json.dump(claims, f, indent=2)
    print("\nwrote tables to", out)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--exp", default="matrix_smoke")
    a = ap.parse_args()
    main_table(a.exp, ROOT / "results" / "tables")
