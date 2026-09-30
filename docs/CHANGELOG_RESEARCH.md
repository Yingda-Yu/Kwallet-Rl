# Research changelog (what was actually run, with evidence)

## 2026-09-09
- Built + ported `src/kwallet/` (env, data, policies, PPO, rules, eval, stats,
  bench, CLI). 33 pytest tests PASS.
- Generated paper-protocol pools T=1000: 5000 train / 300 val / 12×200 eval,
  content-hashed; per-regime mean 47.7–53.6 (calibration target 50).
- Compiled official ICASSP Template.tex (pdflatex+bibtex rc=0, 3pp).
- Smoke matrix (`exp=matrix_smoke`, 5/5 DONE): deterministic test-pool Money at
  C=1200 for reconstructed rule references:
  - FA=8826 (paper REPORTED 8591.65), FWF=7640 (paper 7810.86). Close match →
    environment + 12-regime data faithful.
  - learned methods after only 64 training eps are near-random (expected).
- Strong-rule diagnostic (Phase-2 preview, test pool, C=1200; thresholds to be
  VALIDATION-selected later): best-fit+threshold flush rule reaches
  Money≈15327 (accept≈20724, flush≈540) at threshold 0.5 — ABOVE the paper's
  reported SC-FAC 14687.65. Implication: the paper's rule baseline (native
  multi-flush) is weak; a tuned frugal rule is competitive. Novelty/framing
  impact recorded in `docs/NOVELTY_AND_OVERLAP.md`.
- PPO convergence pilots (sc_fac C=1200 seed 123, T=1000, H=256 E=32):
  - A: entropy .02→.001, no flush-no-op bias. Stochastic train Money≈14k by
    ep~2.3k; deterministic test eval pending.
  - B: entropy .005→.0003 (control).
  - C: entropy .01→.0005 + flush-no-op init bias 2.0 (frugal prior); flush
    count lower at matched episodes.
- Training note: flush head has k flush actions vs ONE no-op; uniform init
  starts flushing ~k/(k+1). Added optional `noop_bias` conservative prior
  (chosen on validation, does not alter architecture/reward).
- Evidence labels: rule match = `CHECKPOINT_REEVALUATED/REIMPLEMENTED`
  consistent; paper Table II values remain `REPORTED_ONLY`.
