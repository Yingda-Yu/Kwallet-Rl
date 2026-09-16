# ICASSP 2027 Submission Form Content (copy-in reference only)

> This file only organizes the fields to enter in the ICASSP 2027 submission
> system. **No web submission has been or will be performed by the assistant.**
> Items marked **AUTHOR-CONFIRMED** are locked by the author (2026-09-16);
> items marked **BLOCKED** or **AUTHOR REVIEW REQUIRED** must still be supplied.

## 1. Title — AUTHOR-CONFIRMED (2026-09-16)
Auditing Structured Policy Learning for Streaming Transaction Collateral
Control: Factorization, Conditioning, and Cross-Scale Transfer

## 2. Topic areas — AUTHOR-CONFIRMED (2026-09-16)
- **Primary:** 2.2 Reinforcement Learning **[ML-REI]**
- **Secondary:** 2.7.5 Emerging Applications of Machine Learning
  **[ML-APP-EMG]**
- Only the live portal's exact code/label picker needs mechanical confirmation
  during data entry; the author's choice is locked.

## 3. Abstract — AUTHOR REVIEW REQUIRED (not final)
The compiled `main.tex` currently carries the long working abstract
(~196-218 words; allowed but above the Paper Kit's 100-150 suggestion).

### 3a. Compact candidate (150 words) — AUTHOR REVIEW REQUIRED
> Factual draft for the author to edit in their own words. Do **not** paste as
> final without review. Every quantitative claim matches the frozen CSVs (see
> SUBMISSION_SNAPSHOT.md, section 5). A 2026-09-16 fact check corrected one
> ambiguous sentence (an earlier wording could be read as SC-FAC beating IFAC
> at three capacities, which the data do not support -- SC-FAC beats IFAC only
> at C=1000); the sentence now states both factorized policies vs the joint
> head unambiguously.

Streaming payment channels route each arriving transaction into one of k
collateral wallets or drop it, periodically flushing a wallet at a fixed fee.
Across twelve traffic regimes, we re-implement three PPO policies -- a joint
head, independent factorized heads, and a settle-conditioned head -- plus a
permutation-equivariant, k-independent encoder. Over five seeds, both
factorized policies beat the joint head -- the conditioned one at all four
capacities and the independent one at three of four; settle-conditioning adds
no detectable gain, confirmed by zero/shuffled-conditioning ablations. The
equivariant encoder deploys zero-shot to unseen wallet counts where a flat
network cannot, with asymmetric transfer and a scale-specific matched-k cost.
A validation-tuned feedback rule attains the highest Money at every capacity
and zero avoidable drops after abrupt regime shifts, beating learning in nearly
every paired comparison. Factorization and equivariance improve structure and
portability; on homogeneous streams a simple fill-feedback rule is the
benchmark to beat.

### 3b. Abstract constraints to re-check after author edit
- Word target 100-150 (form hard cap typically 200); candidate is 150.
- Keep every number traceable; do not reintroduce "significant at every
  capacity" for IFAC or for BFP0.5-vs-all (see claim audit).
- No author/affiliation in the abstract; no references in the abstract.

## 4. Keywords — AUTHOR-CONFIRMED (2026-09-16), exactly 5
1. reinforcement learning
2. structured policies
3. resource allocation
4. permutation equivariance
5. online decision making

Already applied in `main.tex`. The earlier 6-term list (which included
"out-of-distribution") and the intermediate "policy factorization"/"payment
channels" terms are superseded; do not re-add without dropping one.

## 5. Paper type / source — BLOCKED (author confirmation)
- Proposed: **Regular conference paper** (4 technical pages + references-only
  page permitted by the 2027 template).
- Confirm on the form: not special-session; not show-and-tell/demo; not a Grand
  Challenge/SPGC entry (unless intended).
- Presentation preference (lecture/poster/no preference): **BLOCKED**.
- Student-paper competition / best-student-paper eligibility: **BLOCKED**.
- AI-use / generative-AI declaration final wording: **BLOCKED** (a disclosure
  footnote is present in `main.tex`; wording must be finalized by the author to
  match the live ICASSP 2027 policy).
- Prior publication / dual submission / arXiv posting: **BLOCKED** (section 8).

## 6. Authors / affiliations / contact / ORCID / funding — BLOCKED (fill all)

| # | Full name | Order/role (corresp.?) | Affiliation + address | Email | ORCID | Member/grade (if asked) |
|---|-----------|------------------------|-----------------------|-------|-------|--------------------------|
| 1 | Yingda Yu (provisional) | first / corresponding? **[CONFIRM]** | **[FILL]** | **[FILL]** | **[FILL]** | **[CONFIRM]** |
| 2 | **[ADD or delete row]** | | | | | |
| 3 | **[ADD or delete row]** | | | | | |

- Funding / grant / acknowledgment statement: **[FILL]**. If none, the author
  must explicitly state "no funding" rather than leave an implied placeholder.
- Conflict-of-interest / ethics statements, if the form asks: **BLOCKED**.
- eCopyright is completed after acceptance in the IEEE workflow; do not sign
  prematurely.

## 7. Manuscript file
- Internal frozen QA build (NOT for final submission):
  `paper/icassp2027/submission_v1_internal.pdf` (byte-identical to the QA'd
  `main.pdf`; hash in SUBMISSION_SNAPSHOT.md).
- Final upload (only after author metadata + prose rewrite): rebuild
  `main.pdf` from the official template; `\ninept`; no page numbers; fonts
  embedded. Do not upload the AI-assisted draft or the *_internal.pdf.

## 8. Prior submission / manuscript status — BLOCKED
- Relationship of this work to the prior ("old paper") manuscript:
  **[FILL: new submission / substantially extended / independent / etc.]**
- Was any version previously submitted to ICASSP or another venue? **[FILL]**
- Is an arXiv/preprint version public? If yes, DOI/URL: **[FILL]**
- Any overlap text/figures with the prior manuscript must be declared; the old
  Table II numbers are already kept in a separate "paper rep." column.

## 9. Pre-submit gate (all must be true before any upload)
- [ ] Author prose rewrite done (HUMAN_REWRITE_CHECKLIST.md).
- [x] Title confirmed (2026-09-16).
- [x] Primary/secondary topics confirmed (2026-09-16).
- [x] Five keywords confirmed and applied in main.tex (2026-09-16).
- [ ] Final abstract approved by author (~100-150 words); candidate ready.
- [ ] Real author/affiliation/email/ORCID/funding entered in `main.tex`.
- [ ] Final AI-use disclosure matches the live ICASSP 2027 policy.
- [ ] PDF rebuilt after metadata/prose changes; QA re-run; snapshot refreshed.
- [ ] Author explicitly authorizes submission (the assistant will not submit).
