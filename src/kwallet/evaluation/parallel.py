"""Process-parallel evaluation.

The single-environment rollout logic in ``rollout.py`` is the tested source of
truth. To evaluate the 2400-episode test pools quickly we shard episodes across
worker processes, each running the IDENTICAL single-env rollout on its shard.
No environment logic is reimplemented -> results are numerically identical to
serial evaluation up to the order of independent episodes.
"""
from __future__ import annotations

import os
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import Dict, List, Optional

import numpy as np

from ..envs.kwallet import EnvConfig
from .rollout import evaluate_pool

_G = {}


def _init_worker(env_kwargs: dict, method: str, kind: str,
                 checkpoint: Optional[str], threads: int,
                 hidden: int = 256, embed: int = 32, n_layers: int = 2):
    os.environ["OMP_NUM_THREADS"] = str(threads)
    os.environ["MKL_NUM_THREADS"] = str(threads)
    import torch
    torch.set_num_threads(threads)
    env_cfg = EnvConfig(**env_kwargs)
    if kind == "learned":
        from ..policies.actors import build_policy
        pol = build_policy(method, env_cfg.obs_dim, env_cfg.k,
                           hidden=hidden, embed=embed, n_layers=n_layers)
        if checkpoint:
            data = torch.load(checkpoint, map_location="cpu", weights_only=False)
            pol.load_state_dict(data["model"])
        pol.eval()
        _G["policy"] = pol
    else:
        from ..baselines.rules import RULE_POLICIES
        _G["policy"] = RULE_POLICIES[method]
    _G["env_cfg"] = env_cfg
    _G["kind"] = kind


def _shard(task):
    regime, shard, start, deterministic = task
    from .rollout import run_episode_learned, run_episode_rule
    from ..envs.kwallet import KWalletEnv
    env = KWalletEnv(_G["env_cfg"])
    out = []
    drop_keys = ["oversize", "active_none", "frozen", "same_wallet_conflict",
                 "insufficient"]
    for j in range(shard.shape[0]):
        stream = shard[j]
        if _G["kind"] == "learned":
            info = run_episode_learned(_G["policy"], env, stream, deterministic)
        else:
            info = run_episode_rule(_G["policy"], env, stream)
        rec = {"regime": regime, "episode": start + j,
               "money": info["money"],
               "accepted_value": info["accepted_value"],
               "accepted_count": info["accepted_count"],
               "drop_count": info["drop_count"],
               "charged_flushes": info["charged_flushes"],
               "attempted_flushes": info["attempted_flushes"],
               "invalid_flushes": info["invalid_flushes"]}
        for k in drop_keys:
            rec[f"drop_{k}"] = info["drop_reasons"].get(k, 0)
        out.append(rec)
    return out


def evaluate_regimes_parallel(method: str, checkpoint: Optional[str],
                              env_cfg: EnvConfig,
                              eval_pools: Dict[str, np.ndarray],
                              kind: str, workers: int = 8,
                              threads: int = 2, shard: int = 24,
                              deterministic: bool = True,
                              hidden: int = 256, embed: int = 32,
                              n_layers: int = 2) -> List[Dict]:
    tasks = []
    for regime, pool in eval_pools.items():
        for s in range(0, pool.shape[0], shard):
            tasks.append((regime, pool[s:s + shard], s, deterministic))
    env_kwargs = {f: getattr(env_cfg, f) for f in
                  ["C", "k", "F", "T", "max_tx", "alpha_drop", "beta_flush",
                   "value_scale", "p", "tau", "reward_mode"]}
    records: List[Dict] = []
    if workers <= 1:
        _init_worker(env_kwargs, method, kind, checkpoint, threads,
                     hidden, embed, n_layers)
        for t in tasks:
            records.extend(_shard(t))
        return records
    with ProcessPoolExecutor(
            max_workers=workers,
            initializer=_init_worker,
            initargs=(env_kwargs, method, kind, checkpoint, threads,
                      hidden, embed, n_layers)) as ex:
        futs = [ex.submit(_shard, t) for t in tasks]
        for f in as_completed(futs):
            records.extend(f.result())
    records.sort(key=lambda r: (r["regime"], r["episode"]))
    return records
