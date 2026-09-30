# K-Wallet: repository instructions for coding agents

## Current assignment

The user has requested actual implementation and execution of three linked stages: reproduce the existing K-Wallet paper; implement and evaluate improvements; produce an evidence-backed ICASSP 2027 manuscript using the installed TeX Live and official template.

Before acting, read these files in full:

1. `docs/TRAE_START_HERE.md`
2. `docs/TRAE_KWALLET_ICASSP2027_EXECUTION.md`
3. `docs/TRAE_TASK_BOARD.md`

Then inspect the real working tree and read the user-provided `paper/old paper.pdf` and `paper/ICASSP2027_Paper_Templates.zip`. The input files may exist only in the SSH workspace; do not assume a GitHub tree proves they are absent locally.

These documents are a work assignment, not proof that experiments have run. Implement, test, execute within authorized resources, record results and compile the paper. Do not stop after another planning response.

## Non-negotiable working rules

- Preserve user changes, the original paper, the template archive, frozen benchmarks and historical results. Never force-push, hard-reset or clean the working tree to resolve an ordinary conflict.
- Inspect and reuse existing code before introducing a new package. Distinguish legacy DQN/multi-flush code from the paper's one-settlement/one-flush JA-PPO, IFAC and SC-FAC protocol.
- Missing paper parameters remain missing. Trace original evidence first; a documented reimplementation is acceptable, but is not an exact reproduction.
- Every reported experiment needs resolved configuration, code/data provenance, seed, actual logs, checkpoint provenance, metrics and completion status. Never substitute old-paper numbers for new runs.
- Choose models/hyperparameters on training/validation data, not the final test set. Retain failed seeds and negative results in the experiment record.
- Use isolated user-level dependencies. Reuse the installed TeX Live. Do not alter shared drivers, system Python or global environments without explicit authorization.
- A free-looking GPU is not permission to use it. Honor scheduler allocations and project-specific user authorization; never terminate other users' processes or reset GPUs. Without a confirmed allocation, continue lightweight CPU checks and report the resource blocker.
- Automatic approval does not authorize credential disclosure, paid resources, destructive operations, manuscript submission, author-registration payment or copyright signing.
- Do not infer authorship, ORCID, funding, ethics approvals or the previous submission's status. Missing information blocks final submission readiness, not unrelated engineering.
- Maintain progress/decisions/blockers and a machine-readable run manifest. Resume from real state and logs; do not launch duplicate experiments after a new agent session.
- Validate every PDF page visually as well as by compilation checks. The 2027 template, source-to-result traceability and publication/AI-disclosure rules are part of acceptance.

## Communication and delivery

Communicate progress to the user in Chinese; write the manuscript in English. At each milestone, report concrete changed files, commands run, tests, real experiment status and unresolved items. Push small reviewable commits to a work branch and prepare a PR; do not imply a remote push succeeded without checking it.

For the complete specification and acceptance criteria, the detailed execution brief is authoritative within the user's current request and the available permissions. Higher-priority instructions and subsequent explicit user decisions remain controlling.

---

# Appendix (historical, merged from `main` 2026-09-22)

