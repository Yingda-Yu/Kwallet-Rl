# FINAL SUBMISSION GATE — ICASSP 2027

Freeze date: **2026-09-17**. Experiments, statistics, figures, tables, seeds,
protocol, training budget and test pools are **FROZEN**. Internal build
`submission_v1_internal.pdf` remains **INTERNAL / NOT FOR FINAL SUBMISSION**
and must not be uploaded. The real submission PDF is generated from `main.tex`
only AFTER the BLOCKED author metadata is supplied.

Only three states are used below: **READY** / **BLOCKED** /
**AUTHOR CONFIRMATION REQUIRED**.

## 1. Gate table (maps to the live ICASSP 2027 submission form)

| CMS field | State | Current value / note |
|---|---|---|
| Submission Title (ALL CAPS; must equal PDF exactly) | **READY** | AUDITING STRUCTURED POLICY LEARNING FOR STREAMING TRANSACTION COLLATERAL CONTROL: FACTORIZATION, CONDITIONING, AND CROSS-SCALE TRANSFER (verified all-caps and identical to rendered PDF) |
| Abstract (<=200 words) | **AUTHOR CONFIRMATION REQUIRED** | 150-word factual candidate (section 3); long working abstract still compiled in main.tex. Author must approve/rewrite; do not paste candidate unapproved. |
| Primary Topic | **READY** | 2.2 Reinforcement Learning [ML-REI] |
| Secondary Topic | **READY** | 2.7.5 Emerging Applications of ML [ML-APP-EMG] |
| Keywords (<=5; must equal PDF exactly) | **READY** | reinforcement learning; structured policies; resource allocation; permutation equivariance; online decision making (5; identical in main.tex/PDF) |
| Industry / Academia / Both | **AUTHOR CONFIRMATION REQUIRED** | author must select on the form |
| IEEE Privacy / Event Terms acknowledgement | **AUTHOR CONFIRMATION REQUIRED** | author must read and accept on the form (cannot be pre-accepted by assistant) |
| All authors | **BLOCKED** | only provisional "Yingda Yu"; full list missing |
| Author order | **BLOCKED** | unconfirmed |
| Affiliations (+department/city/country) | **BLOCKED** | PDF currently renders "Affiliation to be confirmed" (must be removed before upload) |
| Corresponding email | **BLOCKED** | none provided |
| ORCID for every author | **BLOCKED** | none provided |
| Funding / acknowledgments | **BLOCKED** | none provided (state grant(s) or explicitly "no funding") |
| Prior-submission / preprint / dual-submission status | **BLOCKED** | relation to old paper and any arXiv/venue history unconfirmed; must be declared |
| Final manuscript prose | **AUTHOR CONFIRMATION REQUIRED** | AI-assisted draft; author substantive rewrite per HUMAN_REWRITE_CHECKLIST.md |
| AI-use disclosure wording | **AUTHOR CONFIRMATION REQUIRED** | disclosure footnote present; final wording must match live ICASSP 2027 policy |
| Final PDF metadata + rebuild | **BLOCKED** | generated only after author fields are filled; placeholder text must be gone |
| Final upload approval | **AUTHOR CONFIRMATION REQUIRED** | explicit human authorization required; assistant will not submit |
| Experiments / statistics | **READY** | frozen at code SHA 4a2520f; matrix 60+76, ablation 12, kscale 18+36, switching 54+18; 0 missing/corrupt |
| Figures / tables | **READY** | 6 tables + 4 figures, all generated from CSVs; no hand-typed results |
| References | **READY** | 4 entries, all cited, verified; bibliography will not change |
| Internal QA build | **READY (internal only)** | submission_v1_internal.pdf QA-green but NOT for upload |

Summary: **READY** = title, primary topic, secondary topic, 5 keywords,
experiments/statistics, figures/tables, references, internal QA build.
**BLOCKED** = author list/order, affiliations, corresponding email, ORCID(s),
funding, prior/preprint/dual-submission status, final PDF metadata/rebuild.
**AUTHOR CONFIRMATION REQUIRED** = abstract, final prose, AI-use wording,
Industry/Academia/Both, IEEE Privacy/Event Terms, final upload approval.

