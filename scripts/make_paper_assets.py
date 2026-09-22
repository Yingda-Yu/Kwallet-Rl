"""Generate paper tables/figures STRICTLY from result CSVs (no hand numbers).

Reads results/tables/*.csv and runs/* (bench, switching) and writes into
paper/icassp2027/assets/{tables,figs}/ plus assets/paper_claims.json.
Any artifact whose source CSV is missing is SKIPPED and recorded under
``missing`` in paper_claims.json, so the manuscript never contains a
fabricated number.

Run after aggregate_results.py / aggregate_kscale.py:
    python scripts/make_paper_assets.py --exp matrix_main --ablation matrix_ablation
"""
import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

import matplotlib
matplotlib.use("pdf")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
TBL = ROOT / "results" / "tables"
ASSETS = ROOT / "paper" / "icassp2027" / "assets"
FIG = ASSETS / "figs"
TAB = ASSETS / "tables"

METHOD_LABEL = {"FA": "FA", "FWF": "FWF", "BFP0.5": "BFP0.5 (rule)",
                "ja_ppo": "JA-PPO", "ifac": "IFAC", "sc_fac": "SC-FAC",
                "sc_nocond": "SC-FAC (no cond.)", "sc_shuffled": "SC-FAC (shuf. cond.)",
                "set_ifac": "Set-IFAC", "set_sc_fac": "Set-SC-FAC"}
LEARNED = ["ja_ppo", "ifac", "sc_fac"]
RULES = ["FA", "FWF", "BFP0.5"]
COLORS = {"FA": "#888888", "FWF": "#aaaaaa", "BFP0.5": "#1b9e77",
          "ja_ppo": "#d95f02", "ifac": "#7570b3", "sc_fac": "#e7298a"}


def _fmt(x, nd=1):
    return "--" if pd.isna(x) else f"{x:.{nd}f}"


def main_table(exp):
    f = TBL / f"{exp}_main_table.csv"
    if not f.exists():
        return None, {"main_table": str(f)}
    df = pd.read_csv(f)
    # capacity curve figure
    fig, ax = plt.subplots(figsize=(3.4, 2.4))
    for m in LEARNED + RULES:
        g = df[df.method == m]
        if len(g) < 2:
            continue
        g = g.sort_values("C")
        style = "--" if m in RULES else "-"
        ax.errorbar(g.C, g.money_mean, yerr=g.money_se, label=METHOD_LABEL[m],
                    color=COLORS.get(m), linestyle=style, marker="o", ms=3,
                    capsize=2, lw=1.4)
    ax.set_xlabel("collateral budget $C$")
    ax.set_ylabel("Money / episode")
    ax.grid(alpha=.3)
    ax.legend(fontsize=6, ncol=2)
    fig.tight_layout(); fig.savefig(FIG / "capacity_curve.pdf"); plt.close(fig)

    # LaTeX table: rows = method, cols = C (mean +/- se)
    Cs = sorted(df.C.unique())
    lines = [r"\begin{tabular}{l" + "c" * len(Cs) + "}",
             r"\hline",
             "method & " + " & ".join(f"$C={int(c)}$" for c in Cs) + r"\\"]
    for m in RULES + LEARNED:
        g = df[df.method == m].set_index("C")
        cells = []
        for c in Cs:
            if c in g.index:
                r = g.loc[c]
                cells.append(f"{r.money_mean:.0f}$\\pm${r.money_se:.0f}"
                             if r.n_seeds and r.n_seeds > 1 else f"{r.money_mean:.0f}")
            else:
                cells.append("--")
        lines.append(f"{METHOD_LABEL[m]} & " + " & ".join(cells) + r"\\")
    lines += [r"\hline", r"\end{tabular}"]
    (TAB / "main_results.tex").write_text("\n".join(lines))
    return df, {}


