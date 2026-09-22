# FINAL SUBMISSION GATE — ICASSP 2027

Freeze date: **2026-09-17**. Experiments, statistics, figures, tables, seeds,
protocol, training budget and test pools are **FROZEN**. Internal build
`submission_v1_internal.pdf` remains **INTERNAL / NOT FOR FINAL SUBMISSION**
and must not be uploaded. The real submission PDF is generated from `main.tex`
only AFTER the remaining BLOCKED author metadata (email / ORCID / funding) is
supplied.

Only three states are used below: **READY** / **BLOCKED** /
**AUTHOR CONFIRMATION REQUIRED**.

## Finalization-pass update (2026-09-22)
- Author block CONFIRMED and written into `main.tex` (5 authors, fixed order,
  affiliations, corresponding author). The assistant did not modify `main.tex`
  in this metadata pass; author list / order / affiliations / corresponding are
  now READY. Contact email, ORCID, and funding remain BLOCKED.
- Fig.1/Fig.2 placeholders RESOLVED (real deterministic vector artwork; no
  raster; no generative images) -- not placeholders.
- References expanded 4 -> 16 verified primary sources; all cited.
- Statistical audit completed (`STATISTICAL_AUDIT.md`); Holm-corrected findings
  now reflected in `main.tex` (IFAC 3/4 raw -> 2/4 after Holm, C=900
  p_Holm=0.064; SC-FAC vs JA-PPO 4/4 raw, all 4 survive Holm; SC-FAC switching
  Money raw p=0.035, Holm p=0.069 -> NOT significant; k=24 9190 includes a
  failed seed, 13785 excluding vs 13610 flat -- a sensitivity finding).
  Overclaims removed: "partially-specified MDP", "near-optimal", "sufficient
  statistic", "causal value", "adapting without retraining", "deterministic
  code". The SC-FAC switching claim was corrected.
- Author guidance: `AUTHOR_REWRITE_PACKET.md` (no LLM final prose).
- PDF interim QA: 5 pages (tech 1-4, refs p.5); 0 undefined refs/cites;
  0 overfull boxes; all fonts embedded/subset; no Type 3; ~281 KB.
- Git divergence resolved (merged origin/main, no force push); PR #2
  mergeable/clean, still draft.
- Remaining gates: contact email / ORCID / funding (BLOCKED), human rewrite
  incl. the abstract (was 223 words; needs recounting after the Holm wording
  edits -- currently similar/slightly different), declarations, final QA.


## 1. Gate table (maps to the live ICASSP 2027 submission form)

