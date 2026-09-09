# K-Wallet RL — TRAE autonomous execution master plan

This file is the executable research-and-engineering specification for TRAE/Agent. The goal is not to make small edits; it is to complete the entire project in three ordered stages:

1. **Reconstruct and reproduce the existing paper completely.**
2. **Implement a stronger technical system and run a substantially stronger experiment suite.**
3. **Use TeX Live to produce a new, stronger paper from the verified results.**

Read `AGENTS.md` first. Do not skip phases. Do not fabricate results. Do not stop at routine environment errors.

---

# 0. Ground truth currently visible in this repository

The repository already contains several generations of exploratory code and a frozen four-regime benchmark. Important facts that must be preserved while rebuilding the project:

- `benchmark_v1/` is a frozen difficulty-controlled benchmark with four regimes: SL, SH, BL, BH. It explicitly states that the benchmark definition should not be overwritten.
- Historical code exists in `legacy/`, `src/idea1/`, `src/idea2/`, `src/idea3/`, and `src/ideaextra/`.
- The historical experiment protocol documents a K-wallet environment with per-wallet balance, availability, freeze timer, current transaction value, joint settlement/flush actions, flush-before-settle semantics, delayed refill, and explicit drop handling.
- Current code is fragmented into many large single-file experiments, including static/generalist, regime-aware, context-aware, attention/context variants, generators, and baseline evaluators.
- Current top-level scripts are minimal and do not yet provide a clean canonical end-to-end research interface.
- The user has a local `paper/old paper.pdf`, an ICASSP 2027 paper-template ZIP, and an installed TeX Live toolchain. Those assets may not yet be committed to GitHub.

The old paper title visible locally is:

> **Settle-Conditioned Policy Learning for Streaming Transaction Collateral Control**

The abstract visible locally names these core methods and claims:

- FlushAll
- FlushWhenFull
- JA-PPO
- IFAC
- SC-FAC
- evaluation up to at least `k = 24` wallets
- paired confidence intervals
- scaling/sensitivity diagnostics
- the motivation that JA-PPO output grows quadratically with wallet count, while factorized policies keep output linear
- SC-FAC adds a settlement-to-flush information path

The exact PDF remains the source of truth for definitions, numbers, and experiment settings.

---

# 1. Global success criteria

The project is considered complete only when all of the following are true.

## 1.1 Reproduction completeness

- Every algorithm claimed as implemented/evaluated in the old paper has a canonical implementation.
- Every rule baseline in the old paper has a canonical implementation.
- Every metric appearing in a table/figure is computable from saved raw evaluation data.
- Every major old-paper table/figure has either:
  - been reproduced numerically within reasonable stochastic tolerance, or
  - been marked as non-reproduced with a precise explanation backed by evidence.
- The paper claim ledger maps claims -> code -> config -> run IDs -> generated evidence.

## 1.2 Stronger-method completeness

- The new method removes the main scaling/permutation weaknesses of the old action head.
- The new method is tested on both stationary and nonstationary/hidden-regime transaction streams.
- It is evaluated on scaling, robustness, generalization, and ablation axes.
- The final claim is based on multiple seeds and paired evaluation, not a single lucky run.

## 1.3 Paper completeness

- The new paper compiles with local TeX Live using the official ICASSP 2027 template present on the machine.
- All numerical tables/figures in the new paper are generated from result files.
- There are no placeholder claims such as `XX`, `TODO result`, or unverified best numbers.
- A final clean compile completes without fatal errors.
- The repository contains sufficient instructions for another researcher to reproduce the core results.

---

# 2. Phase 0 — forensic audit and environment bootstrap

This phase must run before modifying the scientific core.

## 2.1 Inspect the actual local repository

Run and save outputs for:

```bash
pwd
git status --short
git remote -v
git branch --show-current
git log --oneline -n 20
find . -maxdepth 3 -type f | sort
```

Confirm that the SSH checkout corresponds to `Yingda-Yu/Kwallet-Rl` and note whether local `paper/` assets are untracked/ignored/uncommitted.

## 2.2 Inspect hardware/runtime

Record:

```bash
python --version
which python
pip --version
nvidia-smi || true
nvcc --version || true
pdflatex --version || true
latexmk --version || true
```

