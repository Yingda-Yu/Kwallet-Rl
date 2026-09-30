"""Data generation: shapes, hashing, namespace separation, regime structure."""
import numpy as np

from kwallet.data.pools import build_pools, sha256_array
from kwallet.data.regimes import REGIME_ORDER


def _build(tmp_path, base_seed=532, train=24, val=12, ev=6, T=200):
    return build_pools(episode_length=T, train_episodes=train,
                       val_episodes=val, eval_per_regime=ev,
                       base_seed=base_seed, calibration_sample_size=20000,
                       cache_dir=tmp_path)


def test_pool_shapes_and_regimes(tmp_path):
    b = _build(tmp_path)
    assert len(REGIME_ORDER) == 12
    assert b.train.shape == (24, 200)
    assert b.val.shape == (12, 200)
    assert len(b.eval_pools) == 12
    assert b.eval_all().shape[0] == 12 * 6
    for r in REGIME_ORDER:
        assert b.eval_pools[r].shape == (6, 200)
        assert np.all(np.isfinite(b.eval_pools[r]))
        assert (b.eval_pools[r] > 0).all()


def test_manifest_hashes_present(tmp_path):
    b = _build(tmp_path)
    h = b.manifest["hashes"]
    assert h["train"] == sha256_array(b.train)
    for r in REGIME_ORDER:
        assert f"eval_{r}" in h
        assert h[f"eval_{r}"] == sha256_array(b.eval_pools[r])


def test_train_eval_no_exact_overlap(tmp_path):
    b = _build(tmp_path)
    train_rows = {row.tobytes() for row in b.train}
    for r in REGIME_ORDER:
        for row in b.eval_pools[r]:
            assert row.tobytes() not in train_rows


def test_seed_namespace_separation(tmp_path):
    b1 = _build(tmp_path / "a", base_seed=532)
    b2 = _build(tmp_path / "b", base_seed=533)
    assert sha256_array(b1.train) != sha256_array(b2.train)
    assert not np.array_equal(b1.train, b2.train)


def test_calibrated_means_in_range(tmp_path):
    b = _build(tmp_path, ev=12)
    allv = b.eval_all().reshape(-1)
    # raw mean targeted at 50 via calibration; bursts/caps shift modestly
    assert 25.0 < float(allv.mean()) < 80.0
    assert float(allv.min()) > 0.0


def test_deterministic_rebuild(tmp_path):
    b1 = _build(tmp_path / "x")
    h1 = b1.manifest["hashes"]["train"]
    b2 = build_pools(episode_length=200, train_episodes=24, val_episodes=12,
                     eval_per_regime=6, base_seed=532,
                     calibration_sample_size=20000, cache_dir=tmp_path / "x")
    assert b2.manifest["hashes"]["train"] == h1
