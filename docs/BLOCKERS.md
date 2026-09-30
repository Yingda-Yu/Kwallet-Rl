# Blockers — K-Wallet ICASSP 2027

Last updated: 2026-09-22. Supersedes all earlier blocker lists.

## Resolved (READY) — author identity fields

The following author-identity fields are CONFIRMED and written into
`paper/icassp2027/main.tex`. The assistant did not modify `main.tex` in this
metadata pass.

- **final author list**: READY — 5 authors: Yingda Yu, Sijia Zhou, Jiaqi
  Xuan, Zhentong Ye, Guanchao Tong.
- **author order**: READY — fixed order (Yu, Zhou, Xuan, Ye, Tong); do not
  change.
- **author affiliations**: READY — Wenzhou-Kean University (authors 1, 2, 3,
  5); Northwestern University (author 4).
- **corresponding author identity**: READY — Guanchao Tong (author 5),
  marked * in main.tex.
- **Industry / Academia / Both**: READY — Academia (all authors academic).

## Active blockers

### B1 — Author contact / identifiers / funding (BLOCKED on the author)
The author block is confirmed, but the following must NOT be guessed:
- contact email for all 5 authors (corresponding author = Guanchao Tong):
  BLOCKED;
- ORCID iD for every author: BLOCKED;
- funding / acknowledgements (or an explicit "no funding"): BLOCKED;
- IEEE member grade, department, city/country, postal address (if the live
  form asks): BLOCKED — not guessed.

### B2 — Human rewrite (BLOCKED on the author per ICASSP 2027 AI policy)
- Substantial prose must be authored by a human; assistant provides only
  `AUTHOR_REWRITE_PACKET.md` (factual bullets; no final prose).
- The compiled working abstract was **223 words** (over the 200-word hard
  form cap); after the 2026-09-22 Holm-corrected wording edits the count
  needs rechecking (should be similar/slightly different) and must still be
  shortened to 120-150 words.
- Overclaim terms removed from main.tex and must NOT be reintroduced:
  "partially-specified MDP", "near-optimal", "sufficient statistic", "causal
  value", "adapting without retraining", "deterministic code".
- Holm-corrected statistical findings now in main.tex (AUTHOR REVIEW REQUIRED
  to confirm the prose):
  1. IFAC vs JA-PPO: 3/4 raw -> 2/4 after Holm (C=900 p_Holm=0.064);
  2. SC-FAC vs JA-PPO: 4/4 raw, all 4 survive Holm;
  3. SC-FAC switching: Money raw p=0.035, Holm p=0.069 -> NOT significant;
  4. k=24: 9190 includes one failed seed; 13785 excluding vs 13610 flat -- a
     sensitivity finding.
- final manuscript sections must receive substantive human rewrite: PENDING.

### B3 — Declarations (BLOCKED on the author)
- Final AI-use disclosure wording matching the live ICASSP 2027 policy
  (AUTHOR CONFIRMATION REQUIRED; the factual checklist in
  FINAL_SUBMISSION_GATE.md section 1a must NOT be deleted or understated; the
  assistant will NOT decide final disclosure wording);
- prior submission / preprint / dual-submission status and overlap with the
  prior manuscript: BLOCKED;
- IEEE privacy/event-terms acknowledgement on the form (cannot be
  pre-accepted); final upload authorization (assistant will not submit).

### B4 — Final QA and submission (gated)
- Full clean rebuild and Final PDF QA can only run after B1-B3; afterwards
  refresh FINAL_SUBMISSION_GATE.md, SUBMISSION_SNAPSHOT.md and
  SUBMISSION_ARTIFACT_SHA256.json. PDF/CMS consistency of title, authors,
  abstract and keywords is part of this gate.

## Resolved / removed stale blockers

- ~~"convergence pilot running"~~ — all training and evaluation complete and
  frozen; no pilot is running.
- ~~"Phase 2 / Phase 3 not started"~~ — improvements and manuscript drafts
  are complete.
- ~~"push / PR awaiting user"~~ — PR #2 is open, pushed, draft; divergence
  vs main is handled via merge in the finalization pass.
- ~~"author list / order / affiliations / corresponding / Academia"~~ —
  RESOLVED (2026-09-22); written into main.tex.
- No GPU/scheduler blocker: no GPU work remains.