Also record CPU count, RAM, free disk, CUDA availability, and PyTorch build after environment installation.

The user's screenshot shows a Windows client with 16 GB RAM and an RTX 4060 Laptop GPU, but the code is being executed over SSH on another machine. **Do not assume the local Windows GPU is the training GPU. Inspect the SSH server directly.**

## 2.3 Preserve the old paper and template

If the files exist locally:

- move/copy the old paper to `paper/archive/old_paper.pdf` without modifying it;
- unzip/copy the ICASSP 2027 template into `paper/template_reference/` or extract only the files required by the official author kit;
- do not commit a large template ZIP if individual required template files are enough;
- document the source file names and checksums.

## 2.4 Extract the old paper into a claim ledger

Use `pdftotext` if available. Otherwise install the needed PDF text utility or use Python PDF extraction. Create:

`docs/ORIGINAL_PAPER_CLAIM_LEDGER.md`

For every section, table, figure, and algorithm in the old paper, record:

- claim ID, e.g. `C-METHOD-001`, `C-EXP-004`;
- paper page/section/table/figure;
- exact semantic claim in concise paraphrase;
- required code module;
- required config;
- required metric;
- current repository evidence if any;
- status: `missing / partial / implemented / reproduced / contradicted`;
- notes on ambiguity.

At minimum extract:

- environment definition;
- state variables;
- action parameterization;
- wallet replenishment/freeze semantics;
- objective/reward or Money definition;
- JA-PPO architecture;
- IFAC architecture;
- SC-FAC conditional factorization;
- training hyperparameters;
- all capacities/wallet counts;
- transaction distributions/regimes;
- rule baselines;
- evaluation metric definitions;
- seed count;
- confidence interval method;
- every headline number in abstract/conclusion;
- every table and figure.

**No implementation may be called an exact reproduction until this ledger exists.**

## 2.5 Build a dependency environment

Prefer a clean virtual environment or conda environment. Create one canonical dependency file, e.g. `requirements.txt` and optionally `environment.yml`.

Likely dependencies include:

- numpy
- scipy
- pandas
- matplotlib
- torch
- gymnasium (only if useful; do not force a Gym API rewrite if unnecessary)
- tqdm
- pyyaml
- pytest
- pytest-cov
- tensorboard or equivalent lightweight logger if useful

Do not pin arbitrary versions before checking compatibility. Record exact installed versions after success.

Create:

`scripts/bootstrap_env.sh`

It should install dependencies or clearly instruct how to install them, then run import checks.

## 2.6 Phase 0 acceptance gate

Do not continue unless:

- old paper is readable;
- TeX Live commands are discoverable;
- Python environment imports successfully;
- GPU status is known;
- claim ledger skeleton exists;
- current git state is documented.

---

# 3. Phase 1 — exact reconstruction of the original paper

The purpose of Phase 1 is to eliminate the gap between what the old paper claims and what the repository actually contains.

---

## 3.1 Create a canonical Python package

Create a new clean package rather than editing the large historical files in place:

```text
kwallet/
  __init__.py
  envs/
  policies/
  models/
  training/
  evaluation/
  utils/
```

Historical code is reference material only.

The package should support imports such as:

```python
from kwallet.envs.kwallet_env import KWalletEnv
from kwallet.policies.ja_ppo import JAPPOPolicy
from kwallet.policies.ifac import IFACPolicy
from kwallet.policies.sc_fac import SCFACPolicy
```

---

## 3.2 Canonical K-Wallet environment

Implement `kwallet/envs/kwallet_env.py` with config-driven parameters.

Required environment responsibilities:

- maintain `k` wallet states;
- total or per-wallet collateral/capacity according to the old paper;
- settlement decision;
- flush decision;
- freeze duration;
- delayed replenishment;
- transaction progression;
- deterministic seeded reset;
- support pre-generated fixed streams;
- support generated streams;
- expose complete transition bookkeeping via `info`.

### Required semantic unit tests

Create tests for at least:

1. reset balances and timers;
2. valid settlement;
3. insufficient-balance drop;
4. explicit no-settlement action;
5. valid flush;
6. invalid flush on unavailable wallet;
7. delayed refill timing;
8. flush-before-settle ordering;
9. same-wallet flush+settle behavior;
10. oversize transaction handling;
11. episode termination;
12. deterministic fixed-stream evaluation;
13. conservation/accounting invariants;
14. behavior at `k=1`;
15. behavior at largest target `k`.