def ablation_table(abl_exp, main_exp):
    """Mechanism ablations. sc_nocond/sc_shuffled come from the ablation run;
    the sc_fac reference is taken from the main run on the SAME seeds and
    capacities so the comparison is paired (identical training budget/seeds)."""
    f_abl = TBL / f"{abl_exp}_main_long.csv"
    f_main = TBL / f"{main_exp}_main_long.csv"
    if not f_abl.exists():
        return {"ablation_table": str(f_abl)}
    abl = pd.read_csv(f_abl)
    abl["seed"] = abl["seed"].astype(str)
    abl_seeds = sorted(abl.seed.dropna().unique().tolist())
    frames = [abl[abl.method.isin(["sc_nocond", "sc_shuffled"])] ]
    if f_main.exists():
        mn = pd.read_csv(f_main)
        mn["seed"] = mn["seed"].astype(str)
        frames.append(mn[(mn.method == "sc_fac") & (mn.seed.isin(abl_seeds))])
    df = pd.concat(frames, ignore_index=True)
    Cs = sorted(df.C.unique())
    C_show = 1200.0 if 1200.0 in Cs else Cs[-1]
    lines = [r"\begin{tabular}{lcc}", r"\hline",
             f"variant & Money ($C{{=}}{int(C_show)}$, same 3 seeds) & flush cost\\\\"]
    for m in ["sc_fac", "sc_nocond", "sc_shuffled"]:
        g = df[(df.method == m) & (df.C == C_show)]
        if not len(g):
            continue
        money = g.money.to_numpy(float)
        mean = money.mean()
        se = money.std(ddof=1) / np.sqrt(len(money)) if len(money) > 1 else 0.0
        fl = g.flush.mean()
        lines.append(f"{METHOD_LABEL.get(m, m)} & {mean:.0f}$\\pm${se:.0f} & {fl:.0f}\\\\")
    lines += [r"\hline", r"\end{tabular}"]
    (TAB / "ablation.tex").write_text("\n".join(lines))
    return {}


def transfer_table(exp):
    f = TBL / f"{exp}_transfer_long.csv"
    if not f.exists():
        return {"transfer": str(f)}
    df = pd.read_csv(f)
    missing = {}
    for method in df.method.unique():
        sub = df[df.method == method]
        piv = sub.pivot_table(index="train_k", columns="test_k",
                              values="money", aggfunc="mean")
        ks = sorted(piv.index)
        # heatmap
        fig, ax = plt.subplots(figsize=(2.8, 2.4))
        mat = piv.loc[ks, ks].values
        im = ax.imshow(mat, cmap="viridis", aspect="auto")
        ax.set_xticks(range(len(ks))); ax.set_xticklabels(ks)
        ax.set_yticks(range(len(ks))); ax.set_yticklabels(ks)
        ax.set_xlabel("deploy $k$"); ax.set_ylabel("train $k$")
        for i in range(len(ks)):
            for j in range(len(ks)):
                v = mat[i, j]
                if not np.isnan(v):
                    ax.text(j, i, f"{v:.0f}", ha="center", va="center",
                            color="w", fontsize=5)
        fig.colorbar(im, ax=ax, fraction=.046)
        fig.tight_layout(); fig.savefig(FIG / f"transfer_{method}.pdf"); plt.close(fig)
        # latex
        lines = [r"\begin{tabular}{l" + "c" * len(ks) + "}", r"\hline",
                 "train/deploy & " + " & ".join(f"k={k}" for k in ks) + r"\\"]
        for i, kt in enumerate(ks):
            cells = [_fmt(piv.loc[kt, ke], 0) if ke in piv.columns else "--"
                     for ke in ks]
            lines.append(f"$k={kt}$ & " + " & ".join(cells) + r"\\")
        lines += [r"\hline", r"\end{tabular}"]
        (TAB / f"transfer_{method}.tex").write_text("\n".join(lines))
    # retention summary
    ret = {}
    setm = [m for m in df.method.unique() if m.startswith("set")]
    for m in setm:
        sub = df[df.method == m]
        piv = sub.pivot_table(index="train_k", columns="test_k", values="money",
                              aggfunc="mean")
        ks = [k for k in piv.index if k in piv.columns]
        diag = np.mean([piv.loc[k, k] for k in ks])
        off = [piv.loc[a, b] for a in ks for b in ks if a != b]
        ret[m] = {"diag": float(diag), "offdiag": float(np.mean(off)),
                  "retention_pct": float(100 * np.mean(off) / diag)}
    return {"transfer_retention": ret} if ret else missing


