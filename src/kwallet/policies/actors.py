"""Actor-critic policies for K-Wallet: JA-PPO, IFAC, SC-FAC.

All three share an MLP backbone ``h = f(s)`` and a value head ``V(s)`` and
differ ONLY in the policy distribution over (a_s, a_f), exactly as paper
Sec. IV.E-G:

* JA-PPO : one joint categorical over (k+1)^2 logits.
* IFAC   : two independent categoricals over (k+1) each;
           log pi = log pi_s(a_s|s) + log pi_f(a_f|s).
* SC-FAC : sample a_s, embed it (dim E), flush head reads [h, e(a_s)];
           log pi = log pi_s(a_s|s) + log pi_f(a_f|s, a_s).
           Emits 2(k+1) logits; adds the settlement->flush information path.

PPO correctness notes (paper Sec. IV.F + task brief 6.2):
* Rollout stores (obs, a_s, a_f, joint log-prob, value, reward, done).
* On update, SC-FAC's conditional flush head uses the STORED sampled a_s (it
  never re-samples a settle action).
* The PPO ratio uses the JOINT log-prob of the chosen parameterization.
* Conditional entropy for SC-FAC is H(A_s|s) + E_{a_s}[H(A_f|s,a_s)]; the
  cheap/standard Monte Carlo estimate H(A_s|s)+H(A_f|s,a_s^{samp}) is used for
  the entropy bonus (unbiased), and an exact-enumeration version is provided for
  small-k validation/diagnostics.
"""
from __future__ import annotations

from typing import Dict, Optional

import torch
import torch.nn as nn
from torch.distributions import Categorical


def _mlp(sizes, act=nn.ReLU):
    layers = []
    for i in range(len(sizes) - 1):
        layers.append(nn.Linear(sizes[i], sizes[i + 1]))
        if i < len(sizes) - 2:
            layers.append(act())
    return nn.Sequential(*layers)


class BaseActorCritic(nn.Module):
    """Shared backbone + value head. Subclasses define the policy heads."""

    method: str = "base"

    def __init__(self, obs_dim: int, k: int, hidden: int = 256,
                 embed: int = 32, n_layers: int = 2):
        super().__init__()
        self.obs_dim = obs_dim
        self.k = k
        self.n = k + 1  # actions per component (k wallets + no-op)
        self.hidden = hidden
        self.embed = embed
        enc_sizes = [obs_dim] + [hidden] * n_layers
        self.encoder = _mlp(enc_sizes)
        self.value_head = nn.Linear(hidden, 1)

    def encode(self, x):
        return self.encoder(x)

    def value(self, x):
        return self.value_head(self.encode(x)).squeeze(-1)

    # ---- to be implemented by subclasses ----
    def step(self, x: torch.Tensor, deterministic: bool = False) -> Dict[str, torch.Tensor]:
        raise NotImplementedError

    def evaluate_actions(self, x: torch.Tensor, a_settle: torch.Tensor,
                         a_flush: torch.Tensor) -> Dict[str, torch.Tensor]:
        """Recompute joint log-prob / entropy / value for stored actions."""
        raise NotImplementedError

    def output_logits(self) -> int:
        """Number of policy logits emitted per step (paper Fig. 4 quantity)."""
        raise NotImplementedError


class JAPPO(BaseActorCritic):
    """Flat joint-action PPO: (k+1)^2 logits."""

    method = "ja_ppo"

    def __init__(self, obs_dim, k, hidden=256, embed=32, n_layers=2):
        super().__init__(obs_dim, k, hidden, embed, n_layers)
        self.joint_head = nn.Linear(hidden, self.n * self.n)

    def _joint_dist(self, x):
        h = self.encode(x)
        logits = self.joint_head(h)
        return Categorical(logits=logits), self.value_head(h).squeeze(-1)

    def step(self, x, deterministic=False):
        dist, value = self._joint_dist(x)
        if deterministic:
            joint = logits_argmax(dist)
        else:
            joint = dist.sample()
        a_s = torch.div(joint, self.n, rounding_mode="floor")
        a_f = joint % self.n
        return {"a_settle": a_s, "a_flush": a_f,
                "log_prob": dist.log_prob(joint),
                "entropy": dist.entropy(), "value": value}

    def evaluate_actions(self, x, a_settle, a_flush):
        dist, value = self._joint_dist(x)
        joint = a_settle * self.n + a_flush
        return {"log_prob": dist.log_prob(joint),
                "entropy": dist.entropy(), "value": value}

    def output_logits(self):
        return self.n * self.n