Do not reuse tests that merely mirror buggy implementation code; include hand-constructed trajectories whose expected values are manually calculable.

---

## 3.3 Transaction stream abstraction

Create `kwallet/envs/transaction_streams.py`.

It should support all distributions/regimes actually used by the old paper. Also provide adapters for existing repository datasets and `benchmark_v1`.

Required properties:

- deterministic generation by seed;
- split separation (train/validation/test);
- fixed held-out streams for paired evaluation;
- stream metadata saved with each run;
- no accidental test leakage into training.

If old paper stream generation differs from current `benchmark_v1`, preserve both as separate named protocols.

---

## 3.4 Rule-based baselines

Implement the exact paper definitions for:

### FlushAll

Do not infer from its name alone. Extract the exact trigger/selection semantics from the paper and/or historical baseline code.

### FlushWhenFull

Likewise use the exact old-paper definition. Add deterministic tests on manually constructed streams.

If other paper baselines exist, implement them too.

All rule-based methods must conform to the same evaluator interface as learned policies.

---

## 3.5 JA-PPO

Implement **Joint-Action PPO** exactly as described by the paper.

Likely form, subject to exact PDF audit:

- one actor representing the full coupled `(settle, flush)` action;
- output size grows as approximately `(k+1)^2`;
- one critic/value head;
- standard clipped PPO objective;
- GAE or exact advantage method used in paper;
- entropy regularization if used;
- training/evaluation action masking only if the original method uses it.

Required tests:

- action encoding/decoding bijection for small k;
- output dimension formula;
- log-prob lookup consistency;
- PPO ratio correctness;
- no invalid tensor shape at target k values.

---

## 3.6 IFAC

Implement **Independent Factorized Actor-Critic** as two factorized action heads:

```text
pi_s(a_s | s)
pi_f(a_f | s)
```

so that:

```text
pi(a_s, a_f | s) = pi_s(a_s | s) * pi_f(a_f | s)
```

unless the paper defines another convention.

The key intended property is linear-size actor output with wallet count rather than quadratic joint output.

Required tests:

- output dimension scales linearly in k;
- joint log probability equals sum of factor log probabilities;
- entropy convention matches the policy factorization;
- sampling matches explicit small-k joint enumeration statistically.

---

## 3.7 SC-FAC

Implement **Settle-Conditioned Factorized Actor-Critic** with directed coupling:

```text
pi_s(a_s | s)
pi_f(a_f | s, a_s)
```

and therefore:

```text
pi(a_s, a_f | s)
= pi_s(a_s | s) * pi_f(a_f | s, a_s)
```

The settlement action must influence the flush distribution through an explicit learned information path.

Possible valid implementations include:

- settlement one-hot/embedding concatenated into flush-head features;
- settlement-selected wallet embedding passed to the flush head;
- a conditional low-rank coupling module.

For **Phase 1**, choose the implementation matching the old paper most closely, not the most sophisticated one.

Required tests:

- changing `a_s` while holding state fixed can change `pi_f`;
- joint log probability is exact;
- PPO ratio uses the correct old/new joint log probability;
- gradients flow through settlement-conditioned flush parameters;
- output dimension remains O(k).

---

## 3.8 PPO trainer shared by JA-PPO / IFAC / SC-FAC

Create a unified trainer under `kwallet/training/`.

Required features:

- rollout collection;
- bootstrapped value estimates;
- advantage normalization;
- PPO clipping;
- minibatch epochs;
- gradient clipping if old paper uses it;
- entropy coefficient;
- learning-rate configuration;
- checkpointing;
- best-validation vs final-policy selection exactly according to the old paper;
- deterministic evaluation mode;
- no epsilon-greedy in PPO evaluation.

Do not maintain three separate copy-pasted PPO loops.

---

## 3.9 Metrics and evaluator

Create a single evaluator with a fixed schema.

At minimum support:

- `Money` / utility metric exactly as defined by paper;
- transaction count acceptance ratio;
- value acceptance ratio;
- drop rate;
- oversize drop rate if applicable;
- number/rate of flushes;
- collateral utilization;
- invalid-action rate if relevant;
- per-episode return;
- mean and dispersion across episodes/seeds;
- policy inference cost if measured.

