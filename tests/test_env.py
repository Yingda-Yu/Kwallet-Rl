"""Environment mechanics, timing and accounting invariants for KWalletEnv."""
import numpy as np
import pytest

from kwallet.envs.kwallet import EnvConfig, KWalletEnv, NONE


def make_env(k=6, C=300.0, F=3, T=20, reward_mode="original"):
    return KWalletEnv(EnvConfig(C=C, k=k, F=F, T=T, reward_mode=reward_mode))


def const_stream(T, x):
    return np.full(T, float(x))


def test_init_state():
    env = make_env()
    obs = env.reset(tx_stream=const_stream(20, 10.0))
    assert obs.shape[0] == 3 * 6 + 2
    assert np.allclose(env.balance, env.wallet_size)
    assert np.all(env.cooldown == 0)
    # wallet size = C/k
    assert env.wallet_size == pytest.approx(50.0)


def test_normal_settle():
    env = make_env()
    env.reset(tx_stream=const_stream(20, 10.0))
    obs, r, done, info = env.step(0, env.k)  # settle wallet 0
    assert info["accepted"] is True
    assert info["settled_wallet"] == 0
    assert env.balance[0] == pytest.approx(env.wallet_size - 10.0)
    assert info["accepted_value"] == pytest.approx(10.0)
    assert r == pytest.approx(10.0 / 1000.0)
    assert info["charged_flushes"] == 0


def test_exact_balance_settle():
    env = make_env()
    env.reset(tx_stream=const_stream(20, env.wallet_size))
    _, r, _, info = env.step(2, env.k)
    assert info["accepted"] is True
    assert env.balance[2] == pytest.approx(0.0, abs=1e-6)
    assert r == pytest.approx(env.wallet_size / 1000.0)


def test_insufficient_drop():
    env = make_env()
    env.reset(tx_stream=const_stream(20, 10.0))
    env.balance[0] = 5.0  # drain below tx
    _, r, _, info = env.step(0, env.k)
    assert info["accepted"] is False
    assert info["drop_reason"] == "insufficient"
    assert info["drop_reasons"]["insufficient"] == 1
    assert r == pytest.approx(-0.02)


def test_noop_settle_drops_active_none():
    env = make_env()
    env.reset(tx_stream=const_stream(20, 10.0))
    _, r, _, info = env.step(env.k, env.k)
    assert info["accepted"] is False
    assert info["drop_reason"] == "active_none"
    assert r == pytest.approx(-0.02)


def test_same_wallet_conflict():
    """Flush and settle the same wallet: flush executes (charged), settle drops
    with same_wallet_conflict (freshly-flushed wallet unavailable)."""
    env = make_env()
    env.reset(tx_stream=const_stream(20, 10.0))
    _, r, _, info = env.step(0, 0)
    assert info["flushed_wallet"] == 0
    assert info["charged_flushes"] == 1
    assert info["accepted"] is False
    assert info["drop_reason"] == "same_wallet_conflict"
    # flush penalty applied, plus drop penalty
    assert r == pytest.approx(-0.01 - 0.02, abs=1e-9)
    # flushed wallet emptied and frozen
    assert env.balance[0] == pytest.approx(0.0)
    assert env.cooldown[0] == env.F - 1  # decremented at end of flush step


def test_frozen_wallet_flush_invalid_and_settle_frozen():
    env = make_env(F=3)
    env.reset(tx_stream=const_stream(20, 10.0))
    env.step(env.k, 1)  # flush wallet 1 (charged)
    assert env.cooldown[1] == env.F - 1
    # next step: try to flush the still-frozen wallet 1 -> invalid, not charged
    _, _, _, info = env.step(env.k, 1)
    assert info["invalid_flushes"] == 1
    assert info["charged_flushes"] == 1
    # trying to settle a frozen (different) wallet -> frozen drop
    _, _, _, info2 = env.step(1, env.k)
    assert info2["drop_reason"] == "frozen"


