"""The one-settlement / one-flush K-Wallet environment.

Faithful reimplementation of the discrete K-Wallet instantiation described in
the paper *Settle-Conditioned Policy Learning for Streaming Transaction
Collateral Control* (old paper, Sec. III).

Semantics (locked from paper Eq. (1)-(7), the transition order in Sec. III.B,
and corroborated by the legacy DQN protocol note ``notes/idea3/code_protocol.md``):

* k homogeneous wallets, each capacity ``wallet_size = C / k``.
* An episode has horizon T steps. Each step a transaction value x_t arrives.
  The generator emits ONLY a value (no target wallet / route / sender).
* The policy chooses (a_s, a_f), each in {0..k} where 0..k-1 select a wallet
  and k denotes the no-op (None). At most one settlement and at most one flush.
* Transition order is **flush first, then settle**:
    1. If a_f < k (a flush is requested) AND wallet a_f is usable, the wallet
       is emptied, one flush is counted/charged, and it is made unavailable
       for the current decision and the next F-1 decisions (F decisions total),
       after which a pending refill restores it to full capacity.
    2. Settlement is then attempted with a_s.
* Acceptance (paper Eq. 1):
    y = 1 [ a_s != None , a_f != a_s , wallet a_s usable , balance[a_s] >= x ].
  If x > C/k no wallet can settle -> oversize drop for every policy.
* Flush indicator z = 1[a_f != None] in paper Eq. (2), but we separately record
  attempted / executed / charged / invalid flushes because a flush requested on
  an already-frozen wallet cannot execute and is not charged. A flush on a
  *usable* wallet always executes (and is charged) even when the same step's
  settlement then fails.

Observation (paper Eq. 6), dimension 3k+2 (74 at k=24):
    [ balances / (C/k)  (k) ]
    [ availability u     (k) ]  u_i = 1 if wallet i usable (PAPER convention;
    [ freeze timer r     (k) ]    note legacy code used the INVERTED flag)
    [ x / max_tx         (1) ]
    [ t / T              (1) ]  1-based progress: first step 1/T, last T/T.

Reward (``reward_mode='original'``, shaping disabled, paper Sec. V.B):
    accepted transaction: + x / 1000
    dropped transaction:  - alpha_drop  (alpha_drop = 0.02)
    each charged flush:  - beta_flush  (beta_flush = 0.01)

Evaluation Money metric (paper Eq. 4), computed in info (not the RL reward):
    Money = p * accepted_value - tau * charged_flushes   (default p=1, tau=10).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Dict, Optional, Tuple

import numpy as np

NONE = -1  # sentinel for "no wallet selected"; actions use integer k for no-op.


@dataclass
class EnvConfig:
    C: float = 1200.0          # total collateral budget
    k: int = 24                # number of wallets
    F: int = 3                 # freeze duration (wallet unavailable for F decisions after a flush)
    T: int = 1000              # episode horizon
    max_tx: float = 1000.0     # normalization scale for transaction value
    alpha_drop: float = 0.02   # penalty for a dropped transaction (original reward)
    beta_flush: float = 0.01   # penalty per charged flush (original reward)
    value_scale: float = 1000.0  # reward scale for accepted value (x / value_scale)
    p: float = 1.0             # Money value multiplier
    tau: float = 10.0          # Money cost per charged flush
    reward_mode: str = "original"  # 'original' | 'money_aligned'

    @property
    def wallet_size(self) -> float:
        return self.C / self.k

    @property
    def obs_dim(self) -> int:
        return 3 * self.k + 2

    @property
    def n_actions(self) -> int:
        return self.k + 1  # per action component: k wallets + no-op

    def validate(self) -> None:
        if self.k <= 0:
            raise ValueError(f"k must be positive, got {self.k}")
        if self.C <= 0:
            raise ValueError(f"C must be positive, got {self.C}")
        if self.F < 0:
            raise ValueError(f"F must be >= 0, got {self.F}")
        if self.T <= 0:
            raise ValueError(f"T must be positive, got {self.T}")
        if self.wallet_size <= 0:
            raise ValueError("wallet_size must be positive")


class KWalletEnv:
    """Discrete one-settlement/one-flush K-Wallet environment.

    Actions are passed as ``(a_settle, a_flush)`` integers in ``0..k`` where
    ``k`` is the no-op. Use :meth:`feasibility_masks` for advisory masks.
    """

    # drop primary-reason labels
    DROP_OVERSIZE = "oversize"
    DROP_NONE = "active_none"
    DROP_FROZEN = "frozen"
    DROP_CONFLICT = "same_wallet_conflict"
    DROP_INSUFFICIENT = "insufficient"

    def __init__(self, config: EnvConfig):
        config.validate()
        self.cfg = config
        self.k = config.k
        self.F = config.F
        self.T = config.T
        self.wallet_size = config.wallet_size
        self._rng = np.random.default_rng()
        self._stream: Optional[np.ndarray] = None
        self._stream_gen: Optional[Callable[[int], np.ndarray]] = None
        self.reset()

    # ------------------------------------------------------------------
    # reset / stream management
    # ------------------------------------------------------------------
    def reset(
        self,
        tx_stream: Optional[np.ndarray] = None,
        seed: Optional[int] = None,
    ) -> np.ndarray:
        if seed is not None:
            self._rng = np.random.default_rng(seed)
        if tx_stream is not None:
            tx_stream = np.asarray(tx_stream, dtype=np.float64).reshape(-1)
            if tx_stream.shape[0] < self.T:
                raise ValueError(
                    f"tx_stream length {tx_stream.shape[0]} < horizon T={self.T}"
                )
            self._stream = tx_stream
        else:
            self._stream = None
        self.balance = np.full(self.k, self.wallet_size, dtype=np.float64)
        self.cooldown = np.zeros(self.k, dtype=np.int64)  # steps until usable+refilled
        self.t = 0
        # cumulative counters (episode-level)
        self.accepted_value = 0.0
        self.accepted_count = 0
        self.drop_count = 0
        self.drop_reasons: Dict[str, int] = {
            self.DROP_OVERSIZE: 0,
            self.DROP_NONE: 0,
            self.DROP_FROZEN: 0,
            self.DROP_CONFLICT: 0,
            self.DROP_INSUFFICIENT: 0,
        }
        self.attempted_flushes = 0
        self.executed_flushes = 0
        self.charged_flushes = 0
        self.invalid_flushes = 0
        self.episode_reward = 0.0
        # Initial observation only needed when a stream is present.
        # __init__ calls reset() with no stream to init wallet state.
        self._current_tx = self._draw(0) if self._stream is not None else 0.0
        return self._obs()

    def _draw(self, t: int) -> float:
        if self._stream is not None:
            return float(self._stream[t])
        raise RuntimeError("no transaction stream provided; pass tx_stream to reset")

    # ------------------------------------------------------------------
    # observation / masks
    # ------------------------------------------------------------------
    def _obs(self) -> np.ndarray:
        avail = (self.cooldown == 0).astype(np.float64)
        bal = self.balance / self.wallet_size
        freeze = self.cooldown / float(self.F) if self.F > 0 else np.zeros(self.k)
        x_norm = self._current_tx / self.cfg.max_tx
        progress = (self.t + 1) / float(self.T)  # 1-based, last step = 1.0
        return np.concatenate(
            [bal, avail, freeze, [x_norm], [progress]]
        ).astype(np.float32)

    def availability(self) -> np.ndarray:
        """Boolean array: True if wallet i is usable at the current step."""
        return (self.cooldown == 0)

    def feasibility_masks(self) -> Tuple[np.ndarray, np.ndarray]:
        """Advisory masks over the k+1 settle and flush actions (True = feasible).

        These do NOT change the environment; an agent may still select an
        infeasible action (it then produces a recorded drop / invalid flush).
        Index k is always feasible (the no-op).
        """
        avail = self.availability()
        tx = self._current_tx
        settle_mask = np.zeros(self.k + 1, dtype=bool)
        settle_mask[self.k] = True  # no-op always allowed
        flush_mask = np.zeros(self.k + 1, dtype=bool)
        flush_mask[self.k] = True
        for i in range(self.k):
            if avail[i]:
                flush_mask[i] = True
                if self.balance[i] >= tx and tx <= self.wallet_size:
                    settle_mask[i] = True
        return settle_mask, flush_mask

    # ------------------------------------------------------------------
    # transition
    # ------------------------------------------------------------------
    def step(self, a_settle: int, a_flush: int) -> Tuple[np.ndarray, float, bool, Dict]:
        if not (0 <= a_settle <= self.k and 0 <= a_flush <= self.k):
            raise ValueError(f"actions must be in 0..{self.k}")
        tx = self._current_tx
        reward = 0.0

        # ---- Phase 1: flush (executes first) ----
        flushed_wallet = NONE
        if a_flush < self.k:  # a flush is requested (not the no-op)
            self.attempted_flushes += 1
            if self.cooldown[a_flush] == 0:  # usable -> flush executes
                self.balance[a_flush] = 0.0
                self.cooldown[a_flush] = self.F  # unavailable this + F-1 future decisions
                self.executed_flushes += 1
                self.charged_flushes += 1
                flushed_wallet = a_flush
                reward -= self.cfg.beta_flush
            else:  # request on an already-frozen wallet: cannot execute, not charged
                self.invalid_flushes += 1

        # ---- Phase 2: settle ----
        accepted = False
        drop_reason = None
        settled_wallet = NONE
        if tx > self.wallet_size:
            drop_reason = self.DROP_OVERSIZE
        elif a_settle >= self.k:  # no-op settle
            drop_reason = self.DROP_NONE
        elif self.cooldown[a_settle] != 0:
            # wallet unavailable (frozen). Note: a wallet flushed THIS step has
            # cooldown=F, so same-wallet flush+settle is caught here too; we
            # disambiguate the conflict case explicitly below.
            if a_settle == flushed_wallet:
                drop_reason = self.DROP_CONFLICT
            else:
                drop_reason = self.DROP_FROZEN
        elif a_settle == flushed_wallet:
            drop_reason = self.DROP_CONFLICT
        elif self.balance[a_settle] + 1e-9 < tx:
            drop_reason = self.DROP_INSUFFICIENT
        else:
            accepted = True
            settled_wallet = a_settle
            self.balance[a_settle] -= tx
            self.accepted_value += tx
            self.accepted_count += 1
            reward += tx / self.cfg.value_scale

        if accepted:
            if self.cfg.reward_mode == "money_aligned":
                # overwrite with money-aligned shaping (phase 2); keep flush term
                reward = (self.cfg.p * tx) / self.cfg.value_scale - self.cfg.beta_flush * (
                    1 if flushed_wallet != NONE else 0
                )
        else:
            self.drop_count += 1
            self.drop_reasons[drop_reason] += 1
            reward -= self.cfg.alpha_drop

        self.episode_reward += reward

        # ---- time advance + pending refills ----
        self.t += 1
        for i in range(self.k):
            if self.cooldown[i] > 0:
                self.cooldown[i] -= 1
                if self.cooldown[i] == 0:
                    self.balance[i] = self.wallet_size  # pending refill restores full

        done = self.t >= self.T
        if not done:
            self._current_tx = self._draw(self.t)
        else:
            self._current_tx = 0.0

        info = self._info(accepted, drop_reason, settled_wallet, flushed_wallet, tx)
        return self._obs(), reward, done, info

    def _info(self, accepted, drop_reason, settled_wallet, flushed_wallet, tx) -> Dict:
        money = self.cfg.p * self.accepted_value - self.cfg.tau * self.charged_flushes
        return {
            "accepted": bool(accepted),
            "drop_reason": drop_reason,
            "settled_wallet": int(settled_wallet),
            "flushed_wallet": int(flushed_wallet),
            "tx": float(tx),
            # episode-level cumulative metrics
            "accepted_value": float(self.accepted_value),
            "accepted_count": int(self.accepted_count),
            "drop_count": int(self.drop_count),
            "drop_reasons": dict(self.drop_reasons),
            "attempted_flushes": int(self.attempted_flushes),
            "executed_flushes": int(self.executed_flushes),
            "charged_flushes": int(self.charged_flushes),
            "invalid_flushes": int(self.invalid_flushes),
            "money": float(money),
            "episode_reward": float(self.episode_reward),
            "time": int(self.t),
        }

    # ------------------------------------------------------------------
    # helpers
    # ------------------------------------------------------------------
    def money(self, p: Optional[float] = None, tau: Optional[float] = None) -> float:
        p = self.cfg.p if p is None else p
        tau = self.cfg.tau if tau is None else tau
        return p * self.accepted_value - tau * self.charged_flushes