Store per-episode raw metrics before aggregation.

Use the same transaction streams for paired comparisons among policies.

---

## 3.10 Reproduction configs

Create version-controlled configs under `configs/reproduction/`.

There must be a machine-readable config for every experiment family in the old paper, including all claimed k/capacity settings.

Example only — replace with exact paper values:

```text
configs/reproduction/
  main_k4.yaml
  main_k8.yaml
  main_k12.yaml
  main_k16.yaml
  main_k24.yaml
  scaling.yaml
  sensitivity.yaml
```

Do not infer missing values from the abstract if the full paper specifies them.

---

## 3.11 Reproduction experiment matrix

Create `docs/EXPERIMENT_MATRIX.md` before long runs.

For each experiment row record:

- experiment ID;
- old-paper table/figure target;
- method;
- environment config;
- stream config;
- training seeds;
- evaluation seeds/stream IDs;
- train budget;
- expected output files;
- GPU requirement;
- status.

Suggested run sequence:

### Tier A — smoke

- each rule baseline;
- JA-PPO short run;
- IFAC short run;
- SC-FAC short run;
- one tiny `k` and one large `k` shape test.

### Tier B — one-seed integration

- run all methods on one principal setting;
- verify metrics, result schema, plotting, and paper-table generation.

### Tier C — full reproduction

- all paper settings;
- all declared seeds;
- all tables/figures;
- paired CI computation.

---

## 3.12 Confidence intervals/statistics

The old paper abstract explicitly mentions paired confidence intervals. Implement these correctly.

Preferred design:

- evaluate two policies on identical held-out streams;
- compute per-stream or per-episode paired differences;
- use a paired t-interval or paired bootstrap depending on old-paper definition;
- report mean difference and 95% CI;
- never compute an unpaired CI when a paired design is available.

Implement `kwallet/evaluation/statistics.py` and test it on synthetic arrays with known answers.

---

## 3.13 Old-paper result reproduction

For each old paper table/figure:

1. run canonical code;
2. produce a structured result file;
3. aggregate it with a script;
4. compare reproduced values to paper values;
5. classify each row as:
   - matched;
   - close within stochastic tolerance;
   - materially different;
   - impossible to verify.

Create `docs/REPRODUCTION_REPORT.md` with absolute and relative discrepancies.

Do **not** massage hyperparameters after viewing the test result solely to force a match. If tuning is necessary, use validation data and document it.

---

## 3.14 Phase 1 acceptance gate

Phase 1 is complete only when:

- all tests pass;
- each original method exists in canonical code;
- all old-paper experiment families have executable configs;
- at least one end-to-end full setting succeeds;
- the full reproduction suite has been attempted;
- claim ledger is updated with evidence;
- discrepancies are documented;
- the code no longer depends on manual editing of giant experiment files to switch settings.

---

# 4. Phase 2 — build a stronger research contribution

The old paper's main architectural story is useful but can be strengthened substantially. The core improvement should target **scaling, permutation structure, and nonstationarity** rather than merely adding a larger MLP.

The recommended new main method is tentatively named:

> **Permutation-Equivariant History-Conditioned SC-FAC (PEHC-SC-FAC)**

The exact name may be changed during paper writing, but the technical components below should be implemented and ablated separately.

---

## 4.1 Weakness A — wallet-index-sensitive flat state

A flat concatenation of `k` wallet features gives the network arbitrary wallet-index semantics and does not naturally generalize across permutations or different k.

### Improvement: shared wallet encoder

Represent each wallet by features such as:

- normalized balance;
- availability flag;
- remaining freeze time;
- optional pending-refill indicator;
- optional normalized capacity if heterogeneous wallets are introduced.

Pass every wallet through the same MLP:

```text
h_i = phi(wallet_i)
```

Use a permutation-invariant global summary:

```text
g = pool({h_i})
```

where pool may be mean/max/attention pooling.

Current transaction features and recent-context features form separate embeddings.

This gives a set-structured state representation.

---

## 4.2 Weakness B — action logits not structurally tied to wallets

The action head should score wallets with a shared function rather than allocate unrelated output neurons to wallet indices.

### Improvement: pointer-style settlement head

For each wallet:

