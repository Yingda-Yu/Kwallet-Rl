# ICASSP 2027 Submission Form Content (copy-in reference only)

> This file only organizes the fields to enter in the ICASSP 2027 submission
> system. **No web submission has been or will be performed by the assistant.**
> Items marked **[AUTHOR CONFIRM]** must be filled/confirmed by the author.
> Nothing here is final until the author approves it.

## 1. Title (author-selected)
Auditing Structured Policy Learning for Streaming Transaction Collateral
Control: Factorization, Conditioning, and Cross-Scale Transfer

## 2. Topic areas
- **Primary:** 2.2 Reinforcement Learning **[ML-REI]**
- **Secondary (alternative):** 2.7.5 Emerging Applications of Machine Learning
  **[ML-APP-EMG]**
- **[AUTHOR CONFIRM]** final primary/secondary assignment on the live form,
  since the exact 2027 codes/labels are set in the submission portal.

## 3. Abstract — current long version is in `main.tex` (~200 words; allowed but
##    above the Paper Kit's 100-150 suggestion)

### 3a. Compact candidate (149 words) — **AUTHOR REVIEW REQUIRED**
> This is a factual, evidence-faithful draft for the author to edit in their own
> words. Do **not** paste it as final without review. All quantitative claims
> match the generated CSVs (see SUBMISSION_SNAPSHOT.md).

Streaming payment channels route each arriving transaction into one of k
collateral wallets or drop it, periodically flushing a wallet at a fixed fee.
Across twelve traffic regimes, we re-implement three PPO policies -- a joint
head, independent factorized heads, and a settle-conditioned factored head --
plus a permutation-equivariant, k-independent encoder. Over five seeds, the
conditioned factored policy beats the joint head at all four capacities and the
independent factored policy at three; settle-conditioning itself adds no
detectable gain, confirmed by zero/shuffled-conditioning ablations. The
equivariant encoder deploys zero-shot to unseen wallet counts where a flat
network cannot, with asymmetric transfer and a scale-specific matched-k cost.
A validation-tuned feedback rule attains the highest Money at every capacity
and zero avoidable drops after abrupt regime shifts, beating learning in nearly
every paired comparison. Factorization and equivariance improve structure and
portability; on homogeneous streams a simple fill-feedback rule is the
benchmark to beat.

### 3b. Abstract constraints to re-check after author edit
- Word target ~100-150 (form hard cap typically 200).
- Keep every number traceable; do not reintroduce "significant at every
  capacity" for IFAC or for BFP0.5-vs-all (see claim audit).
- No author/affiliation in the abstract; no references in the abstract.

## 4. Keywords (exactly 5 — final candidate set)
1. reinforcement learning
2. structured policies
3. resource allocation
4. permutation equivariance
5. online decision making

**[AUTHOR CONFIRM]** before submission. The 6th prior keyword
("out-of-distribution") and "policy factorization"/"payment channels" were
removed; adjust only by swapping, keeping the count at 5.

## 5. Paper type / source — **[AUTHOR CONFIRM]**
- Proposed: **Regular conference paper** (standard ICASSP paper; 4 technical
  pages + references-only page permitted by the 2027 template).
- Confirm on the form: not a special-session paper; not a show-and-tell / demo;
  not a Grand Challenge / SPGC entry (unless intended).
- Presentation preference (lecture/poster/no preference): **[AUTHOR CONFIRM]**.
- Student paper competition / best-student-paper eligibility:
  **[AUTHOR CONFIRM]**.
- AI-use / generative-AI declaration: **[AUTHOR CONFIRM final wording]**
  (a disclosure footnote is already present in `main.tex`).
- Prior publication / dual submission / arXiv posting: **[AUTHOR CONFIRM]**
  (see section 8).

## 6. Authors / affiliations / contact / ORCID / funding — BLOCKERS (fill all)

| # | Full name | Order/role (corresp.?) | Affiliation + address | Email | ORCID | Member/grade (if asked) |
|---|-----------|------------------------|-----------------------|-------|-------|--------------------------|
| 1 | Yingda Yu (provisional) | first / corresponding? **[CONFIRM]** | **[FILL]** | **[FILL]** | **[FILL]** | **[CONFIRM]** |
| 2 | **[ADD or delete row]** | | | | | |
| 3 | **[ADD or delete row]** | | | | | |

- Funding / grant / acknowledgment statement: **[FILL]**. If none, the author
  must explicitly state "no funding" rather than leave an implied placeholder.
- Conflict-of-interest / ethics statements, if the form asks: **[AUTHOR CONFIRM]**.
- Copyright authorizing form / eCopyright is completed **after** acceptance in
  the IEEE workflow; do not sign anything prematurely.

## 7. Manuscript file
- File to upload after author finalization: `paper/icassp2027/main.pdf`
  (exact hash/build listed in SUBMISSION_SNAPSHOT.md).
- Template: ICASSP 2027 Paper Kit; `\ninept`; no page numbers; fonts embedded.
- Re-export the PDF **after** the author fills metadata and rewrites the prose;
  do not upload the current AI-assisted draft.

## 8. Prior submission / manuscript status — **[AUTHOR CONFIRM]**
- Relationship of this work to the prior ("old paper") manuscript:
  **[FILL: new submission / substantially extended / independent / etc.]**
- Was any version previously submitted to ICASSP or another venue? **[FILL]**
- Is an arXiv/preprint version public? If yes, provide DOI/URL: **[FILL]**
- Any overlap text/figures with the prior manuscript must be declared; the old
  Table II numbers are already kept in a separate "paper rep." column.

## 9. Pre-submit gate (all must be true before any upload)
- [ ] Author prose rewrite done (HUMAN_REWRITE_CHECKLIST.md).
- [ ] Real author/affiliation/email/ORCID/funding entered in `main.tex`.
- [ ] Final abstract (author-approved, ~100-150 words) and 5 keywords.
- [ ] Final AI-use disclosure matches the live ICASSP 2027 policy.
- [ ] PDF rebuilt; QA in SUBMISSION_SNAPSHOT.md re-run and all green.
- [ ] Author explicitly authorizes submission (the assistant will not submit).
