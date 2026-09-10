"""Non-stationary switching-stream evaluation (Phase-2 OOD), persisted to CSV.

Evaluates rule policies and (optionally) trained learned-policy checkpoints on
regime-spliced streams and writes one long-format CSV:
    runs/<exp>/switch_<policy>.csv  and an aggregated switch_summary.csv.

Rules need no checkpoint. Learned policies are located as
    runs/<train_exp>/<method>_C<C>_k<k>_F<F>_s<seed>/checkpoint.pt
and re-evaluated deterministically. Policies are trained on STATIONARY pools
only; the switch is seen only at test time.
"""
import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
import torch

from kwallet.baselines.rules import get_rule_fn
from kwallet.data.pools import build_pools
from kwallet.data.switching import SWITCH_PAIRS, build_switch_streams, switch_point
from kwallet.envs.kwallet import EnvConfig
from kwallet.evaluation.switch import evaluate_switch
from kwallet.policies.actors import build_policy

ROOT = Path(__file__).resolve().parents[1]
RULES = ["FA", "FWF", "BFP0.5"]


def env_cfg(C=1200, k=24, F=3, T=1000):
    return EnvConfig(C=C, k=k, F=F, T=T, max_tx=1000)


def eval_rules(cfg, pools, n, out):
    rows = []
    for name in RULES:
        fn = get_rule_fn(name)
        for (ra, rb, frac) in SWITCH_PAIRS:
            streams = build_switch_streams(pools, ra, rb, frac, n=n)
            sp = switch_point(ra, rb, frac, cfg.T)
            r = evaluate_switch(fn, cfg, streams, sp, is_rule=True,
                                deterministic=True)
            rows.append(dict(policy=name, kind="rule", a=ra, b=rb, frac=frac, **r))
        print(f"[rule] {name} done")
    df = pd.DataFrame(rows)
    df.to_csv(out / "switch_rules.csv", index=False)
    return df


def eval_learned(cfg, pools, n, out, train_exp, methods, seeds, hidden=256,
                 embed=32):
    rows = []
    for method in methods:
        for seed in seeds:
            ck = ROOT / "runs" / train_exp / \
                f"{method}_C{cfg.C}.0_k{cfg.k}_F{cfg.F}_s{seed}" / "checkpoint.pt"
            if not ck.exists():
                print(f"[skip] no checkpoint {ck}")
                continue
            pol = build_policy(method, cfg.obs_dim, cfg.k, hidden=hidden,
                               embed=embed)
            ck_obj = torch.load(ck, map_location="cpu", weights_only=False)
            pol.load_state_dict(ck_obj["model"])
            pol.eval()
            for (ra, rb, frac) in SWITCH_PAIRS:
                streams = build_switch_streams(pools, ra, rb, frac, n=n)
                sp = switch_point(ra, rb, frac, cfg.T)
                r = evaluate_switch(pol, cfg, streams, sp, is_rule=False,
                                    deterministic=True)
                rows.append(dict(policy=method, kind="learned", seed=seed,
                                 a=ra, b=rb, frac=frac, **r))
            print(f"[learned] {method} s{seed} done")
    if rows:
        df = pd.DataFrame(rows)
        df.to_csv(out / "switch_learned.csv", index=False)
        return df
    return pd.DataFrame()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--exp", default="switching")
    ap.add_argument("--train-exp", default="matrix_main")
    ap.add_argument("--C", type=float, default=1200)
    ap.add_argument("--n", type=int, default=200)
    ap.add_argument("--methods", nargs="*",
                    default=["sc_fac", "ifac", "ja_ppo"])
    ap.add_argument("--seeds", nargs="*", type=int, default=[123])
    ap.add_argument("--hidden", type=int, default=256)
    ap.add_argument("--embed", type=int, default=32)
    ap.add_argument("--no-learned", action="store_true")
    args = ap.parse_args()

    out = ROOT / "runs" / args.exp
    out.mkdir(parents=True, exist_ok=True)
    cfg = env_cfg(C=args.C)
    pools = build_pools(cfg.T, 5000, 300, 200, base_seed=532).eval_pools

    frames = [eval_rules(cfg, pools, args.n, out)]
    if not args.no_learned:
        df = eval_learned(cfg, pools, args.n, out, args.train_exp,
                          args.methods, args.seeds, args.hidden, args.embed)
        if len(df):
            frames.append(df)
    allf = pd.concat(frames, ignore_index=True)
    allf.to_csv(out / "switch_summary.csv", index=False)
    cols = ["policy", "a", "b", "frac", "money", "post_money",
            "post_recoverable_drops", "post_flush"]
    print(allf[cols].round(1).to_string(index=False))


if __name__ == "__main__":
    main()
