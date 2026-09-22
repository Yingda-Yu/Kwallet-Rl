# Agent Progress — K-Wallet ICASSP 2027

Last updated: 2026-09-22 (finalization pass). Communicate in Chinese; the
manuscript itself is English.

## Overall status

- Research results, training seeds, test pools, and training budgets are
  **FROZEN**. No new PPO training; raw result CSVs are immutable.
- Execution stages: **Stage 1 (reproduce) COMPLETE; Stage 2 (improvements /
  evaluation) COMPLETE; Stage 3 (manuscript) in FINALIZATION** — internally
  complete pending the author's human rewrite and metadata.
- PR **#2** is open on GitHub (`work/icassp2027-reproduce-improve` ->
  `main`), kept **draft**, pushed. It must not be merged or submitted by the
  assistant.
- No GPU work is outstanding; remaining work is author-side.

## Stage 1 — reproduction: COMPLETE

- Environment and twelve-regime traffic generator ported and tested;
  JA-PPO / IFAC / SC-FAC implemented as one-settlement / one-flush policies.
- Provenance, frozen configuration, seeds, and the distinction between
  faithful port and documented re-implementation are recorded in
  `docs/REPRODUCTION_REPORT.md` and `docs/DECISIONS.md`.
- The prior manuscript is unpublished; it is not cited as prior art and its
  reported numbers were removed from the submission-paper table (retained in
  REPRODUCTION_REPORT.md).

## Stage 2 — improvements and evaluation: COMPLETE, FROZEN

- Main capacity matrix (C in {800, 900, 1000, 1200}), 5 seeds, fixed shared
  test pools; seed-level paired Money tests.
- Settle-conditioning mechanism ablations (no-cond., shuffled): null result.
- Cross-k scaling/transfer for k in {6, 12, 24}, set encoder vs flat; failed
  seeds retained.
- Switching streams: six abrupt-change scenarios, 3 learned seeds, rules.
- Parameter/output/CPU efficiency audit. Outputs live under `runs/` and
  `results/tables/`; details in `docs/DECISIONS.md`.

## Stage 3 — manuscript FINALIZATION (internal pass 2026-09-22)

1. State re-audited from the real working tree (git, CSVs, logs).
2. **Fig. 1 / Fig. 2 placeholders RESOLVED**: deterministic matplotlib-only
   vector artwork (`scripts/make_concept_figures.py` ->
   `assets/figs/overview.pdf`, `assets/figs/structures.pdf`); placeholders
   replaced, captions/labels unchanged.
3. **Citation audit DONE**: references 4 -> 16 verified primary sources; all
   cited; three unsupported claims removed/softened; "paper rep." column
   removed from Table 2.
4. **Statistical audit DONE** (`STATISTICAL_AUDIT.md`): every paired test
   recomputed; Holm sensitivity flags IFAC C=900 and the SC-FAC switching
   comparison; three claims marked AUTHOR REVIEW REQUIRED; avoidable-drop
   wording classified as mechanistic, not causal.
5. **AUTHOR_REWRITE_PACKET.md delivered**: factual bullets only, no
   paste-ready prose. The 223-word working abstract exceeds the 200-word
   hard cap and must be shortened (target 120-150).
6. Author metadata fields remain BLOCKED (no guessing).
7. Final clean-build QA is gated on items 5-6.
8. This progress/blocker refresh.
9. Git divergence vs `origin/main` being resolved via merge (no force push).

## Current paper QA snapshot (interim)

5 pages (technical content pages 1-4; page 5 references only), ~278 KB,
0 undefined references/citations, 0 overfull boxes, 5 keywords, all figures
real vector artwork. Final QA rerun required after the author's changes.
