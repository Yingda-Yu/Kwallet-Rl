# Statistical Audit (ICASSP 2027 finalization)

Date: 2026-09-22. Branch: `work/icassp2027-reproduce-improve`.

**Scope.** Internal audit only. No new training, no protocol change, no raw
CSV modified. Data sources: `results/tables/*.csv`, seed-level files under
`runs/`, and `paper/icassp2027/assets/paper_claims.json`. All tests were
recomputed independently from seed-level data during this audit.

## 1. Statistical-unit rules (apply manuscript-wide)

1. The statistical unit is the **matched training seed**: n=5 for the main
   matrix; n=3 for settle-conditioning ablations and switching.
2. 2400 test episodes (200 episodes x 12 regimes, or analogous totals) are
   evaluation repeats, **not** independent training replicates. They must not
   be used as n=2400 in any test.
3. Paired tests pair methods that share a seed and, where applicable, the same
   deterministic test episodes. Rules are deterministic, so pairing a rule
   with a learned seed reduces to a one-sample test of learned values against
   the fixed rule value.
4. 5/5 (or 3/3) wins is descriptive; it is **not** a significance test and
   must not be reported as one.
5. Cross-k off-diagonal cells (Fig. 4) are zero-shot deployment evidence, not
   a fair matched-task accuracy benchmark (see §6).
6. At fixed total capacity C, changing k simultaneously changes per-wallet
   capacity C/k **and** the fraction of transactions that are oversized. Any
   cross-k comparison inherits this coupled difficulty; it cannot be
   attributed to k alone.

## 2. Main matrix (n=5), raw paired t-tests — verified

Recomputed from `matrix_main_main_long.csv`; values match
`matrix_main_paired.csv`.

| contrast | C | mean diff | 95% CI | p |
|---|---|---|---|---|
| IFAC - JA-PPO | 800 | +1096.0 | [881.2, 1310.7] | 0.0001 |
| IFAC - JA-PPO | 900 | +1059.6 | [146.6, 1972.7] | 0.0322 |
| IFAC - JA-PPO | 1000 | +599.6 | [-2089.6, 3288.8] | 0.5694 |
| IFAC - JA-PPO | 1200 | +1620.8 | [1108.1, 2133.5] | 0.0009 |
| SC-FAC - JA-PPO | 800 | +676.7 | [245.0, 1108.3] | 0.0121 |
| SC-FAC - JA-PPO | 900 | +999.0 | [462.5, 1535.4] | 0.0067 |
| SC-FAC - JA-PPO | 1000 | +1327.2 | [1135.1, 1519.2] | <0.0001 |
| SC-FAC - JA-PPO | 1200 | +1285.3 | [670.7, 1899.9] | 0.0044 |
| SC-FAC - IFAC | 800 | -419.3 | [-665.6, -173.0] | 0.0091 |
| SC-FAC - IFAC | 900 | -60.7 | [-503.5, 382.1] | 0.7230 |
| SC-FAC - IFAC | 1000 | +727.6 | [-1926.6, 3381.8] | 0.4890 |
| SC-FAC - IFAC | 1200 | -335.5 | [-1231.1, 560.0] | 0.3569 |

BFP0.5 vs learned (n=5): BFP advantage significant at all 12 contrasts
except **BFP0.5 vs IFAC at C=1000**: +2545.4, 95% CI [-118.9, 5209.7],
p=0.0568, 5/5 wins.

## 3. Holm multiple-comparison sensitivity

Holm step-down applied **within pre-specified families** (corrections are
exploratory; the experiment was not powered for them).

- **Family F1 (factorization vs JA-PPO, 8 tests).** All SC-FAC contrasts
  survive (adjusted p: 0.036, 0.027, 0.0003, 0.022). IFAC survives at C=800
  (0.001), C=1200 (0.006), and the C=1000 null stays null; **IFAC at C=900
  does NOT survive: adjusted p=0.064**.
- **Family F2 (SC-FAC vs IFAC, 4 tests).** Only C=800 is significant, and it
  survives (adjusted p=0.036, direction: SC-FAC *lower*); other three are
  null.