```text
settle_logit_i = f_settle(h_i, g, tx_embed, history_embed)
```

plus one learned/logit path for `no-settle`.

This keeps output O(k) and is permutation equivariant.

### Improvement: conditioned pointer-style flush head

After a settlement action is sampled/chosen, form a settlement context:

- selected wallet embedding if a wallet was chosen;
- learned embedding for no-settle;
- transaction embedding;
- global state embedding.

Then score each flush candidate with shared parameters:

```text
flush_logit_j = f_flush(h_j, g, tx_embed, history_embed, settle_context)
```

plus `no-flush`.

This preserves the SC-FAC directional dependency while making wallet scoring permutation-equivariant.

---

## 4.3 Weakness C — purely instantaneous observation cannot infer stream regime

Existing repository work already explores context-aware DQN and hidden switching. Incorporate that idea cleanly into the actor-critic paper as a separate component, not as a tangle of special-purpose scripts.

### Improvement: recent-history encoder

Maintain a fixed recent window or compact online summary using features such as:

- recent transaction mean/std;
- quantiles or normalized high-value frequency;
- burstiness/inter-arrival proxy if applicable;
- recent accepted value ratio;
- recent drop rate;
- recent flush rate;
- wallet pressure/utilization summary.

Implement two versions for ablation:

1. **Handcrafted statistics encoder** — lightweight and interpretable.
2. **GRU history encoder** — consumes recent transaction/state summaries.

Do not require a Transformer unless results clearly justify it.

The main paper should emphasize that the history component enables adaptation under hidden regime switching without oracle regime labels.

---

## 4.4 Weakness D — invalid or dominated actions waste probability mass

Add feasibility masks as an **optional, explicitly ablated** engineering improvement.

Possible masks:

- cannot settle a transaction in a wallet that is unavailable;
- cannot settle where balance is insufficient;
- cannot flush an unavailable/frozen wallet;
- rules for simultaneous settle+flush must respect environment semantics.

Important: masking changes the effective policy class. Therefore report it as a separate ablation, not a hidden implementation tweak.

Compare:

- no mask;
- hard feasibility mask.

---

## 4.5 Weakness E — unclear generalization across k

The set/pointer architecture should enable the same parameterization to operate at multiple wallet counts.

Design an explicit cross-k experiment:

- train on a subset of k values, e.g. small/medium;
- test zero-shot on unseen k where mathematically valid;
- fine-tune on unseen k and compare sample efficiency;
- compare to flat MLP SC-FAC, which typically needs size-specific output layers.

Do not claim zero-shot cross-k generalization unless the code truly uses size-agnostic operations.

---

# 5. Phase 2 experiment program

The final experiment suite should be materially stronger than the old paper.

## 5.1 E1 — exact old-paper benchmark comparison

Compare on the original paper protocol:

- FlushAll
- FlushWhenFull
- JA-PPO
- IFAC
- SC-FAC
- PE-SC-FAC (equivariant, no history)
- PEHC-SC-FAC (equivariant + history)

Purpose: establish that the new method does not sacrifice performance on the original task.

## 5.2 E2 — scaling in wallet count

Use a broad k range, including and extending the old maximum if compute allows, for example:

`k ∈ {2, 4, 8, 12, 16, 24, 32, 48, 64}`

Only use k values that remain meaningful under the paper's capacity definition.

Report:

- actor output dimension;
- parameter count;
- forward latency;
- training wall time;
- peak GPU memory;
- performance metric;
- invalid-action rate.

This experiment should directly visualize the quadratic-vs-linear/scalable action parameterization story.

## 5.3 E3 — capacity and freeze sensitivity

Vary the key environment difficulty controls from the old paper, especially:

- total capacity or wallet capacity;
- freeze duration F;
- transaction scale T;
- load/arrival intensity if applicable.

Use a small but systematic grid. Avoid uncontrolled combinatorial explosion.

## 5.4 E4 — frozen benchmark_v1 generalization

Use `benchmark_v1` exactly as frozen:

- SL: smooth + light-tail
- SH: smooth + heavy-tail
- BL: bursty + light-tail
- BH: bursty + heavy-tail

Train/evaluate:

- specialists per regime;
- static generalist;
- equivariant generalist;
- history-conditioned generalist.

Report cross-regime matrix and generalist-vs-specialist gap.

