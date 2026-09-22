# Blockers — K-Wallet ICASSP 2027

Last updated: 2026-09-22. Supersedes all earlier blocker lists.

## Active blockers

### B1 — Author metadata (BLOCKED on the author)
All of the following are missing and must not be guessed:
- final author list, author order, corresponding author;
- affiliation, department, city/country;
- corresponding email; ORCID for every author;
- funding / acknowledgements (or an explicit "no funding");
- industry / academia / both selection.

### B2 — Human rewrite (BLOCKED on the author per ICASSP 2027 AI policy)
- Substantial prose must be authored by a human; assistant provides only
  `AUTHOR_REWRITE_PACKET.md` (factual bullets; no final prose).
- The working abstract is **223 words — over the 200-word hard form cap**;
  shorten to 120-150 words.
- Flagged terms requiring an author decision: "partially-specified MDP",
  "sufficient statistic", "near-optimal", "significant", "adaptation",
  "robust" (the "every few milliseconds" timing claim was removed).
- Three AUTHOR REVIEW REQUIRED items (see STATISTICAL_AUDIT.md):
  1. IFAC 3/4 vs Holm-corrected 2/4 capacities;
  2. SC-FAC switching: drops p=0.088; Money Holm p=0.069;
  3. k=24 set-vs-flat reading depends on one failed seed;
  plus weakening the avoidable-drop "exactly the failure mode" wording.

### B3 — Declarations (BLOCKED on the author)
- Final AI-use disclosure wording matching the live ICASSP 2027 policy;
- prior submission / preprint / dual-submission status and overlap with the
  prior manuscript;
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
- No GPU/scheduler blocker: no GPU work remains.
