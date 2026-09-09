"""Constrained one-flush rule reference policies.

The paper reports FlushAll (FA) and FlushWhenFull (FWF) as *deterministic,
eval-only* references under the shared one-settlement/one-flush K-Wallet
interface. The native policies in Almashaqbeh et al. [1] are multi-flush
online rules and the paper does not give their exact constrained one-flush
algorithm, so these are **reconstructed reference rules** (not claimed to be an
exact reproduction of [1]). They share the same environment and Money metric as
the learned policies.

Provenance: the FWF round-robin logic mirrors
``src/idea2/fwf_regime_difficulty_eval_fixed.py`` (a one-flush rotating rule);
FA adds best-fit wallet routing. The stronger rotation / best-fit+threshold
rules used in the improvement phase live in ``rules_strong.py``.

Rules receive the environment and read its public state (balances, cooldown,
current transaction). They return ``(a_settle, a_flush)`` with each value in
0..k (k = no-op).
"""
from __future__ import annotations

import numpy as np


def _usable_indices(env):
    return [i for i in range(env.k) if env.cooldown[i] == 0]


def fwf_action(env):
    """FlushWhenFull (round-robin, reactive): maintain a rotating pointer.

    Try the next usable wallet: settle there if it fits; otherwise flush that
    wallet (replenish it) and advance the pointer; the transaction is dropped.
    Never flushes proactively.
    """
    tx = env._current_tx
    idx = getattr(env, "_fwf_idx", 0)
    if tx > env.wallet_size:
        return env.k, env.k  # oversize: nothing can help

    usable = _usable_indices(env)
    if not usable:
        return env.k, env.k  # whole system cooling: drop

    # next usable wallet rotating from idx
    target = None
    for s in range(env.k):
        j = (idx + s) % env.k
        if env.cooldown[j] == 0:
            target = j
            break
    if target is None:
        return env.k, env.k

    if env.balance[target] + 1e-9 >= tx:
        env._fwf_idx = target
        return target, env.k  # settle, no flush
    # target wallet cannot fit -> flush it (replenish), drop tx
    env._fwf_idx = (target + 1) % env.k
    return env.k, target  # no settle; flush target


def fa_action(env):
    """FlushAll reference (best-fit routing, reactive flush):

    Settle using best-fit (the usable wallet with the *smallest* balance that
    still covers the tx, conserving larger-balance wallets). If no usable
    wallet can fit, flush the usable wallet with the smallest remaining balance
    to replenish it for future requests, and drop the current transaction.
    """
    tx = env._current_tx
    if tx > env.wallet_size:
        return env.k, env.k

    usable = _usable_indices(env)
    if not usable:
        return env.k, env.k

    fits = [i for i in usable if env.balance[i] + 1e-9 >= tx]
    if fits:
        # best-fit: smallest remaining balance that still covers tx
        target = min(fits, key=lambda i: env.balance[i])
        return target, env.k
    # no usable wallet can fit -> flush most-depleted usable wallet, drop tx
    flush_target = min(usable, key=lambda i: env.balance[i])
    return env.k, flush_target


RULE_POLICIES = {"FA": fa_action, "FWF": fwf_action}
