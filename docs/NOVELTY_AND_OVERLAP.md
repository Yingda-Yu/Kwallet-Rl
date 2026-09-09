# Novelty, overlap with the old manuscript, and claims we can/cannot make

Locked 2026-09-09 from REAL experiments on reconstructed code. Update only with
new evidence.

## What the old manuscript claims
- A settle-conditioned factorized PPO (SC-FAC) for streaming K-Wallet
  collateral control beats joint JA-PPO and independent IFAC in Money, and
  beats native FlushAll/FWF references (reported Table II Money at C=1200:
  FA 8592 / FWF 7811 / JA 14443 / IFAC 14473 / SC 14688).
- Reports O(k) vs O(k^2) output logits (Fig. 4).

## What we verified (REIMPLEMENTED under one controlled protocol)
- Environment + 12-regime data port reproduce the RULE references: reconstructed
  FA=8826, FWF=7640 at C=1200 vs reported 8592/7811 (close; FA/FWF are
  reconstructed, `CHECKPOINT_REEVALUATED`). This validates the simulator/data.
- Factorization vs joint (early+mid-training stochastic, deterministic TBD):
  IFAC Money clearly > JA-PPO; JA over-flushes (flush ~610-790) and learns much
  slower. Supports the structural ordering.
- Output-logit efficiency is reproduced exactly: JA emits (k+1)^2=625 logits at
  k=24; factorized methods emit 2(k+1)=50 (bench C1200). Params in
  `runs/bench/bench_C1200.0_k24.0.csv`.

## Important CORRECTIVE finding (do not hide)
- The paper compares learned policies only against NAIVE rules (FA/FWF) that
  never flush proactively. A simple deterministic "best-fit + threshold flush"
  rule (BFP0.5; threshold SELECTED ON VALIDATION, val Money=15290) reaches
  Money ~15,327 on the C=1200 test pools with **zero avoidable
  ("recoverable") drops**, i.e. it accepts every transaction that fits in any
  wallet. It is essentially optimal on stationary streams.
- Reimplemented learned policies (SC-FAC, 3000 episodes, single-seed pilots)
  reach Money ~13.2-13.5k: accept ~19.1k (vs ~20.7k ceiling) and flush ~560-600.
  They DO NOT beat the tuned rule on Money. Paper Table II learned numbers stay
  `REPORTED_ONLY`; our hyperparameters are `chosen_for_reimplementation`.
- Non-stationary (regime-switch) test: BFP0.5 keeps zero recoverable drops on
  EVERY switch direction/change-point tested (calm->burst, burst->calm, early
  and late). Because it feeds back on wallet balance — the sufficient statistic
  — a single fixed threshold is already robust to distribution shift under the
  current observation. So "learned adapts better to streaming shifts" is a
  NEGATIVE result under the paper observation; we report it honestly.

## Defensible contributions for ICASSP 2027 (all backed by runs)
1. **Settle-conditioned factorization sample-efficiency / correctness**: under
   matched params/budget, the conditional path (SC-FAC) vs independent IFAC vs
   joint JA-PPO, including MECHANISM ABLATIONS (no-condition = SC-FAC with zeroed
   settle embedding; shuffled-condition = wrong settle embedding). Tests the
   causal claim that the settle->flush path carries useful information.
2. **Permutation-equivariant set encoder (NEW)**: treat wallets as a set
   (shared per-wallet MLP + pooling + per-wallet logits). Proven equivariant to
   wallet permutation (4 tests) and, because no parameter size depends on k, its
   WEIGHTS TRANSFER ZERO-SHOT across wallet counts k. A flat MLP cannot
   (state-dict shape mismatch, demonstrated). Concrete systems benefit: train
   once at small scale, deploy at larger scale.
3. **Honest strong-baseline correction + efficiency/logit analysis** on a
   realistic streaming transaction-collateral workload (12 regimes).

## Claims we will NOT make
- We do NOT claim learned beats tuned rules on absolute Money (it does not).
- We do NOT reproduce the exact Table II learned numbers (no released policy /
  hyperparameters); those are `REPORTED_ONLY`.
- No burst PREDICTION advantage is claimed: observations exclude future arrival
  data, and balance-feedback already achieves zero recoverable drops.
- No fabricated authors / funding / ORCID / prior-submission status.

## Open (results decide)
- Does SC-FAC > IFAC > JA hold on the full multi-seed main table and across C?
- Does correct conditioning beat no-condition / shuffled-condition ablations?
- Does the set policy's zero-shot cross-k transfer retain most of matched-deploy
  Money (headline system result)?
