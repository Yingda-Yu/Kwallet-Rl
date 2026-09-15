# Human Rewrite Checklist — ICASSP 2027 manuscript

**Status of the companion file (`main.tex`):** internal AI-assisted draft.
The experiments, numbers, tables, figures, statistics, and LaTeX structure are
final and traceable to generated CSVs. **The prose is not author-finalized and
must be substantively rewritten by you (the human author) in your own words
before submission**, in line with the current ICASSP 2027 AI policy. AI use is
already disclosed in the title footnote; keep/update that disclosure to match
your actual use.

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

### Abstract (current draft ~200 words; Kit suggests ~100-150)
Rewrite yourself from this **factual bullet skeleton** (not prose to copy); fill
it in in your own words and compress to ~120-140 words.

- **Problem:** stream collateral control -- route each arriving transaction
  into one of k wallets or drop it; flush a wallet at a fixed fee; online,
  partially-specified MDP over 12 traffic regimes.
- **Scope:** faithful port of environment/generator; re-implementation of three
  PPO policies (joint head JA-PPO; independent factorized heads IFAC;
  settle-conditioned factored SC-FAC).
- **Finding 1 (factorization, positive):** SC-FAC significantly beats JA-PPO
  at all four capacities (p <= 0.013; 5/5 seeds); IFAC beats JA-PPO at 3 of 4
  (C=800/900/1200; not C=1000, p=0.57).
- **Finding 2 (conditioning, null):** SC-FAC vs IFAC CIs cross zero at
  C=900/1000/1200 and SC-FAC is significantly *lower* at C=800 (-419,
  p=0.009); zero/shuffled-conditioning ablations indistinguishable.
- **Finding 3 (cross-k):** k-independent equivariant set encoder deploys
  zero-shot to unseen k (flat MLP cannot); retention asymmetric (~65% mean
  off-diagonal) with a matched-k cost.
- **Finding 4 (strong rule + OOD negative):** validation-selected rule BFP0.5
  attains highest Money at every C, zero avoidable drops on stationary streams
  and on all 6 abrupt-switch scenarios; significant in 11/12 stationary paired
  comparisons (exception: vs IFAC at C=1000, p=0.057); no evidence learning
  adapts better to shifts.
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
  "state-of-the-art").

### Policies / Model / Data (Sections 2-3)
- Mostly technical and accurate; rewrite for clarity only.
- Keep the explicit label that hyperparameters absent from the prior
  manuscript were chosen on validation (`chosen_for_reimplementation`).

### Experiments (Section 5)
- Stationary paragraph: keep the exact significance pattern now in the draft
  (SC-FAC 4/4 vs JA-PPO; IFAC 3/4; conditioning null incl. C=800 reversal;
  BFP0.5 11/12). You may reword, not re-claim.
- Ablations: present as null.
- Cross-k: state deployability as the contribution; state matched-k cost and
  asymmetry explicitly.
- Switching/OOD: keep the honest negative. Allowed direction: learned policies
  beat naive rules under shifts but do not beat BFP0.5; no demonstrated
  adaptation advantage.

### Discussion and limitations
- Rewrite; preserve the "wallet fill ~ sufficient statistic on homogeneous
  i.i.d. streams" interpretation and the explicit limitations list.
- Do **not** insert a new untested heterogeneous-environment success story.

### Conclusion
- Rewrite in your voice; same four evidence points; no new claims.

### Title (provisional; your call)
Current: "Auditing Structured Policy Learning for Streaming Transaction
Collateral Control: Factorization, Conditioning, and Cross-Scale Transfer".
Keep, shorten, or replace after the rewrite.

## Keywords (currently 6; at most 5 allowed)

Current: reinforcement learning; payment channels; resource allocation;
permutation equivariance; policy factorization; out-of-distribution.

**Proposal (not applied -- your decision):**
- **Recommended:** delete **out-of-distribution** (OOD content remains in the
  switching section; it is the least core term for the positive results).
- Alternative: delete **resource allocation** (generic) if you prefer to keep
  the OOD framing.
- Do not add keywords without dropping one.

## Metadata you must supply (do not let anyone guess)

- [ ] Full author list and ordering
- [ ] Affiliation(s) and address(es)
- [ ] Corresponding author email / contact
- [ ] ORCID iD for every author
- [ ] Funding / grant / acknowledgment statement
- [ ] Prior manuscript / submission status (relation to the old paper)
- [ ] Final AI-use disclosure wording consistent with ICASSP 2027 policy
- [ ] Final title
- [ ] Final keyword choice (<= 5)
- [ ] Confirm topic area code (draft used ML-REI) on the submission form

Replace the `\name{}` / `\address{}` placeholders only when you have this.

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
   legibility, column balance.
8. Text search in `main.tex`: no `TODO`, `FIXME`, `XX`, `pending`,
   `placeholder`, "Anonymous Authors" (the intentional author placeholder must
   be replaced with real metadata before submission).
9. Only then mark the PR ready for review / submit. Do not submit until author
   metadata and the final AI disclosure are in place.
