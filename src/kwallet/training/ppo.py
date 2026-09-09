"""Shared PPO/GAE trainer for all three K-Wallet actor-critic policies.

All learned variants (JA-PPO, IFAC, SC-FAC) use the SAME environment, reward,
rollout protocol, advantage estimation and PPO update (paper Sec. IV.F-G); only
the policy distribution differs.

Rollouts are collected as WHOLE finite-horizon episodes (true termination at
t=T), so GAE bootstraps 0 at episode ends (no artificial truncation bootstrap).
"""
from __future__ import annotations

import os
import time
from dataclasses import dataclass, asdict
from typing import Dict, Optional

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

from ..envs.kwallet import KWalletEnv, EnvConfig
from ..policies.actors import build_policy


@dataclass
class PPOConfig:
    seed: int = 123
    device: str = "cpu"
    # model
    method: str = "sc_fac"
    hidden: int = 256
    embed: int = 32
    n_layers: int = 2
    # PPO
    lr: float = 3e-4
    gamma: float = 0.99
    gae_lambda: float = 0.95
    clip_eps: float = 0.2
    value_coef: float = 0.5
    entropy_start: float = 0.02
    entropy_end: float = 0.001
    max_grad_norm: float = 1.0
    update_epochs: int = 10
    minibatch_size: int = 512
    rollout_episodes: int = 8
    # budget
    total_episodes: int = 3000
    eval_every_episodes: int = 500
    # env
    reward_mode: str = "original"


def set_seed(seed: int):
    import random
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


