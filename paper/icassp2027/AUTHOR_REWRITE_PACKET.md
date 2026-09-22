# Author Rewrite Packet — ICASSP 2027 manuscript (per-section execution table)

Updated: 2026-09-22 (Phase 4 of the FINAL AUTHOR + CLAIM HARDENING PASS).
File: `paper/icassp2027/main.tex`.

## Purpose and rules

ICASSP 2027 policy does not permit an LLM to generate substantial manuscript
components. This packet contains **no paste-ready sentences**. For each section
it provides a structured table with columns:

- **A.** Current paragraph location (line numbers in main.tex)
- **B.** Factual claims that must be preserved
- **C.** Exact data (immutable — from source CSVs, not hand-typed)
- **D.** Required citations
- **E.** Overclaims already corrected in this pass (do not reintroduce)
- **F.** Statistical wording requirement
- **G.** Author rewrite goal
- **H.** Word/line budget

After rewriting a section, rebuild and verify: no number may change unless the
author also updates the matching CSV provenance.

**Space budget: ZERO slack.** Technical content fills 4 pages; page 5 holds
references only (16 entries). Replacement text must be same length or shorter.

**Abstract: 232 words currently. Hard form cap = 200. Paper-kit target ≈
125–150. Author must cut ≥32 words (submittable) or ~80 words (on-target).**

**Confirmed authors (do not change order):**
Yingda Yu¹, Sijia Zhou¹, Jiaqi Xuan¹, Zhentong Ye², Guanchao Tong^{1,*}
¹Wenzhou-Kean University  ²Northwestern University  *Corresponding author

**Still BLOCKED (author must provide):** email, ORCID, funding,
prior-submission/preprint status, final AI-disclosure wording, final prose approval.

---

## 1. Abstract (lines 56–81)

| Col | Content |
|-----|---------|
| A | Lines 56–81; sits between `\maketitle` and `\begin{keywords}` |
| B | (i) k wallets, flush at fixed fee, online decision problem, 12 regimes; (ii) port env + 3 PPO policies; (iii) SC-FAC beats JA-PPO 4/4, IFAC 3/4 raw (2/4 Holm); (iv) conditioning path null; (v) equivariant encoder zero-shot cross-k; (vi) BFP0.5 highest Money, zero avoidable drops; (vii) wallet fill captures decision-relevant info; (viii) released code, fixed seeds, fixed eval pools |
| C | SC-FAC vs JA-PPO: 4/4 raw, all survive Holm. IFAC vs JA-PPO: 3/4 raw (C=800,900,1200), 2/4 Holm (C=900 p_Holm=0.064). BFP0.5: 11/12 significant. k=24: 9190 incl failed seed, 13785 excl vs 13610 flat |
| D | No citations in abstract (ICASSP convention) |
| E | Removed: "partially-specified Markov decision process" → "online decision problem"; "significantly beats" → "beats" (test details in body); "trails a size-matched flat network" → "no clear matched-scale advantage"; "sufficient statistic" → "captures much of the decision-relevant information"; "deterministic code" → "code with fixed seeds and fixed evaluation pools"; "flat MLP cannot" → "fixed-shape flat MLP cannot reuse its weights" |
| F | "three of four (two of four after Holm correction)" — must keep both raw and Holm numbers; do not write "significant" without qualifier since abstract has no room for test details |
| G | Compress to 125–150 words while keeping: task, 3 results (factorization, conditioning null, encoder), BFP0.5 finding, provenance. Author decides emphasis. |
| H | Current 232 words → target 125–150. Hard max 200. |

---

## 2. Introduction ¶1 — background (lines 86–109)

| Col | Content |
|-----|---------|
| A | Lines 86–109; first paragraph after `\section{Introduction}` |
| B | Transactions arrive sequentially with value x_t; settle into k wallets or drop; independently flush one wallet at fixed fee with cooldown; C partitioned per wallet; sequential trade-off (flush costs now, frees capacity later) |
| C | k=24, C∈{800,900,1000,1200}, T=1000, x_t∈[0,1000] (details in Model section) |
| D | poon2016lightning, miller2019sprites, kolachala2024sok (Lightning/background); sivaraman2020spider (routing); borodin1998online (online analysis); lykouris2018competitive (learning-augmented); almashaqbeh2024competitive (closest formal model); lin2019competitive (inventory) |
| E | "Every few milliseconds" removed (no source). Do not call the prior unpublished manuscript a published reference. State relationship to Almashaqbeh as "closest formal model". |
| F | No statistical claims in this paragraph |
| G | Keep background concise; author may tighten prose. Do not add timing/frequency claims without source. |
| H | ~25 lines; can be tightened by 3–5 lines if space needed elsewhere |

