"""Permutation equivariance + cross-k transfer tests for set-encoder policies."""
import numpy as np
import torch

from kwallet.policies.set_actors import build_set_policy


def _split_blocks(x, k):
    return x[:, 0:k], x[:, k:2 * k], x[:, 2 * k:3 * k], x[:, 3 * k:3 * k + 2]


def _permute_obs(x, k, perm):
    b, a, f, g = _split_blocks(x, k)
    return torch.cat([b[:, perm], a[:, perm], f[:, perm], g], dim=-1)


def _wallet_logits(pol, x):
    h, pooled, gg = pol._encode_set(x)
    s = pol._settle_logits(h, pooled, gg)
    return s, h, pooled, gg


def test_settle_permutation_equivariant():
    torch.manual_seed(0)
    k = 24
    for method in ("set_ifac", "set_sc_fac"):
        pol = build_set_policy(method, 3 * k + 2, k, hidden=64).eval()
        x = torch.randn(5, 3 * k + 2)
        perm = torch.randperm(k)
        xp = _permute_obs(x, k, perm)
        with torch.no_grad():
            s1, h1, p1, g1 = _wallet_logits(pol, x)
            s2, h2, p2, g2 = _wallet_logits(pol, xp)
        # global value invariant
        v1 = pol._value(p1, g1); v2 = pol._value(p2, g2)
        assert torch.allclose(v1, v2, atol=1e-5), method
        # pooled summary invariant
        assert torch.allclose(p1, p2, atol=1e-5), method
        # per-wallet settle logits: xp slot j holds original wallet perm[j],
        # so logit_s2[j] must equal logit_s1[perm[j]]; null logit unchanged.
        assert torch.allclose(s2[:, :k], s1[:, :k][:, perm], atol=1e-5), method
        assert torch.allclose(s2[:, k], s1[:, k], atol=1e-5), method


def test_flush_equivariant_and_conditioning():
    torch.manual_seed(1)
    k = 12
    pol = build_set_policy("set_sc_fac", 3 * k + 2, k, hidden=64).eval()
    x = torch.randn(4, 3 * k + 2)
    perm = torch.randperm(k)
    xp = _permute_obs(x, k, perm)
    with torch.no_grad():
        h1, p1, g1 = pol._encode_set(x)
        h2, p2, g2 = pol._encode_set(xp)
        # settle action chosen in ORIGINAL coords (includes null settle = k).
        a_s = torch.tensor([0, 3, k, 7])
        invperm = torch.argsort(perm)
        # same physical wallet sits at slot invperm[a_s] in the permuted obs
        idx = a_s.clamp(max=k - 1)
        a_s_xp = torch.where(a_s < k, invperm[idx], a_s)
        f1 = pol._flush_logits(h1, p1, g1, a_s)
        f2 = pol._flush_logits(h2, p2, g2, a_s_xp)
    # flush wallet logits permute the same way; no-op (index k) invariant
    assert torch.allclose(f2[:, :k], f1[:, :k][:, perm], atol=1e-5)
    assert torch.allclose(f2[:, k], f1[:, k], atol=1e-5)


def test_deterministic_action_permutes():
    torch.manual_seed(2)
    k = 24
    pol = build_set_policy("set_sc_fac", 3 * k + 2, k, hidden=64).eval()
    x = torch.randn(1, 3 * k + 2)
    perm = torch.randperm(k)
    xp = _permute_obs(x, k, perm)
    with torch.no_grad():
        o1 = pol.step(x, deterministic=True)
        o2 = pol.step(xp, deterministic=True)
    invperm = torch.argsort(perm)
    for key in ("a_settle", "a_flush"):
        a1 = int(o1[key].item()); a2 = int(o2[key].item())
        if a1 < k:
            # same physical wallet sits at slot invperm[a1] after permutation
            assert a2 == int(invperm[a1]), (key, a1, a2)
        else:
            assert a2 == k, (key, a1, a2)
    # joint log-prob invariant
    assert abs(float(o1["log_prob"].item()) - float(o2["log_prob"].item())) < 1e-5


def test_cross_k_weight_transfer():
    """Weights have no k-dependent dimension: train-shape loads at different k."""
    torch.manual_seed(3)
    pol12 = build_set_policy("set_sc_fac", 3 * 12 + 2, 12, hidden=64)
    pol24 = build_set_policy("set_sc_fac", 3 * 24 + 2, 24, hidden=64)
    sd = pol12.state_dict()
    # every parameter shape must be identical regardless of k
    for (n1, t1), (n2, t2) in zip(sd.items(), pol24.state_dict().items()):
        assert n1 == n2 and tuple(t1.shape) == tuple(t2.shape), n1
    pol24.load_state_dict(sd, strict=True)   # transfers cleanly
    # runs on k=24
    x = torch.randn(2, 3 * 24 + 2)
    with torch.no_grad():
        out = pol24.step(x, deterministic=True)
    assert out["a_settle"].shape == (2,)
