# ICASSP 2027 Submission Form Content (copy-in reference only)

> This file only organizes the fields to enter in the ICASSP 2027 submission
> system. **No web submission has been or will be performed by the assistant.**
> Items marked **AUTHOR-CONFIRMED** are locked by the author (2026-09-16);
> author list/order/affiliations/corresponding are CONFIRMED (2026-09-22);
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
The compiled `main.tex` working abstract was **223 words** (measured
2026-09-22), ABOVE the 200-word hard form cap and far above the Paper Kit's
100-150 suggestion. After the 2026-09-22 Holm-corrected wording edits (IFAC
3/4 -> 2/4 after Holm; SC-FAC switching not significant), the word count needs
rechecking -- it should be similar or slightly different. It must still be
shortened to fit the cap.

### 3a. Compact candidate (150 words) — AUTHOR REVIEW REQUIRED
> Factual draft for the author to edit in their own words. Do **not** paste as
> final without review. Every quantitative claim matches the frozen CSVs (see
> SUBMISSION_SNAPSHOT.md, section 5). A 2026-09-16 fact check corrected one
> ambiguous sentence (an earlier wording could be read as SC-FAC beating IFAC
> at three capacities, which the data do not support -- no SC-FAC vs IFAC
> contrast is significant in the positive direction; C=800 is significantly
> negative); the sentence now states both factorized policies vs the joint
> head unambiguously.

**2026-09-22 statistical-audit updates now reflected in main.tex:**
- IFAC vs JA-PPO: 3/4 raw -> 2/4 after Holm family-wise correction
  (C=900 adjusted p_Holm=0.064).
- SC-FAC vs JA-PPO: 4/4 raw; all 4 survive Holm.
- SC-FAC switching: Money raw p=0.035, Holm p=0.069 -> NOT significant.
- k=24 set-vs-flat: 9190 includes one failed seed; 13785 excluding vs 13610
  flat -- a sensitivity finding, not a clean negative.
- Overclaims removed from main.tex: "partially-specified MDP", "near-optimal",
  "sufficient statistic", "causal value", "adapting without retraining",
  "deterministic code".
See STATISTICAL_AUDIT.md and AUTHOR_REWRITE_PACKET.md.

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
  capacity" for IFAC (only 2/4 survive Holm) or for BFP0.5-vs-all (see claim
  audit).
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

## 5. Paper type / source — mostly BLOCKED (author confirmation)
- Proposed: **Regular conference paper** (4 technical pages + references-only
  page permitted by the 2027 template).
- Confirm on the form: not special-session; not show-and-tell/demo; not a Grand
  Challenge/SPGC entry (unless intended).
- Presentation preference (lecture/poster/no preference): **BLOCKED**.
- Student-paper competition / best-student-paper eligibility: **BLOCKED**.
- Industry / Academia / Both: **Academia (READY, 2026-09-22)** -- all authors
  academic (Wenzhou-Kean University; Northwestern University).
- AI-use / generative-AI declaration final wording: **AUTHOR CONFIRMATION
  REQUIRED** (a disclosure footnote is present in `main.tex`; wording must be
  finalized by the author to match the live ICASSP 2027 policy; see
  FINAL_SUBMISSION_GATE.md section 1a factual checklist -- do NOT delete or
  understate).
- Prior publication / dual submission / arXiv posting: **BLOCKED** (section 8).

## 6. Authors / affiliations / contact / ORCID / funding

Author list, order, affiliations, and corresponding author are CONFIRMED
(2026-09-22) and written into `main.tex`. Email, ORCID, and funding remain
BLOCKED. IEEE member grade, department, and postal address are NOT guessed --
the author supplies them if the live form requires them.

| # | Full name | Affiliation | Corresponding? | Email | ORCID |
|---|-----------|-------------|----------------|-------|-------|
| 1 | Yingda Yu | Wenzhou-Kean University | No | **BLOCKED** | **BLOCKED** |
| 2 | Sijia Zhou | Wenzhou-Kean University | No | **BLOCKED** | **BLOCKED** |
| 3 | Jiaqi Xuan | Wenzhou-Kean University | No | **BLOCKED** | **BLOCKED** |
| 4 | Zhentong Ye | Northwestern University | No | **BLOCKED** | **BLOCKED** |
| 5 | Guanchao Tong | Wenzhou-Kean University | Yes (*) | **BLOCKED** | **BLOCKED** |

- Member/grade (if the form asks): **[CONFIRM by author]** -- not guessed.
- Department / city / country / postal address (if the form asks):
  **[CONFIRM by author]** -- not guessed here; the author block in `main.tex`
  carries affiliation names only.
- Funding / grant / acknowledgment statement: **BLOCKED**. If none, the author
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
  reported numbers were removed from the submission-paper table and remain
  only in docs/REPRODUCTION_REPORT.md (the prior manuscript is unpublished
  and is not cited as prior art).

## 9. Pre-submit gate (all must be true before any upload)
- [ ] Author prose rewrite done (HUMAN_REWRITE_CHECKLIST.md).
- [x] Title confirmed (2026-09-16).
- [x] Primary/secondary topics confirmed (2026-09-16).
- [x] Five keywords confirmed and applied in main.tex (2026-09-16).
- [x] Author list, order, affiliations, corresponding author confirmed and in
      main.tex (2026-09-22).
- [x] Industry / Academia / Both = Academia (2026-09-22).
- [ ] Final abstract approved by author (~100-150 words); candidate ready;
      word count needs rechecking after Holm edits.
- [ ] Real corresponding email / ORCID(s) / funding entered in `main.tex`
      (still BLOCKED).
- [ ] Final AI-use disclosure matches the live ICASSP 2027 policy
      (AUTHOR CONFIRMATION REQUIRED).
- [ ] Prior-submission / dual-submission status declared (BLOCKED).
- [ ] PDF rebuilt after metadata/prose changes; QA re-run; snapshot refreshed.
- [ ] Author explicitly authorizes submission (the assistant will not submit).