---

## 3. Introduction ¶2 — why factorize (lines 111–124)

| Col | Content |
|-----|---------|
| A | Lines 111–124 |
| B | Joint head (k+1)²=625 at k=24; factored 2(k+1)=50; conditioning question settle→flush posed as hypothesis |
| C | 625, 50 (exact) |
| D | tavakoli2018action (branching) |
| E | "squandering samples" removed (sample-efficiency unverified). Do not add sample-complexity claims. |
| F | No statistical claims |
| G | Keep the hypothesis framing; author may condense |
| H | ~14 lines |

---

## 4. Introduction ¶3 — set encoder (lines 126–133)

| Col | Content |
|-----|---------|
| A | Lines 126–133 |
| B | Flat MLP bakes k into weight shapes; shared permutation-equivariant function removes k-dependent params; zero-shot deployment; cost-at-original-scale is open question |
| C | No specific numbers in this paragraph |
| D | (Deep Sets citation is in Contributions item 2, line 162) |
| E | Avoid claiming equivariance improves same-k accuracy (paper finds it does not). Line 131 "a model trained at one k cannot even be loaded at another" — accurate for standard flat MLP; acceptable but author may soften. |
| F | No statistical claims |
| G | Author may condense |
| H | ~8 lines |

---

## 5. Introduction ¶4 — strong baseline / audit framing (lines 135–151)

| Col | Content |
|-----|---------|
| A | Lines 135–151 |
| B | Prior manuscript baselines are simple (flush-all, flush-full); BFP0.5 selected on validation; audit framing: which structural biases help? |
| C | No specific numbers |
| D | (No new citations needed here) |
| E | "Prior comparisons use only trivial rules, which a learner beats easily" removed (comparative ease unsupported). "faithful port ... twelve regimes" qualified: faithful port of env; hyperparameters are documented re-implementations. |
| F | No statistical claims in prose; "null results as prominently as positive ones" is a reporting principle, not a test |
| G | Keep audit framing; author may tighten |
| H | ~17 lines |

---

## 6. Contributions list (lines 152–174)

| Col | Content |
|-----|---------|
| A | Lines 152–174; four `\item` entries |
| B | (1) Re-implementation of env + 3 PPO policies (JA-PPO, IFAC, SC-FAC); (2) permutation-equivariant set encoder; (3) mechanism ablations (null result); (4) strong baseline BFP0.5 |
| C | JA (k+1)²=625; IFAC/SC 2(k+1)=50; tau=10 (tested flush price) |
| D | zaheer2017deepsets (Deep Sets) |
| E | Item 1: "documented re-implementation" qualifier kept. Item 3: "at the tested flush price" kept. Item 4: "robust to regime shifts" → "maintains this across the tested regime shifts" (robust is a flagged term). |
| F | Item 4: "beating the learned policies in nearly all paired comparisons" — 11/12, accurate with "nearly all" |
| G | Author may condense items; keep the four-structure. Do not add "robust" back. |
| H | ~23 lines; can save 2–3 lines by tightening |

---

## 7. Streaming collateral control — Model + Objective + Data (lines 176–211)

| Col | Content |
|-----|---------|
| A | Lines 176–211 (Model ¶176–188; Objective ¶190–199; Data ¶201–211) |
| B | C∈{800,900,1000,1200}; k=24; T=1000; x_t∈[0,1000]; a_s,a_f∈[0,k]; flush FIRST then settle; F=3 cooldown; capacity C/k; obs 3k+2; Money M = p·Σaccepted_x − τ·#flushes, p=1, τ=10; 12 regimes; 5000 train / 300 val / 200 test per regime; deterministic argmax eval; failed seeds retained |
| C | All numbers above are immutable from source CSVs/configs |
| D | schulman2017ppo (PPO), schulman2015gae (GAE) |
| E | "partially-specified MDP" → "online decision problem" (already in abstract). "paired at episode level" → "share identical evaluation inputs; statistical unit = matched training seed (n=5 main; n=3 ablation/switching), not ≈2400 test episodes" — MUST keep this distinction. Drop taxonomy stated as accounting convention, not causal decomposition. Must mention: fixed C + changing k changes both C/k and oversized fraction. |
| F | Data section MUST state statistical unit = training seed; episode-level pairing = identical evaluation inputs only |
| G | Author verifies all numbers; may add the fixed-C-changing-k caveat if space allows |
| H | ~36 lines; dense but all necessary |

