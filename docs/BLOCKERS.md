# Blockers / items needing confirmation

## B1 — GPU authorization (NOT yet authorized)
- 10× RTX 3090 present; GPUs 1/2/4 observed idle. **Idle ≠ authorized.**
  Defaulting to CPU runs (the PPO workload is batch-1-rollout bound; CPU is
  competitive). Large full-matrix sweeps will run on CPU with high parallelism.
- Request: may we run CPU-only full sweeps (no GPU)? If GPU desired for Phase 2
  set-encoder runs, confirm device IDs we are allowed to use. No other users'
  processes will be touched; no driver changes.

## B2 — Disk headroom
- `/data` was 97% full (~225 GB free) at audit. Artifacts are small (pools ~60 MB,
  checkpoints <1 MB each, logs). Monitoring; will not place large files.

## B3 — PPO training budget / hyperparameters absent from paper
- Paper does not report training episodes/iters, lr, clip, minibatch, rollout,
  entropy schedule. We use standard clipped PPO (gamma .99, lambda .95, lr 3e-4,
  clip .2, 10 epochs, mb 512, rollout 8 ep, entropy .02→.001) and select the
  budget on a VALIDATION convergence pilot. Label `chosen_for_reimplementation`.

## B4 — Constrained one-flush FA/FWF exact algorithm not in paper/repo
- Native [1] is multi-flush. We use documented reconstructed references
  (`baselines/rules.py`) and will present strong rules separately in Phase 2.
  Not claimed to be an exact reproduction of [1].

## B5 — Paper Table III (general collateral) under-specified
- Divisible collateral / fractional flush / tau=100 / one- vs two-pool
  extension lacks full setup. Reconstructed as a clearly-labeled extension in
  Phase 2; not presented as reproduction.

## B6 — Author / prior-submission metadata unknown
- Old PDF is anonymous; authorship, ORCID, funding, prior-submission status not
  provided. We will NOT invent these and will NOT submit. Draft stays internal.
