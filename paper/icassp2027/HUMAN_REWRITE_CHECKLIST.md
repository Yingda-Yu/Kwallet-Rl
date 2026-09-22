# Human Rewrite Checklist — ICASSP 2027 manuscript

**Status of the companion file (`main.tex`):** internal AI-assisted draft.
The experiments, numbers, tables, figures, statistics, and LaTeX structure are
final and traceable to generated CSVs. **The prose is not author-finalized and
must be substantively rewritten by you (the human author) in your own words
before submission**, in line with the current ICASSP 2027 AI policy. AI use is
already disclosed in the title footnote; keep/update that disclosure to match
your actual use (see FINAL_SUBMISSION_GATE.md section 1a for the factual
checklist -- do NOT delete or understate it).

**Author metadata status (2026-09-22):** the author list, order, affiliations,
and corresponding author (Guanchao Tong) are CONFIRMED and written into
`main.tex`. What remains BLOCKED for you to supply: contact email (for the
corresponding author and any co-authors the form requires), ORCID iD for every
author, funding/acknowledgment statement, prior-submission/dual-submission
status, and the final AI-use disclosure wording.

## Ground rules for the rewrite

1. **Do not change any number.** Every result is imported from generated files.
   Single source of truth for headline numbers: `assets/paper_claims.json`
   (each entry names its source CSV). Never retype a number from memory or from
   the old paper.
2. **Do not resurrect the old "SC-FAC superiority" story.** Multi-seed evidence
   does not support it.
3. Old-paper Table II values appear only in the separate "paper rep."
   (REPORTED_ONLY) column. Keep them distinct from regenerated results.
4. Keep the title provisional; re-pick it after your rewrite.
5. After rewriting, run the QA sequence at the bottom of this file.

## Evidence map (read while rewriting)

| Claim family | File |
|---|---|
| Main Money table (mean +/- SE, 5 seeds) | `results/tables/matrix_main_main_table.csv` |
| Paired differences / 95% CI / p / wins | `results/tables/matrix_main_paired.csv` |
| Conditioning ablations | `results/tables/matrix_ablation_paired.csv` |
| tau post-hoc sweep | `results/tables/matrix_main_tau_posthoc.csv` |
| Cross-k transfer matrix | `results/tables/kscale_transfer_long.csv` |
| Switching aggregate | `results/tables/switching_summary.csv` |
| Switching learned - BFP0.5 | `results/tables/switching_paired_vs_bfp.csv` |
| Efficiency / params / latency | `runs/bench/bench_C1200.0_k24.csv` |
| LaTeX tables/figures | `assets/tables/*.tex`, `assets/figs/*.pdf` |

## Section-by-section rewrite requirements

### Abstract (compiled working abstract was 223 words; edited for Holm wording -- recount needed; Kit suggests ~100-150)
Rewrite yourself from this **factual bullet skeleton** (not prose to copy); fill
it in in your own words and compress to ~120-140 words.

