# SUBMISSION V1 CHECKLIST — ICASSP 2027

Freeze date: **2026-09-16**. Experiments are FROZEN (no retraining, no seed
re-selection, no evaluation-protocol change). Internal QA PDF:
`submission_v1_internal.pdf` — **INTERNAL / NOT FOR FINAL SUBMISSION**.

## A. Submission-system fields (fill these in the portal)

| # | Field | Status | Value / note |
|---|-------|--------|--------------|
| 1 | Title | **READY** (author-confirmed) | Auditing Structured Policy Learning for Streaming Transaction Collateral Control: Factorization, Conditioning, and Cross-Scale Transfer |
| 2 | Primary topic | **READY** (author-confirmed) | 2.2 Reinforcement Learning [ML-REI] |
| 3 | Secondary topic | **READY** (author-confirmed) | 2.7.5 Emerging Applications of Machine Learning [ML-APP-EMG] |
| 4 | Abstract | **BLOCKED** — AUTHOR REVIEW REQUIRED | 150-word factual candidate in SUBMISSION_FORM_CONTENT.md §3a; long working abstract still compiled in main.tex. Author must approve/re-write in own words. |
| 5 | Keywords (exactly 5) | **READY** (author-confirmed, applied in main.tex) | reinforcement learning; structured policies; resource allocation; permutation equivariance; online decision making |
| 6 | Author order / full list | **BLOCKED** | Only provisional "Yingda Yu"; list/order unconfirmed |
| 7 | Affiliations + addresses | **BLOCKED** | main.tex shows "Affiliation to be confirmed" |
| 8 | Corresponding email | **BLOCKED** | none provided |
| 9 | ORCID for every author | **BLOCKED** | none provided |
| 10 | Funding / acknowledgments | **BLOCKED** | none provided (author must state grant(s) or explicitly "no funding") |
| 11 | Prior submission / dual-submission / arXiv status | **BLOCKED** | unconfirmed; relation to old paper must be declared |
| 12 | Paper type / presentation / student-paper / AI declaration | **BLOCKED** | regular paper proposed; AI-disclosure wording exists but final wording unconfirmed |
| 13 | PDF upload | **BLOCKED — DO NOT UPLOAD YET** | upload only a rebuilt main.pdf after fields 4,6-12 are resolved; do not upload submission_v1_internal.pdf |

**Ready: 5 fields (1,2,3,5 + frozen science/package). Blocked: 8 entries.**

## B. 150-word abstract candidate — fact check (2026-09-16)

Status: **AUTHOR REVIEW REQUIRED** (not final, not pasted into main.tex).
Word count: **150** (hyphenated terms counted as one word; form cap 200,
Paper Kit target 100-150).

One correction made during this fact check: an earlier draft read "...the
conditioned factored policy beats the joint head at all four capacities **and
the independent factored policy at three**", which is parseable as SC-FAC >
IFAC at three capacities. The data show SC-FAC beats IFAC only at C=1000
(7680 vs 6952) and is lower at C=800/900/1200. The candidate now reads "both
factorized policies beat the joint head -- the conditioned one at all four
capacities and the independent one at three of four".

Per-sentence evidence map:

| Sentence | Claim | Evidence source | Supported? |
|---|---|---|---|
| S1 | Route/accept/drop + fixed-fee flush model | src/kwallet/envs/kwallet.py; main.tex §Model | Yes |
| S2 | 12 regimes; 3 PPO policies; equivariant k-independent encoder | src/kwallet/data/regimes.py; experiments/manifest_matrix_main.csv; runs/kscale; main.tex §Policies | Yes |
| S3 | Both factorized > joint; conditioned 4/4, independent 3/4; conditioning null | results/tables/matrix_main_paired.csv (SC-JA p 0.012/0.0067/<0.0001/0.0044; IFAC-JA p 0.00014/0.032/0.57/0.00093); matrix_ablation_paired.csv (all CIs cross 0) | Yes (after correction) |
| S4 | Zero-shot cross-k; flat impossible; asymmetric; scale-specific matched-k cost | results/tables/kscale_transfer_long.csv (off-diagonal retention; matched k6 +4%, k12 +6%, k24 -32% 9190 vs 13610) | Yes |
| S5 | Rule highest Money every C; 0 avoidable drops after shifts; beats learning in nearly every paired comparison | matrix_main_main_table.csv; switching_summary.csv (0.0; 15319); matrix_main_paired.csv (11/12; exception BFP0.5-IFAC C1000 p=0.057) | Yes ("nearly every" matches 11/12) |
| S6 | Factorization/equivariance improve structure/portability; fill-feedback rule is benchmark | efficiency.tex (625->50 logits); S3-S5 evidence | Yes (synthesis, no stronger-than-data claim) |

Stronger-than-evidence claims remaining: **none**. Explicitly absent: no
"state-of-the-art", no "adaptive/robust to OOD" superiority for RL, no claim
conditioning helps, no claim BFP0.5 is significant against every learned
policy.

## C. Science/package readiness (frozen)
- matrix_main 60/60 train + 76/76 eval; ablation 12/12; kscale 18/18 + 36;
  switching 54/54 learned + 18 rule rows (bitwise-identical deterministic
  streams). 0 missing/duplicate/corrupt.
- All numbers traceable via assets/paper_claims.json -> source CSVs; old-paper
  values only in separate REPORTED_ONLY ("paper rep.") column.
- QA on internal PDF: pytest 37/37; clean build rc=0; 4 pages (tech 1-3,
  refs p4); 0 overfull/undefined/pending; all fonts embedded; per-page visual
  check passed; 4 references, all cited.

## D. Gate
**DO NOT SUBMIT** until rows 4, 6-12 are resolved by the author and the PDF is
rebuilt from the finalized source; then re-run QA and refresh
SUBMISSION_SNAPSHOT.md hashes.