## 5.5 E5 — hidden switching benchmark

Construct/version a benchmark where regime labels are not observed by the policy and the stream changes during an episode.

Switching patterns should include at least:

- one abrupt switch;
- repeated alternating switches;
- randomized dwell times;
- unseen transition order.

Do not overwrite benchmark_v1; create a clearly versioned switching benchmark.

Compare:

- static SC-FAC;
- history-statistics SC-FAC;
- GRU-history SC-FAC;
- oracle regime-conditioned upper bound;
- optional classifier-router baseline.

Report performance before/after switches and adaptation lag, not only episode-average Money.

## 5.6 E6 — permutation test

For a fixed physical wallet state, randomly permute wallet indices.

Evaluate whether policy behavior/performance changes.

Compare:

- flat MLP SC-FAC;
- permutation-equivariant SC-FAC.

Metrics:

- distribution/logit equivariance error;
- performance under random index permutations.

This is a critical mechanistic validation of the new architecture.

## 5.7 E7 — cross-k generalization

Train one size-agnostic policy on mixed k values and test on unseen k.

Compare against:

- independently trained flat SC-FAC at each k;
- mixed-k equivariant model;
- mixed-k equivariant+history model.

Report zero-shot and fine-tuned performance.

## 5.8 E8 — ablation suite

At minimum:

1. IFAC vs SC-FAC: value of settlement-to-flush conditioning.
2. SC-FAC vs PE-SC-FAC: value of permutation-equivariant wallet encoding.
3. PE-SC-FAC vs PEHC-SC-FAC: value of history.
4. history statistics vs GRU history.
5. no action mask vs feasibility mask.
6. mean pooling vs attention pooling if attention is used.
7. remove global wallet summary.
8. remove selected-settlement embedding from flush head.

Ablations must use the same train budget and paired evaluation protocol.

## 5.9 E9 — statistical confirmation

For headline claims, use at least 5 seeds; 10 seeds if runtime allows.

For every main comparison report:

- mean;
- standard deviation or standard error;
- 95% CI;
- paired difference CI;
- exact number of independent training seeds;
- exact number of fixed evaluation streams/episodes.

Where many comparisons are made, avoid overclaiming marginal differences.

## 5.10 E10 — failure analysis

Create qualitative/trajectory analysis for representative cases:

- high-value transaction arrives during collateral pressure;
- wrong early flush causes temporary liquidity shortage;
- hidden regime switches from smooth to bursty/heavy-tail;
- history-aware policy adapts flush behavior;
- rule baseline fails due to non-adaptive trigger.

Plot wallet balances, availability, transaction value, settle target, flush target, accepted/dropped status over time for a small number of interpretable episodes.

---

# 6. Experiment scheduling strategy

The agent must not launch the entire grid blindly.

## Stage 1 — CPU semantic validation

- all unit tests;
- all baselines on hand-built streams;
- tiny PPO rollouts.

## Stage 2 — GPU smoke

Run each trainable method for a very short budget.

Check:

- CUDA works;
- GPU utilization appears;
- no leaks/OOM;
- results save correctly;
- evaluation is deterministic on fixed streams.

## Stage 3 — one principal full seed

Run one representative full setting for all old and new methods.

Do not parallelize until this succeeds.

## Stage 4 — multi-seed principal experiments

Run main tables and ablations first.

## Stage 5 — scaling/robustness

Then run expensive k scaling and switching experiments.

## Stage 6 — paper-only confirmatory reruns

Freeze hyperparameters, then rerun only final selected comparisons using clean seeds/streams if needed.

---

# 7. Results directory and schema

Each run should save something like:

```text
results/<phase>/<experiment_id>/<method>/<run_id>/
  config.yaml
  metadata.json
  train_history.csv
  eval_episode_metrics.csv
  eval_summary.json
  checkpoint.pt
```

`metadata.json` should contain:

- git SHA;
- method;
- experiment ID;
- seed;
- device;
- hostname;
- Python version;
- PyTorch version;
- CUDA version;
- timestamp;
- duration;
- result schema version.

Do not commit checkpoints/raw large results by default.

Create compact committed summaries under a location such as:

```text
paper/generated/results_summary.csv
paper/generated/statistical_tests.csv
```

Only after the results are verified.