The text below is the autonomous-agent master plan that lived on `main`.
It is retained for traceability. **Where it conflicts with the current
assignment above, or with the real status in `docs/AGENT_PROGRESS.md`
(experiments frozen; manuscript in finalization; PR #2 open draft), the
current assignment and the status documents control.** Its repository
architecture target was historical planning and does not match the current
tree.

# K-Wallet RL — autonomous agent instructions

This repository is being rebuilt from an exploratory K-Wallet RL codebase into a reproducible research artifact and a stronger paper. Treat `TRAE_MASTER_PLAN.md` as the source of truth for execution order and acceptance criteria.

## Operating mode

- Work autonomously and continue through routine build, dependency, path, plotting, testing, and LaTeX problems instead of stopping after the first error.
- Do **not** silently change the mathematical problem definition to make code pass. If an environment semantic, baseline, metric, or paper claim is ambiguous, extract the exact definition from `paper/old paper.pdf` (or the local equivalent) and record the resolved definition in `docs/ORIGINAL_PAPER_CLAIM_LEDGER.md` before implementation.
- Never fabricate experimental results, confidence intervals, citations, tables, or paper claims. Every number in the new paper must be generated from saved machine-readable experiment outputs.
- Do not overwrite the frozen `benchmark_v1/`. If a benchmark definition must change, create `benchmark_v2/` or another versioned directory.
- Preserve `legacy/` and the existing `src/idea1`, `src/idea2`, `src/idea3`, and `src/ideaextra` as historical references. Build the canonical implementation in a new clean package rather than continuing copy-paste variants.
- Commit code/config/documentation changes; do not commit large checkpoints, transaction pools, raw run directories, or generated binary artifacts unless explicitly required.

## Required execution order

1. **Bootstrap + forensic audit**: inspect git status, local-only paper/template assets, environment, old paper, existing source code, and benchmark semantics.
2. **Phase 1 — exact paper reproduction**: implement all methods/baselines/metrics claimed in the old paper, run tests, reproduce the reported experiment matrix, and create a claim-to-evidence ledger.
3. **Phase 2 — stronger method and experiments**: implement the scalable/permutation-aware/history-aware improvements in `TRAE_MASTER_PLAN.md`; run the predeclared ablation, scaling, robustness, and statistical experiments.
4. **Phase 3 — paper rebuild**: use the installed TeX Live toolchain and the official ICASSP 2027 template already present locally to create a new paper whose tables/figures are generated from actual Phase 1/2 outputs.
5. **Final audit**: clean rerun from documented commands, compile the PDF, check all claims against result files, and produce a concise reproduction README.

Do not begin the stronger-paper experiments before the original-paper implementation passes its semantic tests and reproduction smoke tests.

## Repository architecture target

Create and converge toward this structure (exact module names may be adjusted only when there is a strong engineering reason):

```text
kwallet/
  envs/
    kwallet_env.py
    transaction_streams.py
  policies/
    rule_based.py
    ja_ppo.py
    ifac.py
    sc_fac.py
    equivariant_sc_fac.py
  models/
    wallet_encoder.py
    history_encoder.py
    action_heads.py
    critic.py
  training/
    ppo.py
    rollout.py
    callbacks.py
  evaluation/
    evaluator.py
    metrics.py
    statistics.py
  utils/
    config.py
    seed.py
    io.py
configs/
  reproduction/
  improved/
scripts/
  bootstrap_env.sh
  smoke_test.sh
  run_reproduction.py
  run_improved.py
  aggregate_results.py
  make_paper_assets.py
tests/
results/
  reproduction/
  improved/
paper/
  main.tex
  sections/
  figures/
  generated/
  references.bib
docs/
  ORIGINAL_PAPER_CLAIM_LEDGER.md
  EXPERIMENT_MATRIX.md
  REPRODUCIBILITY.md
```

`results/` is a local/generated artifact tree and should remain ignored except for compact summary CSV/JSON files intentionally committed for reproducibility.

## Canonical environment semantics

The historical protocol states that the base observation contains per-wallet balance, availability, remaining freeze time, plus current transaction value; the historical joint action decodes into settlement and flush choices; the environment executes **flush before settle**; refill is delayed; same-wallet flush+settle causes the transaction not to settle; and oversize transactions are dropped. Preserve these semantics unless the old paper explicitly defines a different protocol. Any divergence must be documented and tested.

For the new canonical environment:

- expose explicit `observation_space`/shape metadata and deterministic reset with seed;
- separate environment transition logic from reward/utility accounting;
- expose a feasibility mask for settlement and flush actions without changing the unmasked reference environment;
- produce an `info` dictionary sufficient to recompute every reported metric independently;
- support fixed transaction streams for paired evaluation across policies;
- support vectorized/batched rollout where practical;
- make `k`, capacity variables, freeze duration, transaction scale, horizon, and stream regime config-driven rather than hard-coded.

## Method definitions to reproduce

The old paper shown in this project names the following methods. The implementation must match the PDF, not a guessed substitute:

- rule baselines including **FlushAll** and **FlushWhenFull**;
- **JA-PPO**: joint-action PPO over the coupled settlement/flush action;
- **IFAC**: independent factorized actor-critic with separate settlement and flush factors;
- **SC-FAC**: settle-conditioned factorized actor-critic implementing a directed information path `settlement -> flush`, i.e. `pi(a_s, a_f | s) = pi_s(a_s | s) * pi_f(a_f | s, a_s)` (subject to the paper's exact conventions).

For factorized policies, PPO log-probability/entropy/ratio calculations must be mathematically consistent with the factorization. Add unit tests that compare factorized joint log-probabilities against explicitly enumerated small-k distributions.

## Engineering quality gates

Before long experiments:

- `python -m pytest -q` must pass;
- a CPU smoke run must finish for each method;
- a short CUDA smoke run must finish when CUDA is available;
- identical seed + identical fixed stream must reproduce identical evaluation trajectories up to documented nondeterminism;
- no NaN/Inf in observations, logits, values, losses, advantages, or metrics;
- saved config must contain all environment/model/training/evaluation parameters;
- each run must save git commit SHA, seed, timestamp, device, Python/PyTorch versions, and result schema version.

## GPU and process safety

- Inspect `nvidia-smi` before allocating GPUs.
- Never kill an unrelated process merely to free VRAM. Only terminate a process when its ownership and relation to this project are verified.
- Prefer a scheduler/explicit `CUDA_VISIBLE_DEVICES` assignment for parallel seed runs.
- Start with smoke tests, then one full seed, then parallelize remaining seeds.
- On OOM: reduce rollout/minibatch size first; do not change the scientific environment or model silently.

## Experiment integrity

- Predeclare the experiment grid in `docs/EXPERIMENT_MATRIX.md` before the large run.
- Use the same held-out transaction streams for paired policy comparisons.
- Report mean, dispersion/CI, number of seeds, and paired uncertainty for headline comparisons.
- Keep screening results separate from final confirmatory results.
- Do not select the best seed for the paper.
- Every final table row must be traceable to a summary CSV/JSON and every summary must be traceable to raw run IDs.

## TeX Live / paper rules

- Use the local official ICASSP 2027 author-kit/template; do not recreate formatting from memory.
- Compile with TeX Live using `latexmk` when available, e.g. `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex`.
- Generated tables and result macros should live under `paper/generated/` and be produced by `scripts/make_paper_assets.py` from result CSV/JSON files.
- Do not hand-copy numerical results into LaTeX if they can be generated.
- Keep the old PDF unchanged under `paper/archive/` once imported.
- Verify the current official page-limit/anonymization/reference rules from the provided author kit before final formatting.

## Definition of done

The project is done only when all three user-requested stages are complete: (1) old-paper code and experiments are reproducible, (2) the stronger method and expanded experiments are implemented and evaluated with ablations/statistics, and (3) a new TeX Live-compiled paper is built from those verified results, with a clean reproduction command documented for another machine.
