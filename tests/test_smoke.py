"""End-to-end smoke: rule rollouts and a tiny PPO training+eval cycle."""
import numpy as np
import torch

from kwallet.baselines.rules import RULE_POLICIES
from kwallet.envs.kwallet import EnvConfig, KWalletEnv
from kwallet.evaluation.rollout import evaluate_pool, evaluate_regimes
from kwallet.evaluation.stats import summarize, to_frame, paired_difference
from kwallet.training.ppo import PPOConfig, PPOTrainer


def tiny_cfg(T=50, k=4, C=200.0):
    return EnvConfig(C=C, k=k, F=2, T=T)


def tiny_pool(n=8, T=50, seed=1):
    rng = np.random.default_rng(seed)
    # values well under wallet_size=50 so most tx are feasible
    return rng.uniform(5, 40, size=(n, T)).astype(np.float64)


def test_rules_legal_and_run():
    cfg = tiny_cfg()
    pool = tiny_pool()
    for name, fn in RULE_POLICIES.items():
        recs = evaluate_pool(fn, pool, cfg, regime="X", kind="rule")
        assert len(recs) == pool.shape[0]
        for r in recs:
            assert np.isfinite(r["money"])
            assert r["accepted_count"] + r["drop_count"] == cfg.T
            assert r["invalid_flushes"] == 0  # rules never flush a frozen wallet
            assert r["charged_flushes"] >= 0


def test_ppo_trains_and_evaluates():
    cfg = tiny_cfg()
    pool = tiny_pool()
    pcfg = PPOConfig(seed=123, device="cpu", method="sc_fac", hidden=32,
                     embed=8, n_layers=1, total_episodes=8, rollout_episodes=4,
                     update_epochs=2, minibatch_size=64)
    trainer = PPOTrainer(pcfg, cfg, pool)
    res = trainer.train(verbose=False)
    assert len(res["history"]) == 2
    assert all(np.isfinite(h["value_loss"]) for h in res["history"])
    # evaluate the trained policy deterministically
    recs = evaluate_pool(trainer.policy, pool, cfg, regime="X", kind="learned")
    df = to_frame(recs)
    assert len(df) == pool.shape[0]
    assert np.isfinite(df["money"]).all()
    summ = summarize(df)
    assert "ALL" in set(summ["group"])


def test_paired_difference_self_zero():
    cfg = tiny_cfg()
    pool = tiny_pool()
    recs = evaluate_pool(RULE_POLICIES["FA"], pool, cfg, regime="X", kind="rule")
    df = to_frame(recs)
    pd = paired_difference(df, df, key="money")
    assert abs(pd["mean_diff"]) < 1e-9
