"""Permutation-equivariant set-encoder actor-critic policies (Phase-2 NEW).

The flat policies in ``actors.py`` run a full MLP over the concatenated
observation and emit per-index logits; their parameters depend on ``k`` and
they are NOT equivariant to wallet ordering. This module instead treats the k
wallets as a SET:

  per-wallet feature  w_i = [balance_i, available_i, frozen_i]   (3 dims)
  global context      g   = [tx_norm, progress]                  (2 dims)

A shared encoder phi(w_i, g) -> h_i is applied identically to every wallet;
permutation-invariant pooling gives a global wallet-state summary; per-wallet
score heads then emit settle / flush logits. Properties:

  * Permutation equivariance: permuting the wallets permutes the per-wallet
    action logits in the same way; chosen action probabilities and the value
    are invariant (tested in tests/test_set_equivariance.py).
  * Scale invariance of the WEIGHTS: no parameter has a k-dependent size, so a
    network trained at k1 can be loaded and evaluated at k2 (cross-k transfer).

Two factorizations are provided, matching the paper's information-path study:
  * SetIFAC  : independent settle and flush heads (flush does NOT see settle).
  * SetSCFAC : settle-conditioned flush; the flush head reads the SETTLED
    wallet's feature h_{a_s} (not its index), preserving equivariance.
"""
from __future__ import annotations

from typing import Dict

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


class _SetBase(nn.Module):
    """Set encoding + value head shared by set-IFAC and set-SCFAC."""

    method: str = "set_base"
    condition_settle: bool = False

    def __init__(self, obs_dim: int, k: int, hidden: int = 128,
                 embed: int = 32, n_layers: int = 2):
        super().__init__()
        self.obs_dim = obs_dim
        self.k = k
        self.n = k + 1
        self.hidden = hidden
        self.embed = embed
        assert obs_dim == 3 * k + 2, f"set encoder expects 3k+2 obs, got {obs_dim}"
        # shared per-wallet encoder: [w_i(3), g(2)] -> h_i(H)
        self.phi = _mlp([3 + 2] + [hidden] * n_layers)
        self.value_head = _mlp([hidden + 2, hidden, 1])
        # settle heads
        self.settle_w = nn.Linear(hidden + hidden + 2, 1)   # per-wallet settle
        self.settle_null = nn.Linear(hidden + 2, 1)         # do-not-settle
        # flush heads (built by subclasses); sized independent of k

    # ---- set encoding -------------------------------------------------
    def _split(self, x):
        b = x.shape[0]
        k = self.k
        bal = x[:, 0:k]
        avail = x[:, k:2 * k]
        freeze = x[:, 2 * k:3 * k]
        g = x[:, 3 * k:3 * k + 2]                       # (b,2)
        W = torch.stack([bal, avail, freeze], dim=-1)   # (b,k,3)
        return W, g

    def _encode_set(self, x):
        W, g = self._split(x)
        b, k, _ = W.shape
        g_exp = g.unsqueeze(1).expand(b, k, g.shape[-1])
        inp = torch.cat([W, g_exp], dim=-1)             # (b,k,5)
        h = self.phi(inp)                               # (b,k,H)
        pooled = h.mean(dim=1)                          # (b,H)
        return h, pooled, g

    def _settle_logits(self, h, pooled, g):
        b, k, H = h.shape
        p = pooled.unsqueeze(1).expand(b, k, H)
        ge = g.unsqueeze(1).expand(b, k, g.shape[-1])
        sw = self.settle_w(torch.cat([h, p, ge], dim=-1)).squeeze(-1)  # (b,k)
        sn = self.settle_null(torch.cat([pooled, g], dim=-1))          # (b,1)
        return torch.cat([sw, sn], dim=-1)                             # (b,k+1)

    def _settled_feature(self, h, a_settle):
        """Feature of the chosen settle wallet (zeros for null settle)."""
        b, k, H = h.shape
        valid = (a_settle < k).unsqueeze(-1).float()    # (b,1)
        idx = a_settle.clamp(max=k - 1).view(b, 1, 1).expand(b, 1, H)
        gathered = h.gather(1, idx).squeeze(1)          # (b,H)
        return gathered * valid

    # ---- to be implemented by subclasses ------------------------------
    def _flush_logits(self, h, pooled, g, a_settle):
        raise NotImplementedError

    # ---- common policy interface --------------------------------------
    def _value(self, pooled, g):
        return self.value_head(torch.cat([pooled, g], dim=-1)).squeeze(-1)

    def _distributions(self, x, a_settle=None):
        h, pooled, g = self._encode_set(x)
        ds = Categorical(logits=self._settle_logits(h, pooled, g))
        value = self._value(pooled, g)
        return ds, h, pooled, g, value

    def step(self, x, deterministic=False):
        ds, h, pooled, g, value = self._distributions(x)
        a_s = torch.argmax(ds.logits, dim=-1) if deterministic else ds.sample()
        fl = self._flush_logits(h, pooled, g, a_s)
        df = Categorical(logits=fl)
        a_f = torch.argmax(fl, dim=-1) if deterministic else df.sample()
        return {"a_settle": a_s, "a_flush": a_f,
                "log_prob": ds.log_prob(a_s) + df.log_prob(a_f),
                "entropy": ds.entropy() + df.entropy(), "value": value}

    def evaluate_actions(self, x, a_settle, a_flush):
        ds, h, pooled, g, value = self._distributions(x, a_settle)
        df = Categorical(logits=self._flush_logits(h, pooled, g, a_settle))
        return {"log_prob": ds.log_prob(a_settle) + df.log_prob(a_flush),
                "entropy": ds.entropy() + df.entropy(), "value": value}

    def output_logits(self):
        return 2 * self.n


