"""Aggregation and paired statistical tests for evaluation records.

Methods are always compared on the SAME episodes (regime, episode index), so
differences are paired. We predeclare: (1) paired Student-t 95% CI on the mean
difference of per-episode Money; (2) non-parametric bootstrap 95% CI (B=10000,
fixed RNG). Both are reported; we use paired-t CIs as the primary table.
"""
from __future__ import annotations

from typing import Dict, List, Sequence, Tuple

import numpy as np
import pandas as pd
from scipy import stats

METRICS = ["money", "accepted_value", "accepted_count", "drop_count",
           "charged_flushes"]
_BOOT_RNG = np.random.default_rng(20270916)


def to_frame(records: List[Dict]) -> pd.DataFrame:
    return pd.DataFrame(records)


def summarize(df: pd.DataFrame, by: str = "regime") -> pd.DataFrame:
    rows = []
    groups = [("ALL", df)] + list(df.groupby(by, sort=False))
    for name, g in groups:
        row = {"group": name, "n": len(g)}
        for m in METRICS:
            vals = g[m].to_numpy(dtype=float)
            row[f"{m}_mean"] = float(vals.mean())
            row[f"{m}_std"] = float(vals.std(ddof=1)) if len(vals) > 1 else 0.0
            row[f"{m}_se"] = float(vals.std(ddof=1) / np.sqrt(len(vals))) if len(vals) > 1 else 0.0
        rows.append(row)
    return pd.DataFrame(rows)


def _aligned_pairs(df_a: pd.DataFrame, df_b: pd.DataFrame, key: str):
    a = df_a.set_index(["regime", "episode"])[key]
    b = df_b.set_index(["regime", "episode"])[key]
    idx = a.index.intersection(b.index)
    return a.loc[idx].to_numpy(float), b.loc[idx].to_numpy(float)


def paired_difference(df_a: pd.DataFrame, df_b: pd.DataFrame, key: str = "money"
                      ) -> Dict:
    """Mean (a - b) over paired episodes with paired-t and bootstrap CIs."""
    va, vb = _aligned_pairs(df_a, df_b, key)
    diff = va - vb
    n = len(diff)
    mean = float(diff.mean())
    sd = float(diff.std(ddof=1)) if n > 1 else 0.0
    se = sd / np.sqrt(n) if n > 1 else 0.0
    tcrit = float(stats.t.ppf(0.975, df=n - 1)) if n > 1 else float("nan")
    ci_t = (mean - tcrit * se, mean + tcrit * se) if n > 1 else (float("nan"),) * 2
    tstat, pval = (float("nan"), float("nan"))
    if n > 1:
        tstat, pval = stats.ttest_rel(va, vb)
        tstat, pval = float(tstat), float(pval)
    # bootstrap
    boots = []
    if n > 1:
        for _ in range(10000):
            samp = _BOOT_RNG.integers(0, n, n)
            boots.append(diff[samp].mean())
        lo, hi = np.percentile(boots, [2.5, 97.5])
        ci_boot = (float(lo), float(hi))
    else:
        ci_boot = (float("nan"), float("nan"))
    return {"n": n, "mean_diff": mean, "se": se, "ci95_t": ci_t,
            "t": tstat, "p": pval, "ci95_boot": ci_boot,
            "a_mean": float(va.mean()), "b_mean": float(vb.mean())}


def seed_summary(run_frames: Sequence[pd.DataFrame]) -> pd.DataFrame:
    """Collapse per-seed frames to per-seed overall means then aggregate.

    For the main table the experimental unit is a training SEED; each seed is
    evaluated on the same fixed eval pools. We compute each seed's mean Money
    over all eval episodes, then report mean/SE across seeds.
    """
    seed_means = []
    for si, df in enumerate(run_frames):
        seed_means.append({"seed": si, "money": df["money"].mean(),
                           "accepted_value": df["accepted_value"].mean(),
                           "charged_flushes": df["charged_flushes"].mean()})
    s = pd.DataFrame(seed_means)
    rows = []
    for m in ["money", "accepted_value", "charged_flushes"]:
        v = s[m].to_numpy(float)
        rows.append({"metric": m, "mean": float(v.mean()),
                     "std": float(v.std(ddof=1)) if len(v) > 1 else 0.0,
                     "se": float(v.std(ddof=1) / np.sqrt(len(v))) if len(v) > 1 else 0.0,
                     "n_seeds": len(v)})
    return pd.DataFrame(rows)
