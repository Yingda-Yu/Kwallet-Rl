# Agent Progress — K-Wallet ICASSP 2027

Last updated: 2026-09-22 (finalization + author-metadata pass). Communicate
in Chinese; the manuscript itself is English.

## Overall status

- Research results, training seeds, test pools, and training budgets are
  **FROZEN**. No new PPO training; raw result CSVs are immutable.
- Execution stages: **Phase 1 (reproduce) COMPLETE; Phase 2 (improvements /
  evaluation) COMPLETE; experiments FROZEN; Phase 3 (manuscript) in
  FINALIZATION** — internally complete pending the author's human rewrite and
  remaining metadata (email / ORCID / funding / prior-submission / AI
  disclosure wording).
- Author list, order, affiliations, and corresponding author (Guanchao Tong)
  are **CONFIRMED** and written into `main.tex`. Industry/Academia/Both =
  Academia. Contact email, ORCID, and funding remain BLOCKED.
- PR **#2** is open on GitHub (`work/icassp2027-reproduce-improve` ->
  `main`), kept **draft**, pushed, mergeable/clean. It must not be merged or
  submitted by the assistant.
- No GPU work is outstanding; remaining work is author-side.

## Phase 1 — reproduction: COMPLETE

- Environment and twelve-regime traffic generator ported and tested;
  JA-PPO / IFAC / SC-FAC implemented as one-settlement / one-flush policies.
- Provenance, frozen configuration, seeds, and the distinction between
  faithful port and documented re-implementation are recorded in
  `docs/REPRODUCTION_REPORT.md` and `docs/DECISIONS.md`.
- The prior manuscript is unpublished; it is not cited as prior art and its
  reported numbers were removed from the submission-paper table (retained in
  REPRODUCTION_REPORT.md).

## Phase 2 — improvements and evaluation: COMPLETE, FROZEN

- Main capacity matrix (C in {800, 900, 1000, 1200}), 5 seeds, fixed shared
  test pools; seed-level paired Money tests.
- Settle-conditioning mechanism ablations (no-cond., shuffled): null result.
- Cross-k scaling/transfer for k in {6, 12, 24}, set encoder vs flat; failed
  seeds retained.
- Switching streams: six abrupt-change scenarios, 3 learned seeds, rules.
- Parameter/output/CPU efficiency audit. Outputs live under `runs/` and
  `results/tables/`; details in `docs/DECISIONS.md`.
- Statistical audit DONE (`STATISTICAL_AUDIT.md`): Holm-corrected findings
  now reflected in main.tex — IFAC 3/4 raw -> 2/4 after Holm (C=900
  p_Holm=0.064); SC-FAC vs JA-PPO 4/4 all survive Holm; SC-FAC switching
  Money raw p=0.035, Holm p=0.069 -> NOT significant; k=24 9190 includes a
  failed seed, 13785 excluding vs 13610 flat. Overclaims removed:
  "partially-specified MDP", "near-optimal", "sufficient statistic", "causal
  value", "adapting without retraining", "deterministic code".

## Phase 3 — manuscript FINALIZATION (internal pass 2026-09-22)

1. State re-audited from the real working tree (git, CSVs, logs).
2. **Author block CONFIRMED**: 5 authors (Yingda Yu, Sijia Zhou, Jiaqi Xuan,
   Zhentong Ye, Guanchao Tong) with affiliations (Wenzhou-Kean University,
   Northwestern University) and corresponding author (Guanchao Tong) written
   into `main.tex`. Industry/Academia/Both = Academia. Email/ORCID/funding
   remain BLOCKED. The assistant did not modify `main.tex` in this metadata
   pass.
3. **Fig. 1 / Fig. 2 placeholders RESOLVED**: deterministic matplotlib-only
   vector artwork (`scripts/make_concept_figures.py` ->
   `assets/figs/overview.pdf`, `assets/figs/structures.pdf`); placeholders
   replaced, captions/labels unchanged. These are real vector artwork, not
   placeholders.
4. **Citation audit DONE**: references 4 -> 16 verified primary sources; all
   cited; three unsupported claims removed/softened; "paper rep." column
   removed from Table 2.
5. **Statistical audit DONE** (`STATISTICAL_AUDIT.md`): every paired test
   recomputed; Holm-corrected findings applied to main.tex (see Phase 2
   bullets); three claims marked AUTHOR REVIEW REQUIRED; avoidable-drop
   wording classified as mechanistic, not causal.
6. **AUTHOR_REWRITE_PACKET.md delivered**: factual bullets only, no
   paste-ready prose. The compiled abstract was 223 words (over the 200-word
   hard cap); after Holm wording edits it needs recounting (similar/slightly
   different) and must be shortened (target 120-150).
7. Author metadata: list/order/affiliations/corresponding/Academia READY;
   email/ORCID/funding/prior-submission/AI-disclosure-wording/human-prose
   BLOCKED.
8. Final clean-build QA is gated on the remaining BLOCKED items.
9. This progress/blocker refresh.
10. Git divergence vs `origin/main` resolved via merge (no force push).

## Current paper QA snapshot (interim)

5 pages (technical content pages 1-4; page 5 references only), ~281 KB,
0 undefined references/citations, 0 overfull boxes, 5 keywords, 16
references, all figures real vector artwork (Fig.1/2 deterministic vector;
Fig.3/4 generated from results CSVs). pytest 37/37 passing. Final QA rerun
required after the author's changes (email/ORCID/funding entry + prose
rewrite + final AI disclosure wording).
