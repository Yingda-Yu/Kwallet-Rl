"""Evaluate policies on non-stationary switching streams (Phase-2 OOD).

Reports whole-episode Money AND pre-/post-switch window Money (accepted value
and flush cost accumulated separately for steps ``[0, sp)`` and ``[sp, T)``).
The post-switch window isolates adaptation to a regime the agent did not see
during (stationary) training.
"""
from __future__ import annotations

from typing import Callable, Dict, Optional

import numpy as np
import torch

from ..envs.kwallet import KWalletEnv


def _action(policy, env, obs, is_rule, deterministic):
    if is_rule:
        return policy(env)
    x = torch.tensor(obs, dtype=torch.float32).unsqueeze(0)
    with torch.no_grad():
        out = policy.step(x, deterministic=deterministic)
    return int(out["a_settle"].item()), int(out["a_flush"].item())


def run_switch_episode(policy, env: KWalletEnv, stream: np.ndarray,
                       switch_point: int, is_rule: bool,
                       deterministic: bool = True) -> Dict:
    obs = env.reset(tx_stream=np.asarray(stream, dtype=np.float64))
    done = False
    # window accumulators: accepted value, executed flushes, recoverable drops
    w = {"pre": {"av": 0.0, "fl": 0, "drop": 0},
         "post": {"av": 0.0, "fl": 0, "drop": 0}}
    while not done:
        a_s, a_f = _action(policy, env, obs, is_rule, deterministic)
        obs, _, done, info = env.step(a_s, a_f)
        win = "pre" if info["time"] <= switch_point else "post"
        if info["accepted"]:
            w[win]["av"] += info["tx"]
        else:
            if info["drop_reason"] in ("insufficient", "active_none",
                                       "same_wallet_conflict"):
                w[win]["drop"] += 1
        if info["flushed_wallet"] >= 0:
            w[win]["fl"] += 1
    p, tau = env.cfg.p, env.cfg.tau
    for win in w:
        w[win]["money"] = p * w[win]["av"] - tau * w[win]["fl"]
    total_money = p * env.accepted_value - tau * env.charged_flushes
    return {"money": total_money,
            "pre_money": w["pre"]["money"], "post_money": w["post"]["money"],
            "pre_accept": w["pre"]["av"], "post_accept": w["post"]["av"],
            "pre_flush": w["pre"]["fl"], "post_flush": w["post"]["fl"],
            "post_recoverable_drops": w["post"]["drop"]}


def evaluate_switch(policy, env_cfg, streams: np.ndarray, switch_point: int,
                    is_rule: bool, deterministic: bool = True) -> Dict:
    env = KWalletEnv(env_cfg)
    recs = [run_switch_episode(policy, env, s, switch_point, is_rule, deterministic)
            for s in streams]
    keys = recs[0].keys()
    agg = {k: float(np.mean([r[k] for r in recs])) for k in keys}
    agg["n"] = len(recs)
    agg["se_money"] = float(np.std([r["money"] for r in recs]) / np.sqrt(len(recs)))
    agg["se_post"] = float(np.std([r["post_money"] for r in recs]) / np.sqrt(len(recs)))
    return agg