## 2. PDF vs CMS consistency checks (re-run when the final PDF is built)
- [x] Title: all-caps in `main.tex` and identical to rendered PDF (verified).
- [x] Keywords: 5 in `main.tex` and rendered PDF (verified identical).
- [ ] Author order: identical between PDF and CMS — cannot verify until BLOCKED.
- [ ] Abstract: compiled PDF must equal the author-approved abstract — the
      candidate is NOT yet adopted into main.tex.
- [ ] PDF must contain NO "Affiliation to be confirmed" / "to be confirmed"
      placeholder (currently present x2 -> final PDF metadata BLOCKED).
- [ ] Final PDF rebuilt after metadata/prose changes; QA re-run;
      SUBMISSION_SNAPSHOT.md hashes refreshed.

## 3. Final fact audit of the 150-word abstract candidate (facts only)
Status **AUTHOR REVIEW REQUIRED**; **150 words** (form cap 200). The earlier
"SC-FAC beats IFAC at three capacities" reading stays eliminated: the sentence
now reads "both factorized policies beat the joint head -- the conditioned one
at all four capacities and the independent one at three of four".

| Sentence | Required evidence category | Source file | Verdict |
|---|---|---|---|
| S1 route/accept/drop + fixed-fee flush | environment/data | src/kwallet/envs/kwallet.py; main.tex "Model" | supported |
| S2 twelve regimes; three PPO policies; k-independent encoder | environment/data | src/kwallet/data/regimes.py; experiments/manifest_matrix_main.csv | supported |
| S3 both factorized > joint (conditioned 4/4, independent 3/4) | matrix_main paired stats | results/tables/matrix_main_paired.csv (SC-JA p=0.012/0.0067/<0.0001/0.0044; IFAC-JA p=0.00014/0.032/0.57/0.00093) | supported |
| S3 settle-conditioning adds no detectable gain (zero/shuffle) | conditioning ablation | results/tables/matrix_ablation_paired.csv (all CIs cross 0) | supported |
| S4 zero-shot cross-k; flat impossible; asymmetric; scale-specific cost | kscale / cross-k | results/tables/kscale_transfer_long.csv (off-diag retention; matched k6 +4%, k12 +6%, k24 -32%, 9190 vs 13610) | supported |
| S5 rule highest Money every capacity | BFP0.5 | results/tables/matrix_main_main_table.csv; matrix_main_paired.csv (11/12; exception vs IFAC C1000 p=0.057) | supported ("nearly every" matches 11/12) |
| S5 zero avoidable drops after abrupt regime shifts | switching | results/tables/switching_summary.csv (0.0 all 6; Money 15319); switching_paired_vs_bfp.csv | supported |
| S6 structure/portability synthesis; fill-feedback benchmark | all of the above | efficiency.tex (625->50 logits) + S3-S5 | supported; no overclaim |

No stronger-than-evidence claim remains (no SOTA; no RL OOD-superiority; no
conditioning benefit; no "rule significant vs every learned policy").

## 4. Author information template (fill one block per author; nothing guessed)
Send back the completed blocks; they will be entered into `main.tex` exactly
as provided. Do not leave any field blank — use "none" / "not applicable"
where true.

```
Author 1:
Full name:
Affiliation:
Department:
City/Country:
Email:
ORCID:
Corresponding author: Yes/No

Author 2:
Full name:
Affiliation:
Department:
City/Country:
Email:
ORCID:
Corresponding author: Yes/No

Author 3:
Full name:
Affiliation:
Department:
City/Country:
Email:
ORCID:
Corresponding author: Yes/No
```
(Add/delete blocks to match the final author count.)

Plus the single-value fields:
- Funding / acknowledgment statement (or "no funding"):
- Industry / Academia / Both:
- Prior-submission / preprint URL or DOI / dual-submission status:
- Final AI-use disclosure wording (or confirmation to use the current footnote):

## 5. Gate rule
No submission, no final submission PDF, and no upload occur until every
BLOCKED field is supplied and every AUTHOR CONFIRMATION REQUIRED item is
explicitly resolved by the human author. `submission_v1_internal.pdf` is never
uploaded. PR #2 stays draft; no merge into main.
