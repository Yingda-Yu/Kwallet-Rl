"""Paired statistical comparisons (seed-level) for the main matrix.

The independent experimental unit is a training SEED. At each capacity C we
pair methods by seed (method A seed s vs method B seed s, both evaluated on the
identical fixed test episodes) and report the mean within-seed Money
difference, a paired-t 95% CI and p-value over seeds, and the sign count.
Rules are deterministic, so their value is compared against every learned
seed. Writes results/tables/<exp>_paired.csv and a LaTeX table.
"""
import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
LABEL = {"FA": "FA", "FWF": "FWF", "BFP0.5": "BFP0.5", "ja_ppo": "JA-PPO",
         "ifac": "IFAC", "sc_fac": "SC-FAC", "sc_nocond": "SC(nocond)",
         "sc_shuffled": "SC(shuf.)"}
# (a, b) -> reports mean(a - b); positive means a beats b
PAIRS = [("sc_fac", "ifac"), ("ifac", "ja_ppo"), ("sc_fac", "ja_ppo"),
         ("BFP0.5", "sc_fac"), ("BFP0.5", "ifac"), ("BFP0.5", "ja_ppo"),
         ("sc_fac", "FA"), ("ifac", "FA"),
         ("sc_fac", "sc_nocond"), ("sc_fac", "sc_shuffled")]


def seed_money_table(long: pd.DataFrame):
    """Return (pivoted DataFrame methods x [seed cols] per C dict, rule values)."""
    out = {}
    learned = long[long.seed != "rule"]
    rules = long[long.seed == "rule"]
    for C, g in learned.groupby("C"):
        piv = g.pivot_table(index="method", columns="seed", values="money")
        rule = rules[rules.C == C].set_index("method")["money"].to_dict()
        out[C] = (piv, rule)
    return out


def paired_ci(a_vals, b_vals):
    a = np.asarray(a_vals, float); b = np.asarray(b_vals, float)
    n = min(len(a), len(b))
    a, b = a[:n], b[:n]
    d = a - b
    mean = d.mean()
    if n > 1:
        se = d.std(ddof=1) / np.sqrt(n)
        tcrit = stats.t.ppf(0.975, n - 1)
        lo, hi = mean - tcrit * se, mean + tcrit * se
        t, p = stats.ttest_rel(a, b)
        wins = int((d > 0).sum())
    else:
        se = lo = hi = t = p = float("nan"); wins = int(d[0] > 0)
    return dict(n=n, mean_diff=mean, lo=lo, hi=hi, p=float(p),
                wins=wins, a_mean=float(a.mean()), b_mean=float(b.mean()))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--exp", default="matrix_main")
    ap.add_argument("--long", default=None,
                    help="long CSV; default results/tables/<exp>_main_long.csv")
    ap.add_argument("--ref-long", default=None,
                    help="optional extra long CSV (e.g. matrix_main) whose "
                         "sc_fac rows are merged for ablation contrasts")
    ap.add_argument("--tex", default="paired.tex",
                    help="output LaTeX filename under assets/tables")
    args = ap.parse_args()
    longf = Path(args.long) if args.long else (
        ROOT / "results" / "tables" / f"{args.exp}_main_long.csv")
    if not longf.exists():
        print("missing", longf); return
    long = pd.read_csv(longf)
    if args.ref_long:
        ref = pd.read_csv(args.ref_long)
        keep = ref[ref.method == "sc_fac"]
        long = pd.concat([long, keep], ignore_index=True)
    long["seed"] = long["seed"].astype(str)
    tables = seed_money_table(long)
    rows = []
    for C in sorted(tables):
        piv, rule = tables[C]
        for (ma, mb) in PAIRS:
            if ma not in piv.index and ma not in rule:
                continue
            if mb not in piv.index and mb not in rule:
                continue
            a = rule[ma] if ma in rule else piv.loc[ma].dropna().to_numpy()
            b = rule[mb] if mb in rule else piv.loc[mb].dropna().to_numpy()
            # broadcast rule scalar to per-seed vector
            if np.isscalar(a):
                a = np.full_like(np.asarray(b, float), float(a))
            if np.isscalar(b):
                b = np.full_like(np.asarray(a, float), float(b))
            r = paired_ci(a, b)
            rows.append(dict(C=int(C), a=LABEL.get(ma, ma), b=LABEL.get(mb, mb),
                            contrast=f"{LABEL.get(ma,ma)}-{LABEL.get(mb,mb)}", **r))
    df = pd.DataFrame(rows)
    out = ROOT / "results" / "tables" / f"{args.exp}_paired.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out, index=False)
    pd.set_option("display.width", 160)
    print(df.round(1).to_string(index=False))
    # LaTeX (C=1200 contrasts of primary interest)
    sub = df[df.C == 1200]
    lines = [r"\begin{tabular}{lrrrr}", r"\hline",
             r"contrast (a$-$b) & $\Delta$Money & 95\% CI & $p$ & wins/$n$\\"]
    for _, r in sub.iterrows():
        ci = f"[{r.lo:.0f},{r.hi:.0f}]" if not np.isnan(r.lo) else "--"
        p = f"{r.p:.3f}" if not np.isnan(r.p) else "--"
        lines.append(f"{r.contrast} & {r.mean_diff:.0f} & {ci} & {p} & "
                     f"{r.wins}/{r.n}\\\\")
    lines += [r"\hline", r"\end{tabular}"]
    tab = ROOT / "paper" / "icassp2027" / "assets" / "tables" / args.tex
    tab.parent.mkdir(parents=True, exist_ok=True)
    tab.write_text("\n".join(lines))
    print("wrote", out, "and", tab)


if __name__ == "__main__":
    main()
