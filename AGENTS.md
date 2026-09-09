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
