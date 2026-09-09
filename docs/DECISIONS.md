# Decisions log (append-only, dated)

Evidence labels used across docs:
`REPORTED_ONLY` (paper states, not regenerated) · `ARTIFACT_REGENERATED` ·
`CHECKPOINT_REEVALUATED` · `TRAINING_REPRODUCED` · `REIMPLEMENTED` ·
`CORRECTED_PROTOCOL` · `NEW_EXPERIMENT` · `MISSING_*` (not recoverable).

## 2026-09-09 — Stage 1 provenance verdict
- The repo's committed RL code is **DQN-era** (joint `(k+1)^2` action decoded
  as settle = joint // (k+1), flush = joint % (k+1)). `notes/idea3/code_protocol.md`
  explicitly states "不做 PPO". The paper's **JA-PPO / IFAC / SC-FAC PPO
  policies and PPO hyperparameters do not exist anywhere in the repo**.
  => Stage 1 is a well-grounded **REIMPLEMENTATION**, not a numerical
  reproduction of trained policies. Environment semantics and the 12-regime
  generator ARE traceable and ported faithfully; the three policies and their
  training configuration are reconstructed from the paper description.
  Label: env+data `REIMPLEMENTED (faithful port)`; learned policies
  `REIMPLEMENTED`; paper Table II numbers stay `REPORTED_ONLY`.

## 2026-09-09 — Data generator ported from real source
- `src/kwallet/data/regimes.py` is a direct port of
  `src/ideaextra/kwallet_ideaextra_generator.py`:
  `REGIME_ORDER=[US,TLS,LNS,TLNS,TPLS,PLS, UB,TLB,LNB,TLNB,TPLB,PLB]`,
  base_seed 532, episode_length 1000, static eval 200/regime,
  MIX12 train 5000 / val 300, seed offsets train 0 / eval 1,000,000 /
  val 2,000,000, per-regime cursor step 100,000, shuffle rng base_seed+999,999.
  Bursts: start_prob .035, length Poisson(6), multiplier 1.40; calibration via
  raw-mean scaling to target 50 (fixed seed 1234567, 200k samples).

## 2026-09-09 — Constrained one-flush FA/FWF are reconstructed references
- Native policies in Almashaqbeh et al. [1] (`legacy/old_code/FA.py`) are
  **multi-flush** (flush ALL wallets). The repo's one-flush rule
  (`src/idea2/fwf_regime_difficulty_eval_fixed.py`) is a round-robin reactive
  rule. The paper does not specify the exact constrained one-flush FA/FWF
  algorithm => label `MISSING_RULE_DEFINITION`; we implement documented
  constrained one-flush references (`src/kwallet/baselines/rules.py`):
  FWF = round-robin next-usable, flush that wallet when it cannot fit (mirrors
  the repo rule); FA = best-fit routing, flush most-depleted usable wallet when
  none can fit. Stronger rules (rotation bound, best-fit+threshold) are built
  in Phase 2 and NOT conflated with these references.

## 2026-09-09 — Locked paper protocol facts (from PDF)
- k=24, C in {800,900,1000,1200}, F=3, T=1000; 10 seeds
  {123,323,532,777,999,2027,3407,4501,6101,8888}.
- State 3k+2 = 74: balances /(C/k), availability u (1=usable), cooldown /F,
  x/max_tx, t/T. Actions a_s,a_f in {1..k, empty}; flush executes FIRST then
  settle; flushed wallet emptied, unavailable current + F-1 decisions, refills
  to full when timer expires.
- Acceptance: settle != empty, flush != settle, u[a_s]=1, balance >= x.
  x > C/k oversize drop. Reward (original): +x/1000 accept, -0.02 drop,
  -0.01 charged flush, shaping OFF. Money = p*accepted_value - tau*charged,
  p=1, tau=10. SC-FAC E=32 H=256 main; k-scaling (C=1200, k in {3,6,12,24})
  uses E=32 H=128, seeds 123/323/532.
- Policy logits: JA (k+1)^2=625; IFAC/SC 2(k+1)=50 at k=24.

## 2026-09-09 — Hyperparameters not given by paper (chosen_for_reimplementation)
- PPO/training budget, lr, clip, epochs, minibatch, rollout, entropy schedule
  are NOT in the paper. We use a standard clipped PPO with GAE (gamma .99,
  lambda .95, lr 3e-4, clip .2, value .5, entropy 0.02->0.001, 10 epochs,
  minibatch 512, rollout 8 episodes, grad clip 1.0) informed loosely by
  `legacy/old_code/PRO_RL.py` (a Bernoulli-PPO prototype). Budget is decided
  by a val-convergence pilot, never tuned on test. Marked
  `source: chosen_for_reimplementation`.