- **Problem:** stream collateral control -- route each arriving transaction
  into one of k wallets or drop it; flush a wallet at a fixed fee; online
  decision problem over 12 traffic regimes. (The earlier "partially-specified
  MDP" phrasing was an overclaim and has been removed from main.tex.)
- **Scope:** faithful port of environment/generator; re-implementation of three
  PPO policies (joint head JA-PPO; independent factorized heads IFAC;
  settle-conditioned factored SC-FAC).
- **Finding 1 (factorization, positive):** SC-FAC significantly beats JA-PPO
  at all four capacities (p <= 0.013; 5/5 seeds; all 4 survive Holm
  correction); IFAC beats JA-PPO at 3 of 4 raw, but only 2 of 4 after Holm
  family-wise correction (C=900 adjusted p_Holm=0.064; not C=1000, p=0.57).
- **Finding 2 (conditioning, null):** SC-FAC vs IFAC CIs cross zero at
  C=900/1000/1200 and SC-FAC is significantly *lower* at C=800 (-419,
  p=0.009); zero/shuffled-conditioning ablations indistinguishable.
- **Finding 3 (cross-k):** k-independent equivariant set encoder deploys
  zero-shot to unseen k (flat MLP cannot); retention asymmetric (~65% mean
  off-diagonal) with a matched-k cost. k=24 reading (9190 vs 13610) depends on
  one failed seed (13785 excluding it) -- a sensitivity finding, not a clean
  negative.
- **Finding 4 (strong rule + OOD negative):** validation-selected rule BFP0.5
  attains highest Money at every C, zero avoidable drops on stationary streams
  and on all 6 abrupt-switch scenarios; significant in 11/12 stationary paired
  comparisons (exception: vs IFAC at C=1000, p=0.057). SC-FAC switching
  comparison against BFP0.5 is NOT significant after Holm (Money raw p=0.035,
  Holm p=0.069); no evidence learning adapts better to shifts.
- **Take-away:** one sentence on what the audit implies (which inductive bias
  matters; simple feedback is the bar learning must beat here).

Verify the final word count between `\begin{abstract}` and `\end{abstract}`.

### Introduction
- Rewrite in your voice; keep the central research question ("which structural
  inductive biases actually matter, and does learning beat a strong feedback
  rule?").
- Confirm motivation claims about payment channels are consistent with
  citation [1]; do not add unsupported factual claims.
- Keep provenance sentences (ported environment vs re-implemented policies vs
  this study's additions).

### Contribution statements
- Reword the four bullets, but keep exact scope:
  (1) port + policy re-implementation;
  (2) equivariant set encoder (portability, with stated trade-off);
  (3) conditioning ablations framed as a **null result**;
  (4) strong baseline as a first-class finding.
- Do not add claims beyond evidence (no "adaptive", "robust to OOD",
  "state-of-the-art"; the overclaim terms "near-optimal", "sufficient
  statistic", "causal value", "adapting without retraining", "deterministic
  code" have been removed from main.tex -- do not reintroduce them).

### Policies / Model / Data (Sections 2-3)
- Mostly technical and accurate; rewrite for clarity only.
- Keep the explicit label that hyperparameters absent from the prior
  manuscript were chosen on validation (`chosen_for_reimplementation`).

### Experiments (Section 5)
- Stationary paragraph: keep the exact significance pattern now in the draft
  (SC-FAC 4/4 vs JA-PPO, all survive Holm; IFAC 3/4 raw -> 2/4 after Holm;
  conditioning null incl. C=800 reversal; BFP0.5 11/12). You may reword, not
  re-claim.
- Ablations: present as null.
- Cross-k: state deployability as the contribution; state matched-k cost and
  asymmetry explicitly; note the k=24 failed-seed sensitivity.
- Switching/OOD: keep the honest negative. Allowed direction: learned policies
  beat naive rules under shifts but do not beat BFP0.5; SC-FAC switching vs
  BFP0.5 is NOT significant after Holm; no demonstrated adaptation advantage.

### Discussion and limitations
- Rewrite; preserve the "wallet fill ~ sufficient on homogeneous i.i.d.
  streams" interpretation (the stronger "sufficient statistic" wording was an
  overclaim and is removed) and the explicit limitations list.
- Do **not** insert a new untested heterogeneous-environment success story.

### Conclusion
- Rewrite in your voice; same four evidence points; no new claims.

### Title — AUTHOR-CONFIRMED (2026-09-16)
"Auditing Structured Policy Learning for Streaming Transaction Collateral
Control: Factorization, Conditioning, and Cross-Scale Transfer".
Locked; do not change unless the author re-opens it explicitly.

## Keywords — AUTHOR-CONFIRMED (2026-09-16), exactly 5, applied in main.tex
reinforcement learning; structured policies; resource allocation;
permutation equivariance; online decision making.
Locked; any later change must keep the count at 5 and be author-approved.

## Topics — AUTHOR-CONFIRMED (2026-09-16)
Primary 2.2 Reinforcement Learning [ML-REI]; secondary 2.7.5 Emerging
Applications of Machine Learning [ML-APP-EMG].

## Metadata status (2026-09-22)

CONFIRMED and written into `main.tex` (do not let anyone change these without
author approval):
- [x] Full author list (5 authors: Yingda Yu, Sijia Zhou, Jiaqi Xuan, Zhentong
      Ye, Guanchao Tong) and fixed order
- [x] Affiliation(s): Wenzhou-Kean University (1,2,3,5); Northwestern
      University (4)
- [x] Corresponding author: Guanchao Tong (*)
- [x] Industry / Academia / Both = Academia

Still BLOCKED -- you must supply (do not let anyone guess):
- [ ] Corresponding author email / contact
- [ ] ORCID iD for every author
- [ ] Funding / grant / acknowledgment statement (or explicit "no funding")
- [ ] Prior manuscript / submission status (relation to the old paper)
- [ ] Final AI-use disclosure wording consistent with ICASSP 2027 policy
- [ ] IEEE member grade / department / postal address (if the live form asks)
- [x] Final title (confirmed 2026-09-16)
- [x] Final keyword choice, 5 terms (confirmed 2026-09-16)
- [x] Topic areas: primary ML-REI, secondary ML-APP-EMG (confirmed 2026-09-16)

Replace the remaining `\thanks` placeholders (email/ORCID/funding) only when
you have the real values. The author `\name{}`/`\address{}` block is already
filled.

## Post-rewrite QA (run after your edits; no new experiments)

1. **Claim/evidence audit:** every quantitative claim still matches
   `paper_claims.json` / source CSVs; no REPORTED_ONLY number presented as new.
2. **Grammar-only editing pass** (no claim changes).
3. **Citation consistency:** every `\cite` resolves; references match claims;
   bibliography style is the template's `IEEEbib`.
4. **Format QA:** 9 pt minimum; no page numbers; technical content within the
   allowed page limit; any extra page only for template-permitted content.
5. `pytest -q` (37 tests) and a clean TeX build (pdflatex x3 + bibtex):
   rc=0, 0 undefined references/citations, 0 pending placeholders.
6. `pdfinfo` / `pdffonts`: all fonts embedded; check file size.
7. Render **every page** (`pdftoppm`) and inspect: table overflow, figure text
   legibility, column balance. Fig.1/2 are now real vector artwork -- confirm
   visually.
8. Text search in `main.tex`: no `TODO`, `FIXME`, `XX`, `pending`,
   `placeholder`, "Anonymous Authors" (the intentional author placeholder must
   be replaced with real metadata before submission -- author block is done;
   email/ORCID/funding placeholders remain).
9. Only then mark the PR ready for review / submit. Do not submit until
   corresponding email, ORCID(s), funding, prior-submission status, and the
   final AI disclosure are in place.