class IFAC(BaseActorCritic):
    """Independent factorized actor-critic: two independent heads, 2(k+1)."""

    method = "ifac"

    def __init__(self, obs_dim, k, hidden=256, embed=32, n_layers=2):
        super().__init__(obs_dim, k, hidden, embed, n_layers)
        self.settle_head = nn.Linear(hidden, self.n)
        self.flush_head = nn.Linear(hidden, self.n)

    def _dists(self, x):
        h = self.encode(x)
        ds = Categorical(logits=self.settle_head(h))
        df = Categorical(logits=self.flush_head(h))
        return ds, df, self.value_head(h).squeeze(-1)

    def step(self, x, deterministic=False):
        ds, df, value = self._dists(x)
        a_s = logits_argmax(ds) if deterministic else ds.sample()
        a_f = logits_argmax(df) if deterministic else df.sample()
        return {"a_settle": a_s, "a_flush": a_f,
                "log_prob": ds.log_prob(a_s) + df.log_prob(a_f),
                "entropy": ds.entropy() + df.entropy(), "value": value}

    def evaluate_actions(self, x, a_settle, a_flush):
        ds, df, value = self._dists(x)
        return {"log_prob": ds.log_prob(a_settle) + df.log_prob(a_flush),
                "entropy": ds.entropy() + df.entropy(), "value": value}

    def output_logits(self):
        return 2 * self.n


class SCFAC(BaseActorCritic):
    """Settle-conditioned factorized actor-critic: pi = pi_s(a_s|s) pi_f(a_f|s,a_s)."""

    method = "sc_fac"

    def __init__(self, obs_dim, k, hidden=256, embed=32, n_layers=2):
        super().__init__(obs_dim, k, hidden, embed, n_layers)
        self.settle_head = nn.Linear(hidden, self.n)
        self.settle_embed = nn.Embedding(self.n, embed)
        # flush head reads fused [h, e(a_s)]
        self.flush_head = _mlp([hidden + embed, hidden, self.n])

    def _settle_dist(self, x):
        h = self.encode(x)
        return Categorical(logits=self.settle_head(h)), h

    def _flush_logits(self, h, a_settle):
        e = self.settle_embed(a_settle)
        return self.flush_head(torch.cat([h, e], dim=-1))

    def step(self, x, deterministic=False):
        ds, h = self._settle_dist(x)
        a_s = logits_argmax(ds) if deterministic else ds.sample()
        df = Categorical(logits=self._flush_logits(h, a_s))
        a_f = logits_argmax(df) if deterministic else df.sample()
        log_prob = ds.log_prob(a_s) + df.log_prob(a_f)
        entropy = ds.entropy() + df.entropy()  # MC conditional entropy (sampled a_s)
        value = self.value_head(h).squeeze(-1)
        return {"a_settle": a_s, "a_flush": a_f, "log_prob": log_prob,
                "entropy": entropy, "value": value}

    def evaluate_actions(self, x, a_settle, a_flush):
        ds, h = self._settle_dist(x)
        # CRITICAL: condition on the STORED sampled settle action (no re-sample).
        df = Categorical(logits=self._flush_logits(h, a_settle))
        log_prob = ds.log_prob(a_settle) + df.log_prob(a_flush)
        entropy = ds.entropy() + df.entropy()  # MC estimate of conditional entropy
        value = self.value_head(h).squeeze(-1)
        return {"log_prob": log_prob, "entropy": entropy, "value": value}

    def conditional_entropy_exact(self, x: torch.Tensor) -> torch.Tensor:
        """Exact H(A_s|s) + sum_a pi_s(a) H(A_f|s,a) by enumerating all k+1 settle
        choices. Complexity O((k+1)) flush-head evals per state (diagnostic)."""
        ds, h = self._settle_dist(x)
        b = h.shape[0]
        # repeat each state n times, once per possible settle action
        h_rep = h.unsqueeze(1).expand(b, self.n, self.hidden).reshape(b * self.n, self.hidden)
        a_rep = torch.arange(self.n, device=h.device).unsqueeze(0).expand(b, self.n).reshape(-1)
        flush_logits = self._flush_logits(h_rep, a_rep).reshape(b, self.n, self.n)
        flush_probs = torch.softmax(flush_logits, dim=-1)
        flush_logp = torch.log_softmax(flush_logits, dim=-1)
        flush_ent = -(flush_probs * flush_logp).sum(-1)  # H(A_f|s,a) for each a
        cond_ent = (ds.probs * flush_ent).sum(-1)       # E_{a~pi_s} H(A_f|s,a)
        return ds.entropy() + cond_ent

    def output_logits(self):
        return 2 * self.n


def logits_argmax(dist: Categorical) -> torch.Tensor:
    return torch.argmax(dist.logits, dim=-1)


POLICY_REGISTRY = {
    "ja_ppo": JAPPO,
    "ifac": IFAC,
    "sc_fac": SCFAC,
}


def build_policy(method: str, obs_dim: int, k: int, hidden: int = 256,
                 embed: int = 32, n_layers: int = 2, **kw) -> BaseActorCritic:
    key = method.lower()
    if key not in POLICY_REGISTRY:
        raise ValueError(f"unknown method '{method}'; choose from {list(POLICY_REGISTRY)}")
    return POLICY_REGISTRY[key](obs_dim, k, hidden=hidden, embed=embed,
                                n_layers=n_layers, **kw)
