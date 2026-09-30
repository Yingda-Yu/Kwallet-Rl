# Paper → Code map (reproduction traceability)

Each paper component maps to code. Labels: `[PORT]` faithful port of repo code,
`[REI]` reimplemented from paper description (no repo original), `[NEW]` added
for improvement/rigor.

## Environment (paper Sec. IV.C-D)
- 3k+2 state, balances /(C/k), availability, cooldown/F, x/max_tx, t/T
  → `src/kwallet/envs/kwallet.py` `KWalletEnv._obs` `[PORT+REI]`
- flush-first-then-settle, one-settle/one-flush, NONE sentinel, actions 0..k
  (k = no-op) → `KWalletEnv.step` `[REI]` (repo DQN used joint decode)
- freeze F decisions + refill-to-full on timer expiry → cooldown logic `[REI]`
- acceptance Eq.1 (oversize/active_none/frozen/conflict/insufficient)
  → drop reasons in `step` `[REI]`
- reward original (+x/1000, -0.02 drop, -0.01 flush, shaping off) → `step` `[PORT]`
- Money = p·accepted_value − tau·charged_flushes (p=1, tau=10)
  → `KWalletEnv._info` / `money()` `[REI]`

## Data (paper Sec. IV.B, 12 regimes)
- regime generator, calibration, bursts, seed namespaces
  → `src/kwallet/data/regimes.py` `[PORT]` of `src/ideaextra/kwallet_ideaextra_generator.py`
- pool build/cache/hash/manifest → `src/kwallet/data/pools.py` `[NEW]`

## Policies (paper Sec. IV.E-F)
- JA-PPO joint (k+1)^2 → `policies/actors.py:JAPPO` `[REI]`
- IFAC independent 2(k+1) → `policies/actors.py:IFAC` `[REI]`
- SC-FAC settle-conditioned factorized 2(k+1), exact conditional entropy
  → `policies/actors.py:SCFAC` `[REI]`

## Training (paper Sec. IV.G)
- clipped PPO + GAE, whole-episode rollout, true terminal, entropy anneal
  → `training/ppo.py` `[REI]` (hyperparameters not in paper → chosen_for_reimplementation;
  loose reference `legacy/old_code/PRO_RL.py`)

## Rule references (paper Sec. IV.E, Almashaqbeh et al. [1])
- constrained one-flush FA/FWF → `baselines/rules.py` `[REI]`
  (MISSING_RULE_DEFINITION: native [1] is multi-flush; repo one-flush reference
  `src/idea2/fwf_regime_difficulty_eval_fixed.py`)

## Evaluation / statistics
- rollout + per-regime aggregation → `evaluation/rollout.py` `[NEW]`
- process-parallel sharded eval (same single-env logic) → `evaluation/parallel.py` `[NEW]`
- paired-t + bootstrap CIs, seed-level summary → `evaluation/stats.py` `[NEW]`
- model-only latency/params → `evaluation/compute.py` `[NEW]`

## CLI / orchestration
- `python -m kwallet.cli {doctor,gen-pools,train,evaluate,bench}` → `cli.py` `[NEW]`
- matrix driver + manifest → `scripts/run_experiments.py` `[NEW]`

## Paper artifacts (Phase 3)
- official template → `paper/icassp2027/` (compiles, pdflatex rc=0)
- figure/table generation → `scripts/make_paper_assets.py` (Phase 3)

## Provenance anchors (legacy, NOT used for results)
- `legacy/old_code/PRO_RL.py` Bernoulli-PPO prototype (hyperparameter hints)
- `legacy/old_code/FA.py` multi-flush FlushAll (name only; NOT our constrained FA)
- `legacy/old_code/ac_k_wallet.py` exponential (k+1)2^k action (rejected)
- `src/idea2/fwf_regime_difficulty_eval_fixed.py` one-flush round-robin (FWF basis)
