# Reproduction report — K-Wallet streaming collateral control

Scope: assess and (where possible) regenerate the claims of the prior
manuscript "Settle-Conditioned Policy Learning for Streaming Transaction
Collateral Control" (`paper/old paper.pdf`). Evidence labels:
`REPORTED_ONLY` (paper states; not regenerated), `REIMPLEMENTED` (we rebuilt
from the paper description), `PORT` (faithful port of traced source),
`ARTIFACT_REGENERATED` / `TRAINING_REPRODUCED` (our code produces it),
`CORRECTED_PROTOCOL`, `NEW_EXPERIMENT`, `MISSING_*`.

## 1. Provenance verdict
- The committed repository RL code is **DQN-era** and `notes/idea3/code_protocol.md`
  explicitly says "不做 PPO". The paper's JA-PPO / IFAC / SC-FAC policies and
  their PPO hyperparameters **do not exist** anywhere in the repo or git history
  (bounded search over `src/`, `legacy/`, `notes/`, git log).
- Therefore: environment semantics + 12-regime generator = faithful **PORT**
  (see §2); the three learned policies + training config = **REIMPLEMENTED**;
  the paper's learned Table~II numbers remain **REPORTED_ONLY**.

## 2. What IS traceable and was faithfully ported (`PORT`)
- 12-regime generator: ported from `src/ideaextra/kwallet_ideaextra_generator.py`.
  REGIME_ORDER, base_seed 532, T=1000, train 5000 / val 300 / eval 200 per
  regime, burst calibration (start .035, length Poisson(6), mult 1.40;
  raw-mean scaling to target 50, seed 1234567). `src/kwallet/data/regimes.py`,
  `data/pools.py`. Pools are cached and hash-checked; no train/test leakage
  (seed offsets 0 / 1e6 / 2e6).
- Environment: k=24 wallets, C in {800,900,1000,1200}, F=3 cooldown, flush-first
  then settle, refill-to-full, oversize/active_none/frozen/conflict/insufficient
  drop reasons, observation 3k+2. `src/kwallet/envs/kwallet.py`, covered by 13
  unit tests.

## 3. Rule references (`REIMPLEMENTED`, partially reconstructed)
- The reference K-Wallet policies in [Almashaqbeh et al. style] are MULTI-flush
  (FlushAll). The exact constrained one-flush FA/FWF algorithm is
  `MISSING_RULE_DEFINITION`; we implement documented one-flush versions
  (`baselines/rules.py`).
- Validation of the port: at C=1200 our reconstructed FA Money = 8826 and
  FWF = 7640 vs paper-reported 8591.65 / 7810.86 (~3-5%). This close agreement
  on the traceable rules is the main evidence that the environment/data port is
  faithful. `ARTIFACT_REGENERATED`.

## 4. Learned policies (`REIMPLEMENTED`)
- JA-PPO (joint (k+1)^2), IFAC (two independent heads, 2(k+1) logits), SC-FAC
  (settle-embedded flush head). Trained with clipped PPO + GAE. All
  hyperparameters absent from the paper (learning rate, budget, schedule,
  minibatch, ...) are marked `source: chosen_for_reimplementation` and fixed on
  validation pilots, never on test.

## 5. Regenerated results and comparison to reported Table II
Deterministic test, our reimplementation (3000-episode PPO; multi-seed
matrix in progress), vs paper-reported (REPORTED_ONLY):

| C | method | ours (REIMPL., seed 123 trace) | paper REPORTED |
|---|---|---|---|
| 1200 | FA | 8826 | 8591.65 |
| 1200 | FWF | 7640 | 7810.86 |
| 800 | JA-PPO | ~2550-3373 across 5 seeds (mean ~3000) | 3368.57 |
| 1200 | JA-PPO | 11604 (s123) | 14443.01 |
| 1200 | IFAC | 13118 (s123) | 14472.93 |
| 1200 | SC-FAC | 13210 (s123) | 14687.65 |

- Rule references match closely; learned reimplementation lands in the same
  regime but does NOT exactly match reported learned numbers (expected: no
  released policy/hyperparameters). We do not backfit to Table II.

## 6. Corrective findings (see NOVELTY_AND_OVERLAP.md)
- **Strong baseline** (`NEW_EXPERIMENT`): a validation-selected best-fit
  threshold rule BFP0.5 reaches Money 15327 at C=1200 with ZERO avoidable
  drops, i.e. above all learned policies and above the reported SC-FAC.
- **Structural floor** (`CORRECTED_PROTOCOL`): ~400 drops/episode are oversize
  (single transaction larger than a wallet capacity C/k) and are unavoidable for
  EVERY policy.
- **Mechanism** (`REIMPLEMENTED`): accepted value rises and avoidable drops fall
  monotonically JA<IFAC<SC<ceiling.
- **OOD** (`NEW_EXPERIMENT`, negative): BFP0.5 keeps zero avoidable drops after
  every regime switch; the "RL adapts better" hypothesis is not supported.

## 7. Items NOT reproduced / out of scope (honest gaps)
- Reported learned Table II numbers: `REPORTED_ONLY` (no released artifact).
- General-collateral one/two-pool extension (paper Table III): `MISSING_SPEC`;
  no code or specification found → marked NOT_RUN, not fabricated.
- Exact native one-flush FA/FWF: `MISSING_RULE_DEFINITION` (reconstructed).
- money-aligned reward retraining and tau/p retraining: code path exists,
  training NOT_RUN under the current CPU budget.

## 8. Reproduce
```
conda activate kwallet
pytest -q                                   # 37 tests
python -m kwallet.cli gen-pools             # ported pools (cached, hashed)
python scripts/run_experiments.py --tier main --exp matrix_main --workers 5 --threads 10
python scripts/aggregate_results.py --exp matrix_main
python scripts/make_paper_assets.py         # CSV -> tables/figures/claims
```
All numbers in the manuscript are produced by these commands; nothing is
hand-typed.
