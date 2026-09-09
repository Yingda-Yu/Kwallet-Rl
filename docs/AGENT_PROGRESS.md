# Agent progress (living)

## Phase 1 — reproduce environment, data, policies (STATUS: code complete, tests pass)
- [x] Workspace protected (paper/ SHAs recorded), work branch created.
- [x] Env audited: repo is DQN; paper PPO policies absent → REIMPLEMENTATION verdict.
- [x] `src/kwallet/` package: env (3k+2, flush-first, Money), 12-regime data
      port + versioned pools, JA/IFAC/SC policies, PPO/GAE trainer, rule
      references, parallel eval, stats, compute benchmark, CLI.
- [x] pytest: 33 tests pass (env timing/drops/invariants, policy factorization /
      ratio / grads / checkpoint, data hashes/namespaces, reward–Money identity).
- [x] Real T=1000 pools generated (5000 train / 300 val / 200×12 eval),
      content-hashed; regime means 47.7–53.6 (target 50).
- [x] TeX Live verified: ICASSP Template.tex compiles (pdflatex+bibtex rc=0, 3pp).
- [x] Smoke matrix (5/5 DONE): reconstructed rules FA=8826 / FWF=7640 at C=1200
      vs paper REPORTED 8592 / 7811 (within ~3–5%) — validates env+data.

## Phase 1 — training runs (STATUS: convergence pilot running)
- [~] Pilot sc_fac C=1200 s123 3000ep running; val curve decides budget.
- [ ] Main matrix 3 learned × 4 C × 10 seeds (rules eval-only).
- [ ] k-scaling (C=1200, k∈{3,6,12,24}, H=128, seeds 123/323/532).
- [ ] Per-regime Fig5, tau post-hoc (1/5/10/20), zero-settle ablation, bench.

## Phase 2 — improvements (NOT STARTED — code being prepped)
- [ ] Strong rules: rotation bound, best-fit+threshold (val-selected), acceptance
      upper bound.
- [ ] Mechanism ablations (no condition, shuffled condition, reverse condition,
      param/depth-matched IFAC), money-aligned reward.
- [ ] Set-encoder wallet-permutation-equivariant policy + equivariance tests.
- [ ] Streaming/OOD regime switching + tail extrapolation.

## Phase 3 — paper (NOT STARTED)
- [ ] Evidence-driven outline; 4-page English ICASSP paper; auto tables/figures;
      latexmk clean build; per-page render check; reproducible artifact export.