def test_oversize_drop():
    env = make_env()
    big = env.wallet_size + 1.0
    env.reset(tx_stream=const_stream(20, big))
    _, _, _, info = env.step(0, env.k)
    assert info["drop_reason"] == "oversize"
    assert info["accepted"] is False


def test_refill_on_expiry():
    env = make_env(F=3)
    env.reset(tx_stream=const_stream(20, 10.0))
    env.step(env.k, 0)  # flush 0 at step t=0; cooldown 3->2 at end
    assert env.cooldown[0] == 2 and env.balance[0] == 0.0
    # steps t=1, t=2: still frozen
    env.step(env.k, env.k)
    assert env.cooldown[0] == 1 and env.balance[0] == 0.0
    env.step(env.k, env.k)
    # end of t=2: cooldown 1->0 -> refill to full
    assert env.cooldown[0] == 0 and env.balance[0] == pytest.approx(env.wallet_size)


def test_terminal_and_step_count():
    env = make_env(T=10)
    env.reset(tx_stream=const_stream(10, 5.0))
    done = False
    steps = 0
    while not done:
        _, _, done, _ = env.step(env.k, env.k)
        steps += 1
    assert steps == 10


def test_determinism_fixed_stream():
    def rollout():
        env = make_env(T=15, k=4, C=200.0)
        env.reset(tx_stream=np.arange(1, 16, dtype=float) % 30 + 5)
        outs = []
        rng = np.random.default_rng(0)
        done = False
        while not done:
            a_s = int(rng.integers(0, env.k + 1))
            a_f = int(rng.integers(0, env.k + 1))
            _, r, done, info = env.step(a_s, a_f)
            outs.append((round(r, 6), info["accepted"], info["drop_reason"]))
        return outs, info["money"]
    o1, m1 = rollout()
    o2, m2 = rollout()
    assert o1 == o2 and m1 == m2


def test_invariants_full_episode():
    env = make_env(T=50, k=8, C=400.0, F=2)
    env.reset(tx_stream=np.linspace(5, 60, 50))
    rng = np.random.default_rng(7)
    done = False
    while not done:
        a_s = int(rng.integers(0, env.k + 1))
        a_f = int(rng.integers(0, env.k + 1))
        _, _, done, info = env.step(a_s, a_f)
    # every step is exactly one accepted or dropped tx
    assert info["accepted_count"] + info["drop_count"] == 50
    assert sum(info["drop_reasons"].values()) == info["drop_count"]
    # balances within bounds
    assert np.all(env.balance >= -1e-9)
    assert np.all(env.balance <= env.wallet_size + 1e-9)


def test_reward_money_identity():
    """original reward (shaping off): reward = accepted/1000 - .01*flush - .02*drop.
    Money/1000 = accepted/1000 - .01*flush  =>  reward = Money/1000 - .02*drop."""
    env = make_env(T=40, k=5, C=250.0, F=3)
    env.reset(tx_stream=np.linspace(2, 55, 40))
    rng = np.random.default_rng(3)
    done = False
    while not done:
        a_s = int(rng.integers(0, env.k + 1))
        a_f = int(rng.integers(0, env.k + 1))
        _, _, done, info = env.step(a_s, a_f)
    expected = info["money"] / 1000.0 - 0.02 * info["drop_count"]
    assert info["episode_reward"] == pytest.approx(expected, abs=1e-6)


def test_config_validation():
    with pytest.raises(ValueError):
        KWalletEnv(EnvConfig(k=0, C=100.0))
    with pytest.raises(ValueError):
        KWalletEnv(EnvConfig(k=4, C=0.0))
    with pytest.raises(ValueError):
        KWalletEnv(EnvConfig(k=4, C=100.0, F=-1))


def test_masks_advisory():
    env = make_env()
    env.reset(tx_stream=const_stream(20, env.wallet_size + 5))  # oversize
    sm, fm = env.feasibility_masks()
    # oversize: no wallet feasible for settle except no-op
    assert sm[env.k] and not sm[: env.k].any()
    # all usable wallets flushable
    assert fm[: env.k].all()