def switching_table():
    f = ROOT / "runs" / "switching" / "switch_summary.csv"
    if not f.exists():
        return {"switching": str(f)}
    df = pd.read_csv(f)
    pols = [p for p in ["FA", "FWF", "BFP0.5", "ja_ppo", "ifac", "sc_fac"]
            if p in df.policy.unique()]
    # figure: post-switch recoverable drops by policy (mean over pairs)
    grp = df.groupby("policy").post_recoverable_drops.mean().reindex(pols).dropna()
    fig, ax = plt.subplots(figsize=(3.2, 2.2))
    ax.bar(range(len(grp)), grp.values,
           color=[COLORS.get(p, "#333") for p in grp.index])
    ax.set_xticks(range(len(grp)))
    ax.set_xticklabels([METHOD_LABEL[p] for p in grp.index], rotation=30, ha="right",
                       fontsize=6)
    ax.set_ylabel("post-switch recoverable drops")
    fig.tight_layout(); fig.savefig(FIG / "switching_drops.pdf"); plt.close(fig)
    lines = [r"\begin{tabular}{lccc}", r"\hline",
             r"policy & Money & post Money & post rec. drops\\"]
    for p in pols:
        g = df[df.policy == p]
        lines.append(f"{METHOD_LABEL[p]} & {g.money.mean():.0f} & "
                     f"{g.post_money.mean():.0f} & {g.post_recoverable_drops.mean():.1f}\\\\")
    lines += [r"\hline", r"\end{tabular}"]
    (TAB / "switching.tex").write_text("\n".join(lines))
    return {}


def efficiency_table():
    import glob
    hits = glob.glob(str(ROOT / "runs" / "bench" / "bench_*.csv"))
    if not hits:
        return {"efficiency": "runs/bench/bench_*.csv"}
    df = pd.read_csv(sorted(hits)[-1]).set_index("method")
    order = ["ja_ppo", "ifac", "sc_fac", "sc_nocond", "set_ifac", "set_sc_fac"]
    # output-scaling figure: logits vs k for joint vs factorized
    ks = np.array([3, 6, 12, 24])
    fig, ax = plt.subplots(figsize=(2.8, 2.2))
    ax.plot(ks, (ks + 1) ** 2, "o-", color="#d95f02", label="joint $(k{+}1)^2$")
    ax.plot(ks, 2 * (ks + 1), "s-", color="#7570b3", label="factorized $2(k{+}1)$")
    ax.set_xlabel("wallets $k$"); ax.set_ylabel("output logits")
    ax.legend(fontsize=7); ax.grid(alpha=.3)
    fig.tight_layout(); fig.savefig(FIG / "output_scaling.pdf"); plt.close(fig)
    lines = [r"\begin{tabular}{lrrr}", r"\hline",
             r"policy & params & logits & latency (ms)\\"]
    for m in order:
        if m not in df.index:
            continue
        r = df.loc[m]
        lines.append(f"{METHOD_LABEL[m]} & {int(r.params):,} & {int(r.output_logits)} "
                     f"& {r.lat_mean_ms:.2f}\\\\")
    lines += [r"\hline", r"\end{tabular}"]
    (TAB / "efficiency.tex").write_text("\n".join(lines))
    return {}