---

## 8. Policies (lines 217–267)

| Col | Content |
|-----|---------|
| A | Lines 217–267 (JA-PPO ¶217–225; IFAC ¶227–232; SC-FAC ¶234–248; Set encoder ¶250–258) |
| B | JA (k+1)²=625; IFAC/SC 50 logits; IFAC π(a_s,a_f\|s)=π_s·π_f; SC-FAC π_f(a_f\|s,a_s); ablations: no-cond zeroes embedding, shuffled feeds deranged embedding; set encoder: shared φ + pooling + per-wallet logits; permutation-equivariant by construction (unit-tested); k-independence; settle-conditioned set variant |
| C | 625, 50 (exact); verified by unit tests |
| D | dulac2015deep (large-action embeddings), hausknecht2016deep (parameterized actions), tavakoli2018action (branching), akkerman2024dynamic (neighborhood) |
| E | "causal value" → "mechanistic value" (§SC-FAC ¶, line 248; and section heading line 353). "a flat MLP cannot" already qualified with "(its weight shapes change with k)" in contributions; in Set encoder ¶, "a flat network lacks" is contextually specific. |
| F | "isolates whether the information path carries any mechanistic value" — mechanism ablation, NOT causal identification |
| G | Author verifies; may condense IFAC/SC-FAC descriptions |
| H | ~50 lines; can save 3–5 lines |

---

## 9. Experiments — Stationary performance (lines 297–323)

| Col | Content |
|-----|---------|
| A | Lines 297–323 |
| B | Factorization helps: SC-FAC > JA-PPO 4/4 (p≤0.013, 5/5 seeds, all survive Holm); IFAC > JA-PPO at C∈{800,900,1200} (p≤0.033) not C=1000 (p=0.57); Holm: IFAC survives C∈{800,1200}, C=900 p_Holm=0.064 does NOT survive. Mechanism consistent with: drops 77→49.5→40.4. Conditioning null: SC-FAC−IFAC CI includes zero at 3/4; C=800 SC-FAC lower (−419, p=0.009). BFP0.5: highest Money every C, zero avoidable drops, 11/12 significant (exception: vs IFAC C=1000 +2545 p=0.057, 5/5 wins). |
| C | All p-values, CIs, drop counts from matrix_main_paired.csv and seed-level data. p<0.001 formatting in paired.tex. |
| D | No new citations needed |
| E | "Two robust effects" → "Two effects" (robust flagged). "mechanism interpretation is direct" → "consistent with". "exactly the failure mode" → "the failure mode ... are expected to reduce". "near-optimal" → "highest observed Money among all evaluated methods". Holm correction now explicit for IFAC. |
| F | MUST distinguish raw vs Holm for IFAC. MUST keep "consistent with" not "direct/exactly" for drop mechanism. BFP0.5 "highest observed Money" not "near-optimal". |
| G | Author verifies; may condense Holm detail if abstract carries it |
| H | ~27 lines |

---

## 10. Experiments — Settle-conditioning ablation (lines 353–361)

| Col | Content |
|-----|---------|
| A | Lines 353–361 |
| B | No-conditioning and shuffled-conditioning both indistinguishable from SC-FAC (all CIs include zero); at C=1200 conditioned variant nominally lowest. Correct-but-useless wiring = evidence that settle-wallet identity is not decision-relevant at τ=10. |
| C | Raw p range 0.27–0.65; Holm-adjusted all 1.0. From matrix_ablation_paired.csv. |
| D | No new citations |
| E | "causal value" → "mechanistic value" in heading |
| F | Null result; no positive claim. "mechanism ablation" not "causal identification". |
| G | Author verifies; keep as honest null |
| H | ~9 lines |

---

## 11. Experiments — Cross-k transfer (lines 371–385)

