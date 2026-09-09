# Blockers / items needing confirmation

## B1 — GPU authorization (RESOLVED 2026-09-10; measured not beneficial)
- 10x RTX 3090 present (driver 580.159.03 / CUDA 13.0). User authorized GPU for
  this project on 2026-09-10.
- At authorization, GPUs 2,3,6,7,8,9 were at 94-100% util under a SEPARATE
  project (envs/glaucoma-vf); GPUs 1 and 4 were fully free. We bind only to free
  devices via CUDA_VISIBLE_DEVICES and never touch other projects' processes or
  drivers.
- Runtime: project env `kwallet` is torch 2.14.0 +cpu. We built an ISOLATED
  `kwallet-gpu` env (torch 2.3.1+cu121 -- the build already proven on these GPUs;
  numpy 1.26.4) with an editable install; `kwallet` (CPU batches) untouched.
- Verified: CUDA_VISIBLE_DEVICES=1 -> RTX 3090 visible, real GPU matmul OK, and
  a real `kwallet.cli train --device cuda` run lands on GPU1 and checkpoints.
- MEASURED (do NOT claim GPU speedup): identical sc_fac/hidden256/OMP=2 gives one
  rollout+update cycle ~10 s on CPU vs ~19 s on CUDA; GPU util ~14%. Batch-1
  sequential rollout + CPU numpy env dominate; GPU launch/transfer overhead makes
  it ~2x slower. Training stays on CPU. A vectorized batched-env rollout would be
  required to benefit (future work). Evidence: runs/gpu_timing_sc.log,
  runs/cpu_timing_sc.log. --device is plumbed through scripts/run_experiments.py
  (train only; eval stays on CPU workers).

## B2 — Disk headroom
- `/data` was 97% full (~214 GB free) at 2026-09-10 audit. Artifacts are small
  (pools ~60 MB, checkpoints <1 MB each); runs/,data/,results/,*.pt gitignored.

## B3 — PPO training budget / hyperparameters absent from paper
- Paper does not report training episodes/iters, lr, clip, minibatch, rollout,
  entropy schedule. We use standard clipped PPO (gamma .99, lambda .95, lr 3e-4,
  clip .2, 10 epochs, mb 512, rollout 8 ep, entropy .02->.001) and select the
  budget on a VALIDATION convergence pilot. Label `chosen_for_reimplementation`.

## B4 — Constrained one-flush FA/FWF exact algorithm not in paper/repo
- Native [1] is multi-flush. We use documented reconstructed references
  (`baselines/rules.py`) and present strong rules separately in Phase 2. Not
  claimed to be an exact reproduction of [1].

## B5 — Paper Table III (general collateral) under-specified
- Divisible collateral / fractional flush / tau=100 / one- vs two-pool extension
  lacks full setup. Marked NOT_RUN / out of scope; not presented as reproduction.

## B6 — Author / prior-submission metadata unknown (blocks submission only)
- Old PDF is anonymous; authorship, ORCID, funding, prior-submission status not
  provided. We will NOT invent these and will NOT submit. Draft stays internal.

## B7 — Push / PR awaiting user
- Work is committed locally to work/icassp2027-reproduce-improve. No push, PR, or
  manuscript submission without explicit user instruction.