---

# 8. Automation scripts required

Implement:

## `scripts/smoke_test.sh`

Runs tests and tiny experiments for every method.

## `scripts/run_reproduction.py`

Arguments should include:

```text
--config
--method
--seed
--device
--output-dir
```

## `scripts/run_improved.py`

Same style, with new model options.

## `scripts/aggregate_results.py`

Reads run directories and writes experiment-level CSV/JSON summaries.

## `scripts/make_paper_assets.py`

Produces:

- LaTeX tables;
- numerical macros;
- figure-ready CSVs;
- optionally publication-quality PDF figures.

The script must refuse to generate a headline table from incomplete required runs unless an explicit `--allow-incomplete` flag is passed.

---

# 9. Phase 3 — new paper using TeX Live

This stage begins only after Phase 1 is substantially reproduced and Phase 2 headline experiments are complete.

---

## 9.1 Use the official ICASSP 2027 author kit

Inspect the local template ZIP and its instructions. Confirm:

- page limit;
- anonymous/review formatting rules;
- reference-page rules;
- required style files;
- PDF compatibility constraints.

Do not rely on memory.

Create canonical paper entry point:

`paper/main.tex`

Use modular sections:

```text
paper/sections/
  01_introduction.tex
  02_related_work.tex
  03_problem.tex
  04_method.tex
  05_experiments.tex
  06_results.tex
  07_analysis.tex
  08_conclusion.tex
```

Adjust to actual template/page constraints.

---

## 9.2 Recommended new paper narrative

The stronger paper should not simply say "we tried more models." It should tell one coherent story:

### Problem

Streaming transaction collateral control requires coupled settlement and replenishment decisions under limited collateral and future uncertainty.

### Limitation of joint action

Naive joint action parameterization scales poorly with wallet count and treats wallet identities as unrelated categorical outputs.

### Old contribution retained

Settle-conditioned factorization captures the directional dependency between settlement and flush while reducing output complexity.

### New contribution 1

Permutation-equivariant wallet encoding and pointer-style action heads preserve the K-wallet set structure and naturally scale to variable wallet counts.

### New contribution 2

A lightweight history encoder allows adaptation to latent/nonstationary transaction regimes without requiring oracle regime labels.

### Empirical story

The resulting policy:

- matches or improves the original protocol;
- scales better in k;
- is robust to wallet-index permutation;
- generalizes better across k;
- adapts faster to hidden distribution switches;
- retains the advantage of settlement-conditioned action coupling.

Only include these claims if the experiments support them.

---

## 9.3 Required figures/tables for the new paper

Subject to page limit, prioritize:

### Figure 1 — method overview

Show:

```text
wallet set -> shared wallet encoder -> global pooling
current transaction -> transaction encoder
recent history -> history encoder
          -> settlement pointer head
selected settlement -> conditioning path -> flush pointer head
```

### Figure 2 — action-space/scaling comparison

Plot/logically show:

- JA-PPO output O(k^2);
- IFAC/SC-FAC O(k);
- equivariant SC-FAC parameter sharing/variable-k property.

### Figure 3 — hidden-switch trajectory

Show adaptation around a regime switch.

### Table 1 — original-protocol main results

### Table 2 — scaling/generalization

### Table 3 — ablations

If the venue page limit is tight, move less critical plots to supplementary material if allowed.

---

## 9.4 Paper numbers must be generated

Do not manually type final experimental numbers throughout the paper.

Use generated TeX such as:

```tex
\input{generated/main_results_table.tex}
```

and macros such as:

```tex
\newcommand{\MainGain}{...}
```

created by `scripts/make_paper_assets.py`.

This prevents the text and tables from becoming inconsistent after reruns.

---

## 9.5 TeX Live build loop

Use:

```bash
cd paper
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

If bibliography requires it, configure latexmk/bibtex/biber according to the official template.

On error:

1. inspect the first true LaTeX error, not only the final "failed" line;
2. fix missing package/path/reference;
3. rebuild;
4. repeat until clean.

Create `scripts/build_paper.sh`.

The script should clean stale aux files when explicitly requested but must not delete source/generated assets.

---

## 9.6 Paper audit checklist

Before declaring done:

- title/abstract match actual method and results;
- every numerical claim has result-file evidence;
- old-paper claims are clearly distinguished from new results;
- no unsupported SOTA language;
- related-work citations are real and bibliographically correct;
- figures are legible at final size;
- no table exceeds column width;
- no overfull boxes that materially damage layout;
- all references resolve;
- all figure/table refs resolve;
- no TODO/FIXME/placeholder;
- anonymity requirements satisfied;
- page count satisfies official template instructions;
- final PDF opens successfully.

---

# 10. Final repository documentation

Create/update top-level `README.md` with:

1. what K-Wallet problem is;
2. what the old paper methods are;
3. what the new method is;
4. repository layout;
5. environment installation;
6. smoke test;
7. reproduce old paper;
8. run improved method;
9. aggregate results;
10. compile paper.

Create `docs/REPRODUCIBILITY.md` with exact commands for one representative result and one full experiment family.

---

# 11. Git workflow

Work directly on the user's repository only in logically grouped commits.

Recommended commit sequence:

1. `docs: add reproduction claim ledger and execution matrix`
2. `build: add reproducible python environment and smoke checks`
3. `refactor: add canonical k-wallet environment and metrics`
4. `feat: implement rule baselines and original PPO policies`
5. `test: add environment and factorized-policy correctness suite`
6. `exp: add old-paper reproduction configs and runners`
7. `feat: add permutation-equivariant settle-conditioned policy`
8. `feat: add history-conditioned nonstationary policy`
9. `exp: add ablation scaling and switching experiment suite`
10. `paper: add generated assets and ICASSP manuscript`
11. `docs: finalize reproducibility report`

If a change is incomplete, commit only when it is still coherent and does not break main. Otherwise keep working locally until the gate passes.

---

# 12. Failure-handling rules for autonomous execution

The user intends to enable automatic approvals. Use that autonomy to solve routine problems, but follow these rules.

## Dependency/install error

- inspect error;
- adjust compatible versions;
- retry;
- record final environment.

## Missing old-paper detail

- search the PDF;
- search historical source;
- search experiment notes;
- if still unknowable, mark the ledger ambiguity and implement the most conservative documented interpretation as a separate config.

## CUDA OOM

- lower rollout/minibatch size;
- enable vectorization/mixed precision only if scientifically neutral;
- do not change k, stream, horizon, or architecture silently.

## NaN training

Check in order:

- invalid observations;
- normalization;
- advantage scale;
- reward scale;
- logits/masking;
- learning rate;
- gradient norm;
- PPO ratio explosion.

Add assertions before simply reducing learning rate.

## Reproduction mismatch

Do not overwrite paper numbers. Diagnose:

- environment semantic mismatch;
- reward/metric definition mismatch;
- transaction generator mismatch;
- hyperparameter mismatch;
- checkpoint selection difference;
- seed/evaluation protocol difference.

Document the cause.

## TeX compile error

Fix iteratively until `latexmk` exits successfully.

---

# 13. First concrete tasks TRAE should execute now

Execute these in order:

1. Read `AGENTS.md` and this file completely.
2. Inspect git status and local-only `paper/` files.
3. Create a new working branch such as `research/rebuild-paper-v2` unless the user explicitly wants direct-main development.
4. Preserve/import the old paper and author kit.
5. Extract old PDF text and build `docs/ORIGINAL_PAPER_CLAIM_LEDGER.md`.
6. Build `docs/EXPERIMENT_MATRIX.md` from every old-paper table/figure.
7. Create the clean Python package skeleton and test skeleton.
8. Implement the canonical environment and semantic tests first.
9. Implement rule baselines.
10. Implement the shared PPO machinery and JA-PPO/IFAC/SC-FAC.
11. Run CPU tests and GPU smoke tests.
12. Run one full old-paper principal setting.
13. Only after that, implement PE-SC-FAC and PEHC-SC-FAC.
14. Run the full new experiment program in prioritized order.
15. Aggregate verified results.
16. Build the new ICASSP paper with TeX Live.
17. Perform final claim-to-result audit.
18. Commit and push the completed work.

The agent should continue automatically through these tasks, resolving ordinary implementation/configuration errors on its own. The stopping conditions are only: a genuinely unknowable scientific definition that cannot be recovered from the paper/code, lack of required credentials/data, or a destructive operation that could affect unrelated users/processes/data.