- **Family F3 (BFP0.5 vs learned, 12 tests).** Same pattern as raw tests:
  11/12 significant after Holm; C=1000 vs IFAC remains the exception.

**AUTHOR REVIEW REQUIRED #1.** Conclusion currently states factorization is
"significant ... at three of four for the independent variant." That is
correct for raw tests (3/4) but becomes **2/4** under the family-wise Holm
correction. The author must decide whether to report raw, corrected, or both.

## 4. Switching streams (n=3) — one claim overstated

Recomputed per seed (mean over six matched scenarios) vs BFP0.5, one-sample
t, then Holm across the six learned-family tests:

| policy | metric | mean diff vs BFP | raw p | Holm p |
|---|---|---|---|---|
| JA-PPO | post drops | +56.00 | 0.0027 | 0.0133 |
| JA-PPO | post Money | -2091.88 | 0.0088 | 0.0264 |
| IFAC | post drops | +28.31 | 0.0029 | 0.0133 |
| IFAC | post Money | -986.41 | 0.0020 | 0.0123 |
| SC-FAC | post drops | +28.29 | **0.0882** | 0.0882 |
| SC-FAC | post Money | -1200.27 | 0.0346 | **0.0692** |

The earlier manuscript text claiming all learned policies are "significantly
worse than BFP0.5 on both drops and Money (p<0.01, n=3)" was not supported
for SC-FAC. The manuscript now reports the precise values, including the Holm
failure for SC-FAC Money. **AUTHOR REVIEW REQUIRED #2:** confirm final wording;
do not restore p<0.01 for SC-FAC.

## 5. Settle-conditioning ablation (n=3) — null confirmed

Four contrasts at C in {800, 1200}: SC-FAC vs no-cond. and SC-FAC vs
shuffled. Raw p range 0.27-0.65; Holm-adjusted all 1.0. Supports "no
detectable Money gain"; no positive claim is made elsewhere. ✓

## 6. Cross-k transfer and failed-seed sensitivity

- 18 off-diagonal Set-SC-FAC deployments (6 train/test pairs x 3 seeds):
  **16 execute**, the two seed-532/train_k=24 deployments produce Money=0
  (failed training seed, retained honestly).
- Per-cell Money retention vs same-seed diagonal, mean: **84.9% excluding**
  the failed seed; **75.5% treating failed deployments as zero**. These
  ratios mix genuinely different task scales (§1.6) and are descriptive.
- Set-SC-FAC diagonal at k=24: mean **9190 including** the failed seed,
  **13785 excluding** it; flat SC-FAC diagonal k=24 = **13610** (n=3).

**AUTHOR REVIEW REQUIRED #3.** Any statement that the set encoder is worse
at k=24 than the flat encoder (e.g., "9190 vs 13610") rests on one failed
seed; excluding it the two are close (13785 vs 13610). The body text avoids
claiming a deficit; keep it that way.

## 7. Avoidable drops — verified; mechanistic, not causal

Means over five seeds at C=1200, k=24 (sum of insufficient-balance and
same-wallet-conflict drops), recomputed from the 15 raw evaluation CSVs:
**77.01 (JA-PPO), 49.51 (IFAC), 40.41 (SC-FAC)** — matching the manuscript's
77.0 / 49.5 / 40.4.

The phrase "avoidable drops fall ... exactly the failure mode the smaller,
better-coupled heads should remove" is **mechanistic consistency evidence**.
There is no intervention isolating drop causes, so it must not be presented
as a causal proof. **AUTHOR REVIEW REQUIRED #4** (wording note already in the
human-rewrite packet).

## 8. Net effect on conclusions

- Unchanged: factorization gains (raw and corrected, except the single IFAC
  C=900 correction noted above); null settle-conditioning result; BFP0.5
  dominance with one exception; zero-shot deployment capability.
- Weakened: SC-FAC switching comparison (no significant contrast after
  Holm); IFAC C=900 under Holm; any k=24 set-vs-flat deficit reading.
- No correction produces a stronger result anywhere.