| Col | Content |
|-----|---------|
| A | Lines 371–385 |
| B | Set encoder loads/runs at every deployment k; flat policies have no off-diagonal entry. Transfer asymmetric (strong → larger wallets/smaller k; weak k=6→24 yields 4433). At matched k=24: 9190 all-seed aggregate SENSITIVE to one failed seed (Money=0); excluding it 13785 vs flat 13610 (n=3) → no clear matched-k deficit. Structural portability holds; matched-scale cost is failed-seed sensitivity. |
| C | 4433 (k=6→24); 9190 (k=24 diag, incl failed); 13785 (excl failed); 13610 (flat, n=3). 18 off-diagonal deployments, 16 execute. From kscale_transfer_long.csv. |
| D | No new citations |
| E | "lower at k=24 (9190 vs 13610): portability comes with a scale-specific accuracy trade-off" → rewritten as failed-seed sensitivity. Do NOT write "clear matched-k cost" — it depends on one failed seed. |
| F | Fixed C + changing k changes both C/k and oversize difficulty (must be noted somewhere). Off-diagonal cells are zero-shot deployment evidence, NOT fair matched-task accuracy benchmark. |
| G | Author verifies; keep sensitivity framing |
| H | ~15 lines |

---

## 12. Experiments — Switching streams (lines 395–414)

| Col | Content |
|-----|---------|
| A | Lines 395–414 |
| B | Six switch scenarios (calm→burst, burst→calm, early/late). BFP0.5: zero avoidable drops after every switch, highest Money, maintains performance without retraining (current fill captures decision-relevant info). Learned: 28–56 vs 144–148 post-switch drops (vs naive rules). JA-PPO/IFAC worse on both drops+Money (n=3, p<0.01). SC-FAC: drops p≈0.09, Money raw p=0.035 → Holm p=0.069 NOT significant. |
| C | All from switching_paired_vs_bfp.csv and seed-level switching data. n=3 (ablation/switching). |
| D | gama2014survey (concept drift / six scenarios) |
| E | "adapting without retraining" → "maintaining its observed performance without retraining". "sufficient statistic" → "captures much of the decision-relevant information". "robust enough not to collapse" → "do not collapse". |
| F | MUST NOT write "significantly worse than BFP0.5 under all switching settings" for SC-FAC (Holm fails). JA-PPO/IFAC p<0.01 survive Holm (0.013). SC-FAC Money Holm p=0.069. |
| G | Author verifies; keep the Holm distinction for SC-FAC |
| H | ~20 lines |

---

## 13. Experiments — Parameter/output efficiency (lines 425–434)

| Col | Content |
|-----|---------|
| A | Lines 425–434 |
| B | Joint→factorized cuts outputs 625→50; actor 245874→98099 params (IFAC); set variants 135k params, no k-dependent tensor, sub-ms CPU latency. |
| C | 625, 50, 245874, 98099, 135k. From efficiency.tex / model configs. |
| D | No new citations |
| E | "statistically stronger than the joint head on most capacities" — 3/4 raw (2/4 Holm) for IFAC; 4/4 for SC-FAC. "most" is acceptable for SC-FAC; for IFAC it's 3/4 raw. Author may want to qualify. |
| F | "on most capacities" — ambiguous given Holm; author should decide if this refers to SC-FAC (4/4) or IFAC (3/4 raw, 2/4 Holm) |
| G | Author clarifies which method "most" refers to |
| H | ~9 lines |

---

## 14. Discussion and limitations (lines 436–483)

| Col | Content |
|-----|---------|
| A | Lines 436–483 (Factorization ¶436–448; Equivariance ¶450–459; Strong rule ¶461–472; Future work ¶473–474; Limitations ¶476–483) |
| B | Factorization: removes avoidable drops (consistent with), gains survive paired tests (Holm: 4/4 SC-FAC, 2/4 IFAC, C=900 non-surviving). Conditioning: null at τ=10. Equivariance: operational deployability not matched-k accuracy; flat architecture cannot do without resizing; k=24 all-seed aggregate sensitive to one failed seed, no clear deficit excluding it. Strong rule: highest Money, zero drops, fill captures decision-relevant info, nearly solved by feedback control. Future work: non-i.i.d. bursts, heterogeneous sizes/fees, multi-step lookahead, misaligned rewards. Limitations: one flush/step, finite horizon, single fee, no lookahead, homogeneous wallets, single-process PPO, CPU faster than GPU for batch-1 rollouts. Prior manuscript: faithful port, documented re-implementations. |
| C | All numbers from source CSVs; Holm values from STATISTICAL_AUDIT.md |
| D | (No new citations needed) |
| E | "removes exactly the avoidable drops" → "consistent with removing". "which a flat MLP structurally cannot do" → "which the particular fixed-shape flat architecture used here cannot do without resizing its weights". "wallet fill is close to a sufficient statistic" → "wallet fill captures much of the decision-relevant information". Holm correction now explicit. "costs matched-scale accuracy" → "sensitive to one failed seed; excluding it, no clear matched-scale deficit". |
| F | MUST keep Holm distinction (4/4 SC-FAC, 2/4 IFAC). MUST keep "consistent with" not "exactly/removes". MUST keep failed-seed sensitivity for k=24. |
| G | Author may tighten Discussion/Conclusion redundancy to save space. The Discussion and Conclusion currently overlap; author may merge or cut. |
| H | ~48 lines; can save 5–8 lines by removing redundancy with Conclusion |

