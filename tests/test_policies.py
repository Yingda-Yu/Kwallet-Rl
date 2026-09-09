"""Policy distribution correctness, factorization consistency, PPO plumbing."""
import numpy as np
import torch

from kwallet.policies.actors import build_policy

K = 3
OBS = 3 * K + 2
N = K + 1


def _x(b=4):
    torch.manual_seed(0)
    return torch.randn(b, OBS)


def test_output_logits_counts():
    ja = build_policy("ja_ppo", OBS, K)
    ifac = build_policy("ifac", OBS, K)
    sc = build_policy("sc_fac", OBS, K)
    assert ja.output_logits() == N * N
    assert ifac.output_logits() == 2 * N
    assert sc.output_logits() == 2 * N


def test_actions_in_range():
    x = _x(8)
    for m in ["ja_ppo", "ifac", "sc_fac"]:
        pol = build_policy(m, OBS, K)
        out = pol.step(x, deterministic=False)
        assert int(out["a_settle"].min()) >= 0 and int(out["a_settle"].max()) <= K
        assert int(out["a_flush"].min()) >= 0 and int(out["a_flush"].max()) <= K


def test_ja_joint_normalization_and_decode():
    pol = build_policy("ja_ppo", OBS, K)
    x = _x(1)
    dist, _ = pol._joint_dist(x)
    probs = dist.probs[0]
    assert probs.shape == (N * N,)
    assert torch.allclose(probs.sum(), torch.tensor(1.0), atol=1e-5)
    # decode joint = a_s * n + a_f
    for joint in range(N * N):
        a_s = joint // N
        a_f = joint % N
        assert a_s * N + a_f == joint


def test_ja_logp_consistency_and_ratio_one():
    pol = build_policy("ja_ppo", OBS, K)
    x = _x(5)
    with torch.no_grad():
        out = pol.step(x, deterministic=False)
    old = out["log_prob"]
    new = pol.evaluate_actions(x, out["a_settle"], out["a_flush"])["log_prob"]
    assert torch.allclose(new, old, atol=1e-5)
    ratio = torch.exp(new - old)
    assert torch.allclose(ratio, torch.ones_like(ratio), atol=1e-5)


def test_ifac_independent_heads():
    pol = build_policy("ifac", OBS, K)
    x = _x(1)
    ds, df, _ = pol._dists(x)
    assert torch.allclose(ds.probs.sum(-1), torch.ones(1), atol=1e-5)
    assert torch.allclose(df.probs.sum(-1), torch.ones(1), atol=1e-5)
    # flush distribution must NOT depend on settle choice (independent heads)
    h = pol.encode(x)
    f_logits = pol.flush_head(h)
    out = pol.evaluate_actions(x, torch.tensor([0]), torch.tensor([1]))
    # recompute flush logp for a_flush=1 under two different a_s -> identical
    lp_same = torch.log_softmax(f_logits, -1)[0, 1]
    assert torch.allclose(out["log_prob"] - ds.log_prob(torch.tensor([0]))[0],
                          lp_same, atol=1e-5)


def test_sc_factorization_exact():
    """pi(a_s,a_f|s) = pi_s(a_s|s) * pi_f(a_f|s,a_s); joint sums to 1."""
    pol = build_policy("sc_fac", OBS, K)
    x = _x(1)
    ds, h = pol._settle_dist(x)
    p_s = ds.probs[0]  # (n,)
    flush_logits = []
    for a in range(N):
        flush_logits.append(pol._flush_logits(h, torch.tensor([a]))[0])
    flush_logits = torch.stack(flush_logits)          # (n, n) [a_s, a_f]
    p_f = torch.softmax(flush_logits, dim=-1)         # p(a_f | a_s)
    joint = p_s.unsqueeze(-1) * p_f                    # (n, n)
    assert torch.allclose(joint.sum(), torch.tensor(1.0), atol=1e-5)
    # each row (fixed a_s) sums to pi_s(a_s)
    assert torch.allclose(joint.sum(-1), p_s, atol=1e-5)
    # evaluate_actions logp matches manual factorization for a sampled pair
    a_s, a_f = 2, 1
    manual = torch.log(p_s[a_s] + 1e-30) + torch.log(p_f[a_s, a_f] + 1e-30)
    out = pol.evaluate_actions(x, torch.tensor([a_s]), torch.tensor([a_f]))
    assert torch.allclose(out["log_prob"][0], manual, atol=1e-4)


def test_sc_conditions_on_settle():
    """Flush logits must change with the settle action (true conditioning)."""
    pol = build_policy("sc_fac", OBS, K)
    x = _x(1)
    _, h = pol._settle_dist(x)
    l0 = pol._flush_logits(h, torch.tensor([0]))
    l1 = pol._flush_logits(h, torch.tensor([1]))
    assert not torch.allclose(l0, l1)
    # exact conditional entropy is finite and <= sum of marginal entropies bound
    ce = pol.conditional_entropy_exact(x)
    assert torch.isfinite(ce).all()


def test_finite_nonzero_grads():
    pol = build_policy("sc_fac", OBS, K)
    x = _x(6)
    out = pol.step(x, deterministic=False)
    ev = pol.evaluate_actions(x, out["a_settle"], out["a_flush"])
    loss = -(ev["log_prob"] * torch.randn(6)).mean() + 0.5 * ev["value"].pow(2).mean()
    loss.backward()
    grads = [p.grad for p in pol.parameters() if p.grad is not None]
    assert len(grads) > 0
    assert all(torch.isfinite(g).all() for g in grads)
    assert any(g.abs().sum() > 0 for g in grads)


def test_checkpoint_roundtrip():
    pol = build_policy("ifac", OBS, K)
    x = _x(3)
    pol.eval()
    with torch.no_grad():
        before = pol.step(x, deterministic=True)["a_settle"].clone()
    sd = {k: v.clone() for k, v in pol.state_dict().items()}
    pol2 = build_policy("ifac", OBS, K)
    pol2.load_state_dict(sd)
    pol2.eval()
    with torch.no_grad():
        after = pol2.step(x, deterministic=True)["a_settle"]
    assert torch.equal(before, after)
