"""Strong rule baselines for Phase 2 (kept separate from Phase-1 references).

These are stronger, explicitly documented heuristic controllers used to test
whether learning is actually needed. All operate through the SAME environment
action interface (a_settle, a_flush), flush at most one wallet per step.
"""
from __future__ import annotations

import numpy as np

from .rules import _usable_indices


def rotate_settle_action(env):
    """Pure round-robin settlement (no learned routing): always try the wallet
    at the rotating cursor; flush it (replenish) only if it cannot fit."""
    tx = env._current_tx
    idx = getattr(env, "_fwf_idx", 0)
    if tx > env.wallet_size:
        return env.k, env.k
    usable = _usable_indices(env)
    if not usable:
        return env.k, env.k
    target = None
    for s in range(env.k):
        j = (idx + s) % env.k
        if env.cooldown[j] == 0:
            target = j
            break
    if target is None:
        return env.k, env.k
    if env.balance[target] + 1e-9 >= tx:
        env._fwf_idx = (target + 1) % env.k
        return target, env.k
    env._fwf_idx = (target + 1) % env.k
    return env.k, target  # replenish this wallet; drop


def bestfit_threshold_action(thresh_frac: float):
    """Best-fit settlement + REACTIVE flush only when capacity is exhausted
    below a threshold. Flush the most-depleted usable wallet only when NO usable
    wallet can fit the current (non-oversize) tx. thresh_frac is unused for the
    flush trigger (fully reactive) but kept to match the threshold API; the
    threshold variant (proactive) is `bestfit_proactive`.
    """
    def action(env):
        tx = env._current_tx
        if tx > env.wallet_size:
            return env.k, env.k
        usable = _usable_indices(env)
        if not usable:
            return env.k, env.k
        fits = [i for i in usable if env.balance[i] + 1e-9 >= tx]
        if fits:
            target = min(fits, key=lambda i: env.balance[i])
            return target, env.k
        flush_target = min(usable, key=lambda i: env.balance[i])
        return env.k, flush_target
    return action


def bestfit_proactive_action(thresh_frac: float):
    """Best-fit settlement; settle normally, AND proactively flush the
    most-depleted usable wallet (other than the settle wallet) when its
    remaining balance is below thresh_frac * wallet_size. The threshold is the
    single tuning parameter and is selected on validation only.
    """
    def action(env):
        tx = env._current_tx
        if tx > env.wallet_size:
            return env.k, env.k
        usable = _usable_indices(env)
        if not usable:
            return env.k, env.k
        a_settle = env.k
        fits = [i for i in usable if env.balance[i] + 1e-9 >= tx]
        if fits:
            a_settle = min(fits, key=lambda i: env.balance[i])
        # proactive flush candidate: most-depleted usable, not the settle wallet
        cand = [i for i in usable if i != a_settle]
        if cand:
            ft = min(cand, key=lambda i: env.balance[i])
            if env.balance[ft] < thresh_frac * env.wallet_size:
                return a_settle, ft
        if a_settle == env.k:
            # nothing fits and nothing below threshold flushed: flush most-depleted
            ft = min(usable, key=lambda i: env.balance[i])
            return env.k, ft
        return a_settle, env.k
    return action


def oracle_feasible_value(env, tx_stream):
    """Loose acceptance upper bound: total value of all transactions that are
    individually feasible (tx <= wallet_size), i.e. ignoring all capacity /
    flush-coupling constraints. Not a policy; used to contextualize headroom.
    """
    return float(np.sum(tx_stream[tx_stream <= env.wallet_size]))


STRONG_RULES = {
    "ROT": rotate_settle_action,
    "BFT_REACTIVE": bestfit_threshold_action(0.0),
}