| CMS field | State | Current value / note |
|---|---|---|
| Submission Title (ALL CAPS; must equal PDF exactly) | **READY** | AUDITING STRUCTURED POLICY LEARNING FOR STREAMING TRANSACTION COLLATERAL CONTROL: FACTORIZATION, CONDITIONING, AND CROSS-SCALE TRANSFER (verified all-caps and identical to rendered PDF) |
| Abstract (<=200 words) | **AUTHOR CONFIRMATION REQUIRED** | 150-word factual candidate (section 3); compiled working abstract was 223 words (over cap) and was edited for Holm-corrected wording -- word count needs rechecking after the edits. Author must shorten/approve/rewrite; do not paste candidate unapproved. |
| Primary Topic | **READY** | 2.2 Reinforcement Learning [ML-REI] |
| Secondary Topic | **READY** | 2.7.5 Emerging Applications of ML [ML-APP-EMG] |
| Keywords (<=5; must equal PDF exactly) | **READY** | reinforcement learning; structured policies; resource allocation; permutation equivariance; online decision making (5; identical in main.tex/PDF) |
| Industry / Academia / Both | **READY** | Academia (all authors academic; Wenzhou-Kean University, Northwestern University) |
| IEEE Privacy / Event Terms acknowledgement | **AUTHOR CONFIRMATION REQUIRED** | author must read and accept on the form (cannot be pre-accepted by assistant) |
| All authors | **READY** | 5 authors confirmed and written into main.tex: Yingda Yu, Sijia Zhou, Jiaqi Xuan, Zhentong Ye, Guanchao Tong (fixed order; do not change) |
| Author order | **READY** | confirmed order (Yu, Zhou, Xuan, Ye, Tong); do not change |
| Affiliations (+department/city/country) | **READY** | Wenzhou-Kean University (authors 1,2,3,5); Northwestern University (author 4); rendered in main.tex. Department / postal address NOT guessed (BLOCKED if the form requires them). |
| Corresponding author identity | **READY** | Guanchao Tong (author 5), marked * in main.tex |
| Corresponding email | **BLOCKED** | none provided (Guanchao Tong's contact email still missing) |
| ORCID for every author | **BLOCKED** | none provided for any of the 5 authors |
| Funding / acknowledgments | **BLOCKED** | none provided (state grant(s) or explicitly "no funding") |
| Prior-submission / preprint / dual-submission status | **BLOCKED** | relation to old paper and any arXiv/venue history unconfirmed; must be declared |
| Final manuscript prose | **AUTHOR CONFIRMATION REQUIRED** | AI-assisted draft; author substantive rewrite per HUMAN_REWRITE_CHECKLIST.md |
| AI-use disclosure wording | **AUTHOR CONFIRMATION REQUIRED** | disclosure footnote present in main.tex; final wording must match live ICASSP 2027 policy. Factual checklist in section 1a below; do NOT delete or understate. |
| Final PDF metadata + rebuild | **BLOCKED** | generated only after email/ORCID/funding fields are filled; placeholder text must be gone |
| Final upload approval | **AUTHOR CONFIRMATION REQUIRED** | explicit human authorization required; assistant will not submit |
| Experiments / statistics | **READY** | frozen at code SHA 4a2520f; matrix 60+76, ablation 12, kscale 18+36, switching 54+18; 0 missing/corrupt |
| Figures / tables | **READY** | 6 tables + 4 figures, all generated from CSVs; Fig.1/2 real vector artwork; no hand-typed results |
| References | **READY** | 16 entries (expanded from 4 in the 2026-09-22 citation audit); all cited; each verified via DOI / publisher / arXiv / proceedings page |
| Internal QA build | **READY (internal only)** | submission_v1_internal.pdf QA-green but NOT for upload |

Summary: **READY** = title, primary topic, secondary topic, 5 keywords,
author list, author order, affiliations, corresponding author identity,
Industry/Academia/Both (Academia), experiments/statistics, figures/tables,
references, internal QA build.
**BLOCKED** = corresponding email, ORCID(s), funding,
prior/preprint/dual-submission status, final PDF metadata/rebuild.
**AUTHOR CONFIRMATION REQUIRED** = abstract, final prose, AI-use wording,
IEEE Privacy/Event Terms, final upload approval.

## 1a. AI-use disclosure factual checklist (wording awaits author confirmation)
The `main.tex` `\thanks` footnote currently reads: "AI-assisted development
disclosure (AUTHOR CONFIRMATION REQUIRED): an AI coding assistant was used for
code development, visualization, and text drafting; quantitative results are
generated by released code with fixed seeds and fixed evaluation pools (pytest
37/37 passing; all claims traced to source CSVs); the manuscript prose requires
substantive human rewrite and author approval before submission. Final
disclosure wording awaits author confirmation. Author contact, ORCID, and
funding remain to be filled."

Factual basis (do NOT delete or understate; do NOT decide final wording):
- AI used for code development: **yes**
- AI used for visualization: **yes**
- AI used for drafting/editing text: **yes**
- code subsequently tested: **yes**, pytest 37/37 passing
- quantitative claims traced to source CSVs: **yes**
- final manuscript sections must receive substantive human rewrite: **PENDING**

## 2. PDF vs CMS consistency checks (re-run when the final PDF is built)
- [x] Title: all-caps in `main.tex` and identical to rendered PDF (verified).
- [x] Keywords: 5 in `main.tex` and rendered PDF (verified identical).
- [x] Author order: 5 authors written into `main.tex` in the confirmed order
      (Yu, Zhou, Xuan, Ye, Tong); must match the CMS entry at upload time.
- [ ] Abstract: compiled PDF must equal the author-approved abstract -- the
      candidate is NOT yet adopted into main.tex; word count needs rechecking
      after the Holm wording edits (was 223; should be similar/slightly
      different now).
- [x] PDF contains NO "Affiliation to be confirmed" / "to be confirmed"
      placeholder (author block is now real in main.tex).
- [ ] Final PDF rebuilt after email/ORCID/funding + prose changes; QA re-run;
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

## 4. Author information (confirmed; email/ORCID/funding still BLOCKED)
Author list, order, affiliations, and corresponding author are CONFIRMED and
written into `main.tex`. The remaining fields below must be supplied by the
authors (do not guess). IEEE member grade, department, and postal address are
NOT filled here -- the author must provide them if the live form requires them.

| # | Full name | Affiliation | Corresponding | Email | ORCID |
|---|-----------|-------------|---------------|-------|-------|
| 1 | Yingda Yu | Wenzhou-Kean University | No | **BLOCKED** | **BLOCKED** |
| 2 | Sijia Zhou | Wenzhou-Kean University | No | **BLOCKED** | **BLOCKED** |
| 3 | Jiaqi Xuan | Wenzhou-Kean University | No | **BLOCKED** | **BLOCKED** |
| 4 | Zhentong Ye | Northwestern University | No | **BLOCKED** | **BLOCKED** |
| 5 | Guanchao Tong | Wenzhou-Kean University | Yes (*) | **BLOCKED** | **BLOCKED** |

Plus the single-value fields (still BLOCKED unless noted):
- Funding / acknowledgment statement (or "no funding"): **BLOCKED**
- Industry / Academia / Both: **Academia (READY)**
- Prior-submission / preprint URL or DOI / dual-submission status: **BLOCKED**
- Final AI-use disclosure wording (or confirmation to use the current
  footnote): **AUTHOR CONFIRMATION REQUIRED** (see section 1a checklist)
- IEEE member grade / department / postal address: NOT guessed -- author
  supplies if the form requires them.

## 5. Gate rule
No submission, no final submission PDF, and no upload occur until every
BLOCKED field is supplied and every AUTHOR CONFIRMATION REQUIRED item is
explicitly resolved by the human author. `submission_v1_internal.pdf` is never
uploaded. PR #2 stays draft; no merge into main.

## 6. Figure placeholders that MUST become real artwork before upload
The narrative-expansion pass (2026-09-20) reserves positions with compilable
framed placeholders. They render as boxes labelled "Figure placeholder" and are
NOT final figures; the final PDF must not contain them.
- **Fig. 1 (`fig:overview`)** -- problem/environment overview: transaction
  stream, k wallets, settle vs.\ flush, objective/drop intuition.
- **Fig. 2 (`fig:structures`)** -- policy-structure comparison: JA-PPO joint
  $(k{+}1)^2$ head; IFAC independent heads; SC-FAC settle-conditioned edge;
  Set shared equivariant encoder; annotate 625 vs.\ 50 outputs.
Already real (generated from results): Fig. 3 `fig:cap` (capacity_curve.pdf),
Fig. 4 `fig:heat` (transfer_set_sc_fac.pdf). Note: output_scaling.pdf and
switching_drops.pdf remain committed assets but are no longer floated (their
content is covered by Table 1 / Table 5); re-floating either is optional.
Status of these two placeholders: **RESOLVED (2026-09-22)** -- both are now
real deterministic vector artwork generated by `scripts/make_concept_figures.py`
(`overview.pdf`, `structures.pdf`; matplotlib-only, pdf.fonttype=42, no raster,
no new results); `pdftotext main.pdf - | grep -i "figure placeholder"` is empty.
The author should still visually confirm both figures.