## 2026-09-09 — Time feature convention
- t/T uses 1-based progress (decision index t' in 0..T-1 presented as
  (t'+1)/T, so the final decision = 1.0). Documented and unit-tested.

## 2026-09-10 — Strong-baseline correction (NEW_EXPERIMENT, validation-selected)
- Rule threshold sweep on VALIDATION only (300 ep): proactive best-fit
  BFP0.5 best (val Money 15290 +/- 135); reactive BFT* degenerates to FA.
  Threshold 0.5 chosen on val, frozen, then evaluated once on test.
- C=1200 deterministic TEST Money: FA 8826 (recoverable drops 255),
  FWF 7640 (286), BFP0.5 **15327 with recoverable drops = 0** (accept 20724,
  i.e. essentially every transaction that fits in any wallet). A single
  balance-feedback threshold is near-optimal on stationary i.i.d. streams.
- Consequence: the old manuscript compares learned policies only against
  naive rules that never flush proactively. We add BFP0.5 as the honest strong
  baseline and do NOT claim RL beats tuned rules on absolute Money.

## 2026-09-10 — Three-way ordering + mechanistic staircase (REIMPLEMENTED)
- Deterministic C=1200 test, seed 123, 3000-episode PPO, identical protocol:
  JA-PPO Money 11604 (accept 16654, flush 505, drops 512 -> ~112 recoverable),
  IFAC 13118 (accept 17960, flush 484, drops 474 -> ~74 recoverable),
  SC-FAC 13210 (accept 19172, flush 596, drops 442 -> ~42 recoverable),
  BFP0.5 15327 (accept 20724 = feasible ceiling, recoverable drops 0).
  (Structural oversize floor = 400.3 drops/episode for all policies.)
- Accepted value rises monotonically JA->IFAC->SC->ceiling and recoverable
  drops fall 112->74->42->0: each structural change closes the gap to the
  feasible ceiling. Settle-conditioning recovers ~+1.2k accepted value vs IFAC
  at the cost of ~+112 flushes; at tau=10 Money is within noise (13210 vs
  13118) but the acceptance / recoverable-drop gap is consistent, and grows
  at lower flush price (tau=1: SC 18576 vs IFAC 17476).
- Ordering claim: factorized (IFAC/SC) clearly beats joint (JA) in Money and
  sample efficiency; SC vs IFAC advantage is primarily acceptance/recovery,
  not raw Money at the paper's tau. Multi-seed matrix_main confirms stats.

## 2026-09-10 — Streaming/OOD is a NEGATIVE result for the "RL adapts" hypothesis
- Regime-switch streams (calm<->burst, early/late change points), n=200:
  BFP0.5 keeps post-switch recoverable drops = 0.0 on EVERY direction/timing;
  FA/FWF accumulate 59-189. Because balance is a sufficient statistic, a fixed
  feedback threshold already absorbs distribution shift under the paper
  observation. Persisted in runs/switching/switch_summary.csv.
- We therefore do NOT claim learned policies adapt better to OOD shifts.
  Phase-2 novelty rests on: (1) settle-conditioned factorization (mechanism +
  acceptance), (2) permutation-equivariant set ENCODER with zero-shot
  cross-k transfer (mechanically verified; weights independent of k),
  (3) the strong-baseline/efficiency correction.

## 2026-09-10 — Efficiency / output-logit scaling (ARTIFACT_REGENERATED)
- bench C1200 k24: JA 245,874 params / 625 logits; IFAC 98,099 / 50;
  SC-FAC & ablations 172,883 / 50; Set-IFAC 135,437 / 50; Set-SC-FAC
  135,949 / 50. Set-policy params are independent of k (cross-k transferable);
  flat policy params change with k and cannot transfer. Per-step latency
  0.4-1.1 ms CPU. runs/bench/bench_C1200.0_k24.csv.

## 2026-09-10 — GPU authorized & verified, but measured unsuitable (CORRECTED)
- User authorized GPU. Isolated `kwallet-gpu` env (torch 2.3.1+cu121) built;
  CUDA verified on free GPU1 (real matmul + real cuda training/checkpoint).
- Head-to-head identical config: PPO cycle ~10 s CPU vs ~19 s CUDA (GPU util
  ~14%). Workload is batch-1 sequential rollout + CPU numpy env; GPU launch/
  transfer overhead makes it ~2x slower. DECISION: keep all training on CPU;
  report GPU as verified-but-not-beneficial for this architecture. Added a
  --device flag to run_experiments.py (train device; eval stays on CPU) for
  completeness/future vectorized rollout.
