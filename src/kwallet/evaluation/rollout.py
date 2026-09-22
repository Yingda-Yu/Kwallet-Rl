"""Episode rollout and evaluation for learned policies and rule references."""
from __future__ import annotations

from typing import Callable, Dict, List

import numpy as np
import torch

from ..envs.kwallet import KWalletEnv, EnvConfig

_DROP_KEYS = ["oversize", "active_none", "frozen", "same_wallet_conflict",
              "insufficient"]


def _final(info: Dict, regime: str, ep: int) -> Dict:
    rec = {
        "regime": regime,
        "episode": ep,
        "money": info["money"],
        "accepted_value": info["accepted_value"],
        "accepted_count": info["accepted_count"],
        "drop_count": info["drop_count"],
        "charged_flushes": info["charged_flushes"],
        "attempted_flushes": info["attempted_flushes"],
        "invalid_flushes": info["invalid_flushes"],
    }
    for k in _DROP_KEYS:
        rec[f"drop_{k}"] = info["drop_reasons"].get(k, 0)
    return rec


@torch.no_grad()
def run_episode_learned(policy, env: KWalletEnv, stream: np.ndarray,
                        deterministic: bool = True) -> Dict:
    policy.eval()
    obs = env.reset(tx_stream=stream)
    done = False
    info = {}
    while not done:
        x = torch.tensor(obs, dtype=torch.float32,
                         device=next(policy.parameters()).device).unsqueeze(0)
        out = policy.step(x, deterministic=deterministic)
        a_s = int(out["a_settle"].item())
        a_f = int(out["a_flush"].item())
        obs, _, done, info = env.step(a_s, a_f)
    policy.train()
    return info


def run_episode_rule(rule_fn: Callable, env: KWalletEnv, stream: np.ndarray) -> Dict:
    obs = env.reset(tx_stream=stream)
    env._fwf_idx = 0
    done = False
    info = {}
    while not done:
        a_s, a_f = rule_fn(env)
        obs, _, done, info = env.step(int(a_s), int(a_f))
    return info


def evaluate_pool(policy_or_rule, pool: np.ndarray, env_cfg: EnvConfig,
                  regime: str, kind: str = "learned",
                  deterministic: bool = True) -> List[Dict]:
    """Evaluate one pool (array of episodes). Returns per-episode records."""
    env = KWalletEnv(env_cfg)
    records = []
    for ep in range(pool.shape[0]):
        stream = pool[ep]
        if kind == "learned":
            info = run_episode_learned(policy_or_rule, env, stream, deterministic)
        else:
            info = run_episode_rule(policy_or_rule, env, stream)
        records.append(_final(info, regime, ep))
    return records


def evaluate_regimes(policy_or_rule, eval_pools: Dict[str, np.ndarray],
                     env_cfg: EnvConfig, kind: str = "learned",
                     deterministic: bool = True) -> List[Dict]:
    records = []
    for regime, pool in eval_pools.items():
        records.extend(evaluate_pool(policy_or_rule, pool, env_cfg, regime,
                                     kind=kind, deterministic=deterministic))
    return records
