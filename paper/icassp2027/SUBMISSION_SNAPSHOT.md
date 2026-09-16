# Submission Snapshot — ICASSP 2027 manuscript

Snapshot date: **2026-09-16**
Status: **INTERNAL AI-ASSISTED DRAFT — NOT READY TO SUBMIT** (author metadata
and author prose rewrite are blockers). Experiments/statistics are frozen.

---
## V1 FREEZE ADDENDUM (2026-09-16)
- Title, primary/secondary topics, and the 5 keywords are **AUTHOR-CONFIRMED**
  and applied in main.tex (removed from the blocker list).
- Internal frozen QA PDF: `paper/icassp2027/submission_v1_internal.pdf`,
  byte-identical to main.pdf at freeze time
  (SHA256 `923e23c60388b3e1fcc07ae4d1ce91795652a8a1c95d732cd0ea96f07e9f6d35`),
  marked INTERNAL / NOT FOR FINAL SUBMISSION (see SUBMISSION_V1_INTERNAL.txt).
- 150-word abstract candidate fact-checked (one ambiguous sentence corrected;
  see SUBMISSION_V1_CHECKLIST.md section B); remains AUTHOR REVIEW REQUIRED.
- Field-by-field READY/BLOCKED state: SUBMISSION_V1_CHECKLIST.md.
- Bibliography re-verified: 4 entries, all cited; no padding references added.
- AGENTS.md add/add conflict: resolution proposal only, at
  docs/AGENTS_MERGE_PROPOSAL.md (no merge performed).

## 1. Code / experiment lineage
- Frozen experiment + aggregation + statistics code SHA: **`4a2520f`**
  (`4a2520ff291ad6070050fd7e6767b6084f162dab`) on branch
  `work/icassp2027-reproduce-improve`. This is the code state that produced
  every number below. Later packaging commits change only manuscript prose /
  metadata / docs, never result CSVs.
- Experiments (NOT re-run for this snapshot): matrix_main 60/60 train +
  76/76 eval; matrix_ablation 12/12; kscale 18/18 + 36 cross-k; switching
  54/54 learned + 18 rule rows on bitwise-identical deterministic streams.
- Machine-readable hash manifest: `results/tables/SUBMISSION_ARTIFACT_SHA256.json`.

## 2. Manuscript artifact
| Item | Value |
|---|---|
| PDF path | `paper/icassp2027/main.pdf` |
| PDF SHA256 | `923e23c60388b3e1fcc07ae4d1ce91795652a8a1c95d732cd0ea96f07e9f6d35` |
| PDF bytes | 235,998 (≈232 KB) |
| Pages | 4 (technical pp.1-3; references-only p.4) |
| paper_claims.json SHA256 | `8b5d8968f313ab35cf3fd581c164fbdabfa332434eb43f6b38f5fd4d41a53f62` |
| Keywords | exactly 5 (see SUBMISSION_FORM_CONTENT.md) |
| Current abstract | ~196-218 words (long, in main.tex); 149-word author-review candidate in SUBMISSION_FORM_CONTENT.md |

## 3. Frozen result hashes (SHA256)
| Artifact | File | SHA256 (prefix) |
|---|---|---|
| Main Money table | results/tables/matrix_main_main_table.csv | `b2c60f7a…1c0cb666` |
| Main per-episode long | results/tables/matrix_main_main_long.csv | `fd168014…238e4c276` |
| Paired contrasts | results/tables/matrix_main_paired.csv | `37a2c3da…288f8a1d1` |
| tau post-hoc | results/tables/matrix_main_tau_posthoc.csv | `f55b75aa…2eec0a46` |
| Ablation table | results/tables/matrix_ablation_main_table.csv | `98abc428…f5d7df04` |
| Ablation paired | results/tables/matrix_ablation_paired.csv | `64e5b4fb…a636227cb` |
| Cross-k long | results/tables/kscale_transfer_long.csv | `043abd6d…a74ff6532a` |
| Switching summary | results/tables/switching_summary.csv | `7e033b9c…28e17512d` |
| Switching paired vs BFP0.5 | results/tables/switching_paired_vs_bfp.csv | `3cea31e6…681e4a75` |
| Efficiency bench | runs/bench/bench_C1200.0_k24.csv | `01c54494…276aeed60` |

Full digests are in `results/tables/SUBMISSION_ARTIFACT_SHA256.json`.

## 4. Build / reproduction commands (no retraining)
```
conda activate kwallet
python -m pytest -q                                   # 37 passed
python scripts/aggregate_results.py --exp matrix_main
python scripts/aggregate_results.py --exp matrix_ablation
python scripts/aggregate_kscale.py --exp kscale
python scripts/paired_stats.py --exp matrix_main --tex paired.tex
python scripts/paired_stats.py --exp matrix_ablation \
    --ref-long results/tables/matrix_main_main_long.csv --tex paired_ablation.tex
python scripts/make_paper_assets.py --exp matrix_main \
    --ablation matrix_ablation --kscale kscale       # writes assets/, paper_claims.json
cd paper/icassp2027
pdflatex -interaction=nonstopmode main.tex; bibtex main
pdflatex -interaction=nonstopmode main.tex; pdflatex -interaction=nonstopmode main.tex
pdfinfo main.pdf; pdffonts main.pdf; pdftoppm -png -r 100 main.pdf render/page
```
Rebuilding from `4a2520f` regenerates the same CSVs/assets; if the PDF SHA
changes after an author edit, regenerate this snapshot and bump the packaging
commit, so the submitted PDF is always traceable to one code SHA.

