"""Command-line interface for K-Wallet reproduction/improvement pipeline.

Subcommands: doctor, gen-pools, train, evaluate, bench.
All commands exit non-zero on failure and save resolved configs/artifacts so
runs are traceable (run manifest).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import traceback
from pathlib import Path

import numpy as np
import pandas as pd

from .data.pools import build_pools
from .envs.kwallet import EnvConfig
from .evaluation.compute import benchmark_policy
from .evaluation.rollout import evaluate_regimes
from .evaluation.stats import paired_difference, summarize, to_frame
from .policies.actors import build_policy
from .baselines.rules import RULE_POLICIES
from .training.ppo import PPOConfig, PPOTrainer


def _env_cfg(a) -> EnvConfig:
    return EnvConfig(C=float(a.C), k=int(a.k), F=int(a.F), T=int(a.T),
                     reward_mode=getattr(a, "reward_mode", "original"))


def cmd_doctor(a) -> int:
    import torch
    print("== kwallet doctor ==")
    print("python:", sys.version.split()[0])
    print("numpy:", np.__version__, "| pandas:", pd.__version__)
    print("torch:", torch.__version__, "| cuda_available:", torch.cuda.is_available())
    cfg = EnvConfig(C=1200, k=24, F=3, T=1000)
    print("env: wallet_size=", cfg.wallet_size, "obs_dim=", cfg.obs_dim,
          "n_actions=", cfg.n_actions)
    # tiny env smoke
    from .envs.kwallet import KWalletEnv
    env = KWalletEnv(cfg)
    stream = np.full(cfg.T, 30.0)
    obs = env.reset(tx_stream=stream)
    assert obs.shape[0] == cfg.obs_dim
    obs2, r, done, info = env.step(cfg.k, cfg.k)  # no-op
    print("env smoke: obs", obs.shape, "reward", round(r, 4), "done", done)
    # policy build smoke
    for m in ["ja_ppo", "ifac", "sc_fac"]:
        pol = build_policy(m, cfg.obs_dim, cfg.k)
        import torch as T
        out = pol.step(T.zeros(1, cfg.obs_dim))
        print(f"  {m}: logits={pol.output_logits()} a_s={int(out['a_settle'].item())}")
    print("doctor OK")
    return 0


def cmd_gen_pools(a) -> int:
    t0 = time.time()
    bundle = build_pools(
        episode_length=a.T,
        train_episodes=a.train,
        val_episodes=a.val,
        eval_per_regime=a.eval,
        base_seed=a.base_seed,
        force_regenerate=a.force,
    )
    print(f"pools built in {time.time()-t0:.1f}s")
    print("train:", bundle.train.shape, "val:", bundle.val.shape)
    for r in list(bundle.eval_pools)[:3]:
        print(" ", r, bundle.eval_pools[r].shape)
    print("hashes:")
    for k, v in bundle.manifest.get("hashes", {}).items():
        print(f"  {k}: {v[:16]}...")
    return 0


def _run_dir(a) -> Path:
    tag = a.exp
    d = Path(a.out) / tag / f"{a.method}_C{a.C}_k{a.k}_F{a.F}_s{a.seed}"
    d.mkdir(parents=True, exist_ok=True)
    return d


def cmd_train(a) -> int:
    import torch
    d = _run_dir(a)
    env_cfg = _env_cfg(a)
    bundle = build_pools(episode_length=a.T, train_episodes=a.pool_train,
                         val_episodes=300, eval_per_regime=a.pool_eval,
                         base_seed=a.base_seed)
    cfg = PPOConfig(
        seed=int(a.seed), device=a.device, method=a.method,
        hidden=int(a.hidden), embed=int(a.embed), n_layers=int(a.n_layers),
        lr=float(a.lr), total_episodes=int(a.episodes),
        rollout_episodes=int(a.rollout), minibatch_size=int(a.mb),
        update_epochs=int(a.epochs), entropy_start=float(a.ent0),
        entropy_end=float(a.ent1), reward_mode=a.reward_mode,
    )
    (d / "resolved_config.json").write_text(json.dumps(
        {"ppo": cfg.__dict__, "env": env_cfg.__dict__,
         "data_manifest_hashes": bundle.manifest.get("hashes", {})},
        indent=2, default=str))
    trainer = PPOTrainer(cfg, env_cfg, bundle.train, val_pool=bundle.val)
    trainer.train(verbose=True)
    trainer.checkpoint(str(d / "checkpoint.pt"))
    pd.DataFrame(trainer.history).to_csv(d / "history.csv", index=False)
    print("saved to", d)
    return 0


def _load_policy(a, env_cfg):
    import torch
    pol = build_policy(a.method, env_cfg.obs_dim, env_cfg.k,
                       hidden=int(a.hidden), embed=int(a.embed),
                       n_layers=int(a.n_layers)).to(a.device)
    ck = Path(a.checkpoint) if a.checkpoint else None
    if ck and ck.exists():
        data = torch.load(str(ck), map_location=a.device, weights_only=False)
        pol.load_state_dict(data["model"])
        print("loaded checkpoint", ck, "episode", data.get("episode"))
    else:
        print("WARNING: no checkpoint -> evaluating UNTRAINED policy", flush=True)
    return pol


def _default_ckpt(a):
    d = Path(a.out) / a.exp / f"{a.method}_C{a.C}_k{a.k}_F{a.F}_s{a.seed}" / "checkpoint.pt"
    return str(d) if d.exists() else None


def cmd_evaluate(a) -> int:
    from .evaluation.parallel import evaluate_regimes_parallel
    env_cfg = _env_cfg(a)
    bundle = build_pools(episode_length=a.T, train_episodes=5000,
                         val_episodes=300, eval_per_regime=a.pool_eval,
                         base_seed=a.base_seed)
    kind = "rule" if a.method in RULE_POLICIES else "learned"
    ckpt = None if kind == "rule" else (a.checkpoint or _default_ckpt(a))
    if kind == "learned" and ckpt is None:
        print("WARNING: no checkpoint -> evaluating UNTRAINED policy", flush=True)
    records = evaluate_regimes_parallel(
        a.method, ckpt, env_cfg, bundle.eval_pools, kind=kind,
        workers=int(a.workers), threads=int(a.eval_threads),
        deterministic=not a.stochastic,
        hidden=int(a.hidden), embed=int(a.embed), n_layers=int(a.n_layers))
    df = to_frame(records)
    d = Path(a.out) / a.exp
    d.mkdir(parents=True, exist_ok=True)
    fname = f"eval_{a.method}_C{a.C}_k{a.k}_F{a.F}"
    if a.method not in RULE_POLICIES:
        fname += f"_s{a.seed}"
    df.to_csv(d / (fname + ".csv"), index=False)
    summ = summarize(df)
    summ.to_csv(d / (fname + "_summary.csv"), index=False)
    # tau post-hoc repricing: Money = accepted_value - tau*charged_flushes
    tau_rows = []
    for tau in [1, 5, 10, 20]:
        m = (df["accepted_value"] - tau * df["charged_flushes"]).mean()
        tau_rows.append({"tau": tau, "money_mean": float(m)})
    pd.DataFrame(tau_rows).to_csv(d / (fname + "_tau_posthoc.csv"), index=False)
    print(summ.to_string(index=False))
    print("tau post-hoc:", tau_rows)
    return 0


def cmd_bench(a) -> int:
    env_cfg = _env_cfg(a)
    rows = []
    for m in ["ja_ppo", "ifac", "sc_fac"]:
        rows.append(benchmark_policy(m, env_cfg.obs_dim, env_cfg.k,
                                     hidden=int(a.hidden), embed=int(a.embed),
                                     device=a.device, repeats=a.repeats))
    df = pd.DataFrame(rows)
    d = Path(a.out) / a.exp
    d.mkdir(parents=True, exist_ok=True)
    df.to_csv(d / f"bench_C{a.C}_k{a.k}.csv", index=False)
    print(df.to_string(index=False))
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="kwallet")
    sub = p.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("doctor")
    sp.set_defaults(func=cmd_doctor)

    sp = sub.add_parser("gen-pools")
    sp.add_argument("--T", type=int, default=1000)
    sp.add_argument("--train", type=int, default=5000)
    sp.add_argument("--val", type=int, default=300)
    sp.add_argument("--eval", type=int, default=200)
    sp.add_argument("--base-seed", type=int, default=532)
    sp.add_argument("--force", action="store_true")
    sp.set_defaults(func=cmd_gen_pools)

    def add_env(s):
        s.add_argument("--C", type=float, default=1200.0)
        s.add_argument("--k", type=int, default=24)
        s.add_argument("--F", type=int, default=3)
        s.add_argument("--T", type=int, default=1000)
        s.add_argument("--reward-mode", default="original")
        s.add_argument("--base-seed", type=int, default=532)
        s.add_argument("--exp", default="smoke")
        s.add_argument("--out", default="runs")

    sp = sub.add_parser("train")
    add_env(sp)
    sp.add_argument("--method", default="sc_fac",
                    choices=["ja_ppo", "ifac", "sc_fac"])
    sp.add_argument("--seed", type=int, default=123)
    sp.add_argument("--episodes", type=int, default=3000)
    sp.add_argument("--rollout", type=int, default=8)
    sp.add_argument("--epochs", type=int, default=10)
    sp.add_argument("--mb", type=int, default=512)
    sp.add_argument("--lr", type=float, default=3e-4)
    sp.add_argument("--hidden", type=int, default=256)
    sp.add_argument("--embed", type=int, default=32)
    sp.add_argument("--n-layers", type=int, default=2)
    sp.add_argument("--ent0", type=float, default=0.02)
    sp.add_argument("--ent1", type=float, default=0.001)
    sp.add_argument("--device", default="cpu")
    sp.add_argument("--pool-train", type=int, default=5000)
    sp.add_argument("--pool-eval", type=int, default=200)
    sp.set_defaults(func=cmd_train)

    sp = sub.add_parser("evaluate")
    add_env(sp)
    sp.add_argument("--method", default="sc_fac",
                    choices=["ja_ppo", "ifac", "sc_fac", "FA", "FWF"])
    sp.add_argument("--seed", type=int, default=123)
    sp.add_argument("--checkpoint", default=None)
    sp.add_argument("--hidden", type=int, default=256)
    sp.add_argument("--embed", type=int, default=32)
    sp.add_argument("--n-layers", type=int, default=2)
    sp.add_argument("--device", default="cpu")
    sp.add_argument("--pool-eval", type=int, default=200)
    sp.add_argument("--stochastic", action="store_true")
    sp.add_argument("--workers", type=int, default=8)
    sp.add_argument("--eval-threads", type=int, default=2)
    sp.set_defaults(func=cmd_evaluate)

    sp = sub.add_parser("bench")
    add_env(sp)
    sp.add_argument("--hidden", type=int, default=256)
    sp.add_argument("--embed", type=int, default=32)
    sp.add_argument("--device", default="cpu")
    sp.add_argument("--repeats", type=int, default=2000)
    sp.set_defaults(func=cmd_bench)
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return int(args.func(args) or 0)
    except Exception as e:  # noqa: BLE001
        print(f"ERROR in '{args.cmd}': {e}", file=sys.stderr)
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