def build_claims(exp, abl, kscale):
    """Headline numbers with explicit source-file pointers, read from the
    generated result CSVs. No number is typed here."""
    c = {"sources": {}}

    def src(key, rel):
        c["sources"][key] = rel

    f = TBL / f"{exp}_main_table.csv"
    if f.exists():
        df = pd.read_csv(f)
        m = {}
        for _, r in df.iterrows():
            m.setdefault(r.method, {})[int(r.C)] = {
                "money": round(float(r.money_mean), 1),
                "se": round(float(r.money_se), 1),
                "n_seeds": int(r.n_seeds),
                "reported_only_paper": None if pd.isna(r.reported) else float(r.reported)}
        c["main_money_by_method_C"] = m
        src("main", f"results/tables/{exp}_main_table.csv")

    fp = TBL / f"{exp}_paired.csv"
    if fp.exists():
        d = pd.read_csv(fp)
        c["paired_C1200"] = [
            {"contrast": r.contrast, "mean_diff": round(float(r.mean_diff), 1),
             "ci95": [round(float(r.lo), 1), round(float(r.hi), 1)],
             "p": round(float(r.p), 4), "wins": int(r.wins), "n": int(r.n)}
            for _, r in d[d.C == 1200].iterrows()]
        src("paired", f"results/tables/{exp}_paired.csv")

    fa = TBL / f"{abl}_paired.csv"
    if fa.exists():
        d = pd.read_csv(fa)
        c["ablation_paired"] = [
            {"C": int(r.C), "contrast": r.contrast,
             "mean_diff": round(float(r.mean_diff), 1),
             "ci95": [round(float(r.lo), 1), round(float(r.hi), 1)],
             "p": round(float(r.p), 4), "wins": int(r.wins), "n": int(r.n)}
            for _, r in d.iterrows()]
        src("ablation_paired", f"results/tables/{abl}_paired.csv")

    fs = TBL / "switching_summary.csv"
    if fs.exists():
        d = pd.read_csv(fs).set_index("policy")
        c["switching"] = {
            p: {"money": round(float(d.loc[p, "money"]), 1),
                "post_money": round(float(d.loc[p, "post_money"]), 1),
                "post_recoverable_drops": round(float(d.loc[p, "post_rec_drops"]), 2)}
            for p in ["FA", "FWF", "BFP0.5", "ja_ppo", "ifac", "sc_fac"] if p in d.index}
        src("switching", "results/tables/switching_summary.csv")
    fsp = TBL / "switching_paired_vs_bfp.csv"
    if fsp.exists():
        d = pd.read_csv(fsp).set_index("policy")
        c["switching_learned_minus_BFP0.5"] = {
            p: {"d_post_drops": round(float(d.loc[p, "d_drops_mean"]), 2),
                "d_money": round(float(d.loc[p, "d_money_mean"]), 1)}
            for p in d.index}
        src("switching_paired", "results/tables/switching_paired_vs_bfp.csv")

    import glob as _glob
    hits = sorted(_glob.glob(str(ROOT / "runs" / "bench" / "bench_*.csv")))
    if hits:
        src("efficiency", str(Path(hits[-1]).relative_to(ROOT)))
    return c


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--exp", default="matrix_main")
    ap.add_argument("--ablation", default="matrix_ablation")
    ap.add_argument("--kscale", default="kscale")
    args = ap.parse_args()
    FIG.mkdir(parents=True, exist_ok=True)
    TAB.mkdir(parents=True, exist_ok=True)
    claims = {"missing": {}}
    _, miss = main_table(args.exp)
    claims["missing"].update(miss)
    claims["missing"].update(ablation_table(args.ablation, args.exp))
    tr = transfer_table(args.kscale)
    claims["missing"].update({k: v for k, v in tr.items() if isinstance(v, str)})
    claims.update({k: v for k, v in tr.items() if not isinstance(v, str)})
    claims["missing"].update(switching_table())
    claims["missing"].update(efficiency_table())
    claims.update(build_claims(args.exp, args.ablation, args.kscale))
    (ASSETS / "paper_claims.json").write_text(json.dumps(claims, indent=2))
    print("assets written to", ASSETS)
    print("missing:", json.dumps(claims["missing"], indent=2))


if __name__ == "__main__":
    main()