## 5. Claim-by-claim evidence audit (2026-09-16)
All quantitative wording in main.tex was checked against the CSVs /
paper_claims.json. Outcomes:

| # | Claim in prose | Evidence (file) | Verdict |
|---|---|---|---|
| 1 | SC-FAC significantly beats JA-PPO at ALL four capacities | matrix_main_paired.csv p=0.012(C800),0.0067(C900),<0.0001(C1000),0.0044(C1200); wins 5/5 | OK |
| 2 | IFAC beats JA-PPO at C=800/900/1200, NOT C=1000 | paired p=0.00014/0.032/0.00093; C1000 p=0.569 | OK (wording fixed) |
| 3 | SC-FAC vs IFAC: null at C=900/1000/1200; significantly LOWER at C=800 | paired: CIs cross 0 at 900/1000/1200; C800 -419, p=0.009 | OK (wording fixed) |
| 4 | BFP0.5 highest Money at every C | matrix_main_main_table.csv (4682/7027/9497/15327) | OK |
| 5 | BFP0.5 significant in 11/12 learned contrasts; exception vs IFAC C1000 | paired: BFP0.5-IFAC C1000 +2545 p=0.057 (5/5 wins); other 11 p<0.05 | OK (wording fixed; contrasts added) |
| 6 | Conditioning not a positive contribution; zero/shuffle ablations indistinguishable | matrix_ablation_paired.csv: all 4 CIs cross 0 | OK |
| 7 | Oversize-drop structural floor ~400/episode for every method | runs/matrix_main/eval_*.csv drop_oversize=400.3 all methods | OK |
| 8 | Set encoder zero-shot cross-k; flat has no off-diagonal | kscale_transfer_long.csv (27 set off-diag, flat diag-only) | OK |
| 9 | Cross-k transfer asymmetric | kscale retention: k6->k24=4433 weak; k24/12->k6 >100% strong | OK |
| 10 | Matched-k cost | set vs flat: k6 46742/44820 (+4%), k12 36391/34193 (+6%), k24 9190/13610 (-32%) | OK ("modest at all k" removed; now stated scale-specific at k24) |
| 11 | BFP0.5 zero post-switch avoidable drops on all 6 scenarios; highest switching Money | switching_summary.csv (0.0; 15319) | OK |
| 12 | Learned post-switch drops 28-56 vs naive rules 144-148 | switching_summary.csv | OK |
| 13 | Learned significantly worse than BFP0.5 on drops & Money (p<0.01, n=3) | switching_paired_vs_bfp.csv (drops p 0.0013/0.0031/0.0014; money <0.0001) | OK |
| 14 | IFAC/SC-FAC essentially identical post-switch drops (28.3) | switching_summary.csv 28.31/28.29 | OK ("tied" made precise) |
| 15 | No RL adaptation advantage over BFP0.5 after shifts | items 11-13 | OK (explicit honest negative) |
| 16 | Outputs (k+1)^2=625 vs 2(k+1)=50 at k=24 | bench + output_scaling; efficiency.tex | OK |
| 17 | Factorization reduces action head to linear factorized heads | efficiency.tex JA 625 logits; IFAC/SC 50 | OK |

No claim in the manuscript contradicts the frozen results. Old-paper Table II
values appear only in the separate "paper rep." column (REPORTED_ONLY).

## 6. Automated QA (this snapshot)
- pytest: **37 passed**.
- Clean TeX build: rc=0; bibtex 0 errors/0 warnings; 4 references, all cited.
- Pages **4**; references-only page confirmed (p.4); technical content on pp.1-3.
- Overfull hbox **0**; undefined refs/citations **0**; rendered "pending"/"placeholder" **0**.
- Fonts: **all embedded** (pdffonts emb=yes for every font).
- All 6 generated tables and 4 figures present and loaded (no fallback boxes).
- Per-page renders in paper/icassp2027/render/page-{1..4}.png visually checked.

## 7. Submission blockers (must be resolved by the human author)
Resolved (2026-09-16): title; primary 2.2 ML-REI / secondary 2.7.5 ML-APP-EMG;
five keywords. Remaining:
1. Real author list/order, affiliations, corresponding email, ORCID(s), funding.
   Currently `main.tex` shows "Yingda Yu" (repo owner; provisional) and
   "Affiliation to be confirmed" — intentional placeholders, not submittable.
2. Author substantive prose rewrite (HUMAN_REWRITE_CHECKLIST.md) and approval
   of the final abstract (~100-150 words; 150-word candidate fact-checked).
3. Final AI-use disclosure wording matching the live ICASSP 2027 policy.
4. Prior manuscript / dual-submission / arXiv status confirmation; paper type /
   presentation / student-paper form options.
5. After all of the above: rebuild the submission PDF, re-run this QA, and
   regenerate the snapshot hashes. Do not upload submission_v1_internal.pdf.

**Do not submit until items 1-4 are complete and the author explicitly authorizes it.**