class PPOTrainer:
    def __init__(self, cfg: PPOConfig, env_cfg: EnvConfig, train_pool: np.ndarray,
                 val_pool: Optional[np.ndarray] = None, val_episodes: int = 24):
        self.cfg = cfg
        self.env_cfg = env_cfg
        self.device = torch.device(cfg.device if cfg.device == "cpu"
                                   or torch.cuda.is_available() else "cpu")
        set_seed(cfg.seed)
        self.env = KWalletEnv(env_cfg)
        self.policy = build_policy(
            cfg.method, env_cfg.obs_dim, env_cfg.k,
            hidden=cfg.hidden, embed=cfg.embed, n_layers=cfg.n_layers
        ).to(self.device)
        self.opt = optim.Adam(self.policy.parameters(), lr=cfg.lr)
        self.train_pool = train_pool
        self.val_pool = val_pool
        self.val_episodes = val_episodes
        self.n_train = train_pool.shape[0]
        # training stream order (reshuffled each pass)
        self._order_rng = np.random.default_rng(cfg.seed)
        self._pool_pos = 0
        self._order = self._order_rng.permutation(self.n_train)
        self.episode = 0
        self.history = []

    # ------------------------------------------------------------------
    def _next_stream(self) -> np.ndarray:
        if self._pool_pos >= self.n_train:
            self._order = self._order_rng.permutation(self.n_train)
            self._pool_pos = 0
        idx = self._order[self._pool_pos]
        self._pool_pos += 1
        return self.train_pool[idx]

    def _entropy_coef(self) -> float:
        frac = min(1.0, self.episode / max(1, self.cfg.total_episodes))
        return self.cfg.entropy_start + frac * (
            self.cfg.entropy_end - self.cfg.entropy_start)

    # ------------------------------------------------------------------
    def collect_rollout(self):
        """Collect whole episodes; returns flat tensors + episode metrics."""
        obs_b, as_b, af_b, logp_b, val_b, rew_b, done_b = [], [], [], [], [], [], []
        ep_money, ep_reward, ep_accept, ep_flush = [], [], [], []
        episodes = 0
        while episodes < self.cfg.rollout_episodes:
            stream = self._next_stream()
            obs = self.env.reset(tx_stream=stream)
            ep_done = False
            while not ep_done:
                x = torch.tensor(obs, dtype=torch.float32, device=self.device).unsqueeze(0)
                with torch.no_grad():
                    out = self.policy.step(x, deterministic=False)
                a_s = int(out["a_settle"].item())
                a_f = int(out["a_flush"].item())
                obs2, r, done, info = self.env.step(a_s, a_f)
                obs_b.append(obs)
                as_b.append(a_s)
                af_b.append(a_f)
                logp_b.append(float(out["log_prob"].item()))
                val_b.append(float(out["value"].item()))
                rew_b.append(r)
                done_b.append(bool(done))
                obs = obs2
                ep_done = done
            ep_money.append(info["money"])
            ep_reward.append(info["episode_reward"])
            ep_accept.append(info["accepted_value"])
            ep_flush.append(info["charged_flushes"])
            self.episode += 1
            episodes += 1
        return {
            "obs": torch.tensor(np.asarray(obs_b), dtype=torch.float32, device=self.device),
            "a_settle": torch.tensor(as_b, dtype=torch.long, device=self.device),
            "a_flush": torch.tensor(af_b, dtype=torch.long, device=self.device),
            "old_logp": torch.tensor(logp_b, dtype=torch.float32, device=self.device),
            "old_value": torch.tensor(val_b, dtype=torch.float32, device=self.device),
            "reward": torch.tensor(rew_b, dtype=torch.float32, device=self.device),
            "done": torch.tensor(done_b, dtype=torch.float32, device=self.device),
            "ep_money": ep_money, "ep_reward": ep_reward,
            "ep_accept": ep_accept, "ep_flush": ep_flush,
        }

    def gae(self, batch) -> tuple:
        rew, done, val = batch["reward"], batch["done"], batch["old_value"]
        n = rew.shape[0]
        adv = torch.zeros(n, device=self.device)
        gae = torch.zeros(1, device=self.device)
        for t in reversed(range(n)):
            next_nonterminal = 1.0 - done[t]
            next_value = val[t + 1] if t + 1 < n else torch.zeros(1, device=self.device)
            delta = rew[t] + self.cfg.gamma * next_value * next_nonterminal - val[t]
            gae = delta + self.cfg.gamma * self.cfg.gae_lambda * next_nonterminal * gae
            adv[t] = gae
        returns = adv + val
        return adv, returns

    def update(self, batch) -> Dict[str, float]:
        adv, returns = self.gae(batch)
        adv = (adv - adv.mean()) / (adv.std() + 1e-8)
        ent_coef = self._entropy_coef()
        n = batch["obs"].shape[0]
        last = {"policy_loss": 0.0, "value_loss": 0.0, "entropy": 0.0, "approx_kl": 0.0}
        for _ in range(self.cfg.update_epochs):
            idx = torch.randperm(n, device=self.device)
            for start in range(0, n, self.cfg.minibatch_size):
                mb = idx[start:start + self.cfg.minibatch_size]
                out = self.policy.evaluate_actions(
                    batch["obs"][mb], batch["a_settle"][mb], batch["a_flush"][mb])
                logp = out["log_prob"]
                ratio = torch.exp(logp - batch["old_logp"][mb])
                with torch.no_grad():
                    last["approx_kl"] = float((batch["old_logp"][mb] - logp).mean().item())
                surr1 = ratio * adv[mb]
                surr2 = torch.clamp(ratio, 1 - self.cfg.clip_eps,
                                    1 + self.cfg.clip_eps) * adv[mb]
                policy_loss = -torch.min(surr1, surr2).mean()
                value_loss = (out["value"] - returns[mb]).pow(2).mean()
                entropy = out["entropy"].mean()
                loss = policy_loss + self.cfg.value_coef * value_loss - ent_coef * entropy
                self.opt.zero_grad()
                loss.backward()
                nn.utils.clip_grad_norm_(self.policy.parameters(), self.cfg.max_grad_norm)
                self.opt.step()
                last = {"policy_loss": float(policy_loss.item()),
                        "value_loss": float(value_loss.item()),
                        "entropy": float(entropy.item()),
                        "approx_kl": last["approx_kl"]}
        return last

    def _eval_val(self) -> float:
        """Deterministic Money on a fixed validation slice (budget selection)."""
        from ..evaluation.rollout import run_episode_learned
        if self.val_pool is None:
            return float("nan")
        moneys = []
        n = min(self.val_episodes, self.val_pool.shape[0])
        for i in range(n):
            info = run_episode_learned(self.policy, self.env, self.val_pool[i],
                                       deterministic=True)
            moneys.append(info["money"])
        return float(np.mean(moneys))

    # ------------------------------------------------------------------
    def train(self, eval_fn=None, verbose: bool = True) -> Dict:
        start = time.time()
        while self.episode < self.cfg.total_episodes:
            batch = self.collect_rollout()
            stats = self.update(batch)
            rec = {
                "episode": self.episode,
                "train_money_mean": float(np.mean(batch["ep_money"])),
                "train_reward_mean": float(np.mean(batch["ep_reward"])),
                "train_accept_mean": float(np.mean(batch["ep_accept"])),
                "train_flush_mean": float(np.mean(batch["ep_flush"])),
                "entropy_coef": self._entropy_coef(),
                "policy_loss": stats["policy_loss"],
                "value_loss": stats["value_loss"],
                "entropy": stats["entropy"],
                "approx_kl": stats["approx_kl"],
                "val_money": self._eval_val() if (
                    self.episode % self.cfg.eval_every_episodes == 0
                    or self.episode >= self.cfg.total_episodes) else float("nan"),
                "elapsed": time.time() - start,
            }
            self.history.append(rec)
            if verbose:
                print(f"[{self.cfg.method}|seed{self.cfg.seed}] ep={self.episode:5d} "
                      f"money={rec['train_money_mean']:9.1f} acc={rec['train_accept_mean']:9.1f} "
                      f"flush={rec['train_flush_mean']:6.1f} vL={rec['value_loss']:.4f} "
                      f"ent={rec['entropy']:.3f} kl={rec['approx_kl']:.4f} "
                      f"t={rec['elapsed']:.0f}s", flush=True)
        return {"history": self.history, "episode": self.episode}

    # ------------------------------------------------------------------
    def checkpoint(self, path: str) -> None:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        torch.save({
            "model": self.policy.state_dict(),
            "optimizer": self.opt.state_dict(),
            "episode": self.episode,
            "config": asdict(self.cfg),
            "env_config": asdict(self.env_cfg),
            "torch_rng": torch.get_rng_state(),
            "numpy_rng": np.random.get_state(),
        }, path)

    def load_checkpoint(self, path: str) -> None:
        ckpt = torch.load(path, map_location=self.device, weights_only=False)
        self.policy.load_state_dict(ckpt["model"])
        if "optimizer" in ckpt:
            self.opt.load_state_dict(ckpt["optimizer"])
        self.episode = ckpt.get("episode", 0)