---

## 15. Conclusion (lines 485–505)

| Col | Content |
|-----|---------|
| A | Lines 485–505 |
| B | Factorization: gain over joint head, significant 4/4 SC-FAC (survives Holm), 3/4 IFAC (2/4 Holm, C=900 non-surviving); cuts outputs (k+1)²→2(k+1). Conditioning: no detectable gain (zero/shuffle ablations). Equivariant encoder: zero-shot deploy to unseen k where fixed-shape flat cannot without resizing; asymmetric transfer; matched-scale cost sensitive to one failed seed. Strong rule: highest Money, zero post-switch drops, beats learned in nearly every paired comparison. |
| C | All numbers from CSVs; Holm from audit |
| D | (No new citations in Conclusion) |
| E | "significant at all four capacities for SC-FAC and at three of four for IFAC" → now adds "(surviving Holm correction)" and "(two of four after Holm correction, C=900 non-surviving)". "where a flat MLP cannot" → "where the particular fixed-shape flat architecture used here cannot without resizing". "matched-scale cost concentrated at the hardest operating point" → "sensitive to one failed seed". |
| F | MUST keep Holm distinction. MUST keep "fixed-shape flat architecture" qualifier. |
| G | Author may condense; avoid repeating Discussion verbatim |
| H | ~21 lines; can save 3–5 lines |

---

## Summary of overclaims corrected in this pass (do not reintroduce)

1. "partially-specified Markov decision process" → "online decision problem"
2. "near-optimal" → "highest observed Money among all evaluated methods"
3. "sufficient statistic" → "captures much of the decision-relevant information"
4. "causal value" → "mechanistic value" (heading + body)
5. "adapting without retraining" → "maintaining its observed performance without retraining"
6. "deterministic code" → "code with fixed seeds and fixed evaluation pools"
7. "flat MLP cannot" → "fixed-shape flat MLP cannot reuse its weights" / "the particular fixed-shape flat architecture used here cannot without resizing"
8. "exactly the failure mode" / "mechanism interpretation is direct" → "consistent with" / "the failure mode ... are expected to reduce"
9. "robust to regime shifts" / "robust enough not to collapse" → "maintains this across the tested regime shifts" / "do not collapse"
10. "paired at the episode level" → "share identical evaluation inputs; statistical unit = matched training seed"
11. "clear matched-k cost / lower at k=24 (9190 vs 13610)" → "failed-seed sensitivity; 13785 excl vs 13610, no clear deficit"

---

## Statistical wording reference (from STATISTICAL_AUDIT.md)

- **Statistical unit = matched training seed** (n=5 main; n=3 ablation/switching)
- **2400 test episodes are evaluation repeats, NOT independent replicates**
- **IFAC vs JA-PPO**: 3/4 raw → 2/4 Holm (C=900 p_Holm=0.064 non-surviving)
- **SC-FAC vs JA-PPO**: 4/4 raw, all 4 survive Holm
- **SC-FAC vs IFAC**: C=800 SC-FAC significantly lower (−419, p=0.009, Holm 0.036); other 3 null
- **BFP0.5 vs learned**: 11/12 significant (exception: vs IFAC C=1000, +2545, p=0.057)
- **Switching SC-FAC**: drops p≈0.09, Money raw p=0.035 → Holm p=0.069 NOT significant
- **k=24**: 9190 incl failed seed; 13785 excl; flat 13610 (n=3)
- **5/5 wins is descriptive, NOT a significance test**
- **Cross-k off-diagonal cells are zero-shot deployment evidence, NOT fair matched-task accuracy benchmark**
- **Fixed C + changing k changes both C/k and oversize difficulty**
- **Avoidable drops (77.01/49.51/40.41): mechanistic consistency, NOT causal proof**

p-value formatting: all p<0.001 displayed as "$<0.001$" in generated tables.