class SetIFAC(_SetBase):
    """Independent factorized SET policy: flush head ignores settle choice."""

    method = "set_ifac"
    condition_settle = False

    def __init__(self, obs_dim, k, hidden=128, embed=32, n_layers=2):
        super().__init__(obs_dim, k, hidden, embed, n_layers)
        self.flush_w = nn.Linear(hidden + hidden + 2, 1)   # per-wallet flush
        self.flush_noop = nn.Linear(hidden + 2, 1)         # no-op flush

    def _flush_logits(self, h, pooled, g, a_settle=None):
        b, k, H = h.shape
        p = pooled.unsqueeze(1).expand(b, k, H)
        ge = g.unsqueeze(1).expand(b, k, g.shape[-1])
        fw = self.flush_w(torch.cat([h, p, ge], dim=-1)).squeeze(-1)  # (b,k)
        fn = self.flush_noop(torch.cat([pooled, g], dim=-1))          # (b,1)
        return torch.cat([fw, fn], dim=-1)                            # (b,k+1)


class SetSCFAC(_SetBase):
    """Settle-conditioned factorized SET policy (equivariant SC-FAC)."""

    method = "set_sc_fac"
    condition_settle = True

    def __init__(self, obs_dim, k, hidden=128, embed=32, n_layers=2):
        super().__init__(obs_dim, k, hidden, embed, n_layers)
        # flush heads read the settled wallet feature e_sel (dim H)
        self.flush_w = nn.Linear(hidden + hidden + 2 + hidden, 1)
        self.flush_noop = nn.Linear(hidden + 2 + hidden, 1)
        self._noop_bias = 0.0

    def _flush_logits(self, h, pooled, g, a_settle):
        b, k, H = h.shape
        e_sel = self._settled_feature(h, a_settle)       # (b,H)
        p = pooled.unsqueeze(1).expand(b, k, H)
        ge = g.unsqueeze(1).expand(b, k, g.shape[-1])
        ee = e_sel.unsqueeze(1).expand(b, k, H)
        fw = self.flush_w(torch.cat([h, p, ge, ee], dim=-1)).squeeze(-1)
        fn = self.flush_noop(torch.cat([pooled, g, e_sel], dim=-1))
        logits = torch.cat([fw, fn], dim=-1)
        if self._noop_bias:
            logits = logits.clone()
            logits[:, -1] = logits[:, -1] + self._noop_bias
        return logits


SET_POLICY_REGISTRY = {
    "set_ifac": SetIFAC,
    "set_sc_fac": SetSCFAC,
}


def build_set_policy(method: str, obs_dim: int, k: int, hidden: int = 128,
                     embed: int = 32, n_layers: int = 2,
                     noop_bias: float = 0.0, **kw) -> _SetBase:
    key = method.lower()
    if key not in SET_POLICY_REGISTRY:
        raise ValueError(f"unknown set method '{method}'; "
                         f"choose {list(SET_POLICY_REGISTRY)}")
    pol = SET_POLICY_REGISTRY[key](obs_dim, k, hidden=hidden, embed=embed,
                                   n_layers=n_layers, **kw)
    if noop_bias:
        # bias the flush no-op logit (index k) at init; stored as buffer-like attr
        if isinstance(pol, SetSCFAC):
            pol._noop_bias = float(noop_bias)
        else:
            with torch.no_grad():
                pol.flush_noop.bias.data.add_(float(noop_bias))
    return pol
