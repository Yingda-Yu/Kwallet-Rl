# Author Rewrite Packet — ICASSP 2027 manuscript

Prepared: 2026-09-22. File: `paper/icassp2027/main.tex`.

## Purpose and rules

ICASSP 2027 policy does not permit an LLM to generate substantial manuscript
components. This packet therefore contains **no paste-ready sentences**. For
each section it gives: immutable facts and exact numbers, required citations,
wording that must be removed or softened, and overclaims to avoid. The author
writes every final sentence.

After the author rewrites a section, rebuild and verify: no number may change
unless the author also updates the matching CSV provenance — none of the
numbers below may be edited by hand.

**Current space budget: ZERO slack.** The technical content fills all four
pages exactly; page 5 holds only references (16 entries, two columns). Any
replacement text must be the same length or shorter, or the author must free
space (e.g., shorten the Discussion/Conclusion redundancy). Do not shrink
figures below the current sizes — concept figures are already at the
minimum legible scale.

---

## Abstract (currently 223 words — OVER the 200-word hard form cap)

Factual skeleton (author decides every word; target 120-150 words; hard form
limit 200 — the current draft is 223 words, so the author must cut at least
24 words even to be submittable; reaching 120-150 words requires cutting
roughly 70-100 words; keywords listed separately, 5 exactly):

- Task: streaming payment-channel transactions routed into k collateral
  wallets, plus optional flush of one wallet at fixed fee; framed as an online
  MDP with twelve traffic regimes.
- Result 1: across 5 seeds, settle-conditioned factored head beats the joint
  head at 4/4 capacities; independently factored head at 3/4 (raw paired
  tests — see Experiments note; Holm sensitivity exists).
- Result 2: conditioning path itself shows no statistically detectable Money
  gain (95% CIs include zero; zero- and shuffle-conditioning ablations
  indistinguishable).
- Result 3: permutation-equivariant encoder has no k-dependent parameters;
  zero-shot deployment across wallet counts; asymmetric transfer.
- Result 4: validation-selected threshold rule attains highest Money at every
  capacity, zero avoidable drops including after abrupt regime shifts; beats
  learned policies in nearly all paired comparisons.
- Provenance: all numbers from released deterministic code on ported data.

Required decisions / removals:
- "partially-specified Markov decision process" — AUTHOR DECISION: the
  transition is in fact fully specified in the port; either define the term
  precisely (what is unobserved?) or replace with "online decision problem".
- "significant(ly) beats" — keep only with the test name; abstract has no room
  for test details, so consider "higher Money in paired tests at 4/4
  capacities".
- "at the largest tested k it trails a size-matched flat network" — remove or
  flag: the difference (9190 vs 13610) depends on one failed seed (13785 vs
  13610 without it). Prefer "asymmetric transfer; no matched-scale advantage
  is claimed".
- "wallet fill is close to a sufficient statistic" — technical term; author
  must justify or replace with "current fill alone drives the feedback rule".
- "significantly outperforms ... in nearly all paired comparisons" — pick one
  qualifier; precise fact: BFP advantage significant in 11/12 main contrasts
  (and in switching for JA/IFAC; not for SC-FAC after Holm).
- Count words after rewrite; <=200 hard, aim 120-150.

## Introduction

Paragraph 1 (background; cite keys already wired):
- Immutable: transactions arrive sequentially with value x_t; settle into one
  of k wallets with enough free balance or drop; independently flush one
  wallet at fixed fee with cooldown; C is partitioned per wallet; sequential
  trade-off (flush costs and removes service now, frees capacity later).
- Citations present: Lightning/state channels [poon, miller, kolachala];
  routing under scarce funds [sivaraman]; online analysis [borodin];
  learning-augmented [lykouris]; closest formal model [almashaqbeh];
  inventory [lin].
- Removed in this pass: "Every few milliseconds" (no source — do not restore
  any concrete timing/frequency claim).
- Do NOT call the prior unpublished manuscript a published reference;
  Almashaqbeh et al. is the citable closest formal model and is not the same
  system — state the relationship carefully ("closest formal model").

Paragraph 2 (why factorize):
- Immutable: joint head outputs (k+1)^2 = 625 at k=24; factored heads 2(k+1)
  = 50; conditioning question settle->flush posed as hypothesis.
- Removed: "squandering samples" (sample-efficiency claim unverified). Do not
  replace with a sample-complexity assertion unless supported.
- Citation present: branching [tavakoli].

Paragraph 3 (set encoder):
- Immutable: flat MLP weight shapes depend on k; cannot be loaded at a new k;
  shared permutation-equivariant function removes k-dependent parameters;
  zero-shot deployment; cost-at-original-scale is an open question.
- Avoid: any claim that equivariance improves same-k accuracy; the paper finds
  it does not.

Paragraph 4 (strong baseline; audit framing):
- Immutable: prior manuscript baselines are simple (flush-always, flush-full)
  and do not use current fill; BFP0.5 selected on validation; audit framing.
- Removed: "Prior comparisons use only trivial rules, which a learner beats
  easily" — comparative ease unsupported. Keep the descriptive version.
- Avoid "faithful port ... twelve regimes" overclaim: faithful port of the
  environment; unspecified hyperparameters are documented re-implementations.

Contributions list: keep four items; item 1 must keep the
"documented re-implementation" qualifier; item 3 must keep "at the tested
flush price" (tau=10; result need not generalize across fees); item 4 word
"robust" is a flagged term — prefer descriptive "zero avoidable drops across
the tested switch scenarios".

## Streaming collateral control

- Exact quantities that must not change: C in {800,900,1000,1200}; k=24;
  T=1000 decisions/episode; x_t in [0,1000]; a_s, a_f in [0,k] with k = null;
  flush executes FIRST then settle; F=3 cooldown; capacity per wallet C/k;
  observation dimension 3k+2; Money M = p * sum(accepted x) - tau * #flushes,
  p=1, tau=10; 12 regimes; data sizes 5000 train / 300 validation / 200 test
  per regime; deterministic argmax evaluation.
- Drop taxonomy is an author-defined attribution: oversize (x_t > C/k),
  frozen (cooldown), avoidable (insufficient balance or flush/settle
  conflict). State it as an accounting convention, not a causal
  decomposition.
- Required: mention that fixed C with changing k changes both C/k and the
  oversized fraction (used in Fig. 4 interpretation).
- Citations present: PPO [schulman2017ppo], GAE [schulman2015gae].

## Policies

- Immutable numbers: JA (k+1)^2 = 625; IFAC/SC 50 logits; IFAC factorization
  pi(a_s,a_f|s) = pi_s pi_f; SC-FAC pi_f(a_f|s,a_s); ablations: no-cond.
  zeroes embedding, shuffled feeds deranged embedding.
- Set encoder: shared phi over wallet features, symmetric pooling, per-wallet
  logits (Fig. 2); cite Deep Sets [zaheer2017].
- Structured-action citations present: [dulac, hausknecht, tavakoli,
  akkerman]. Keep claim wording to "related approaches" — do not assert these
  solve this problem.
- Avoid "causal value" for the conditioning test: the matched ablations
  isolate the information path architecturally; describe as "no detectable
  Money gain", consistent with null result.

## Experiments

Five organizing questions; immutable headline numbers:

1. Stationary performance (Table 2; n=5; mean+/-SE over seeds; 200 fixed
   episodes x regime): exact cells in `assets/tables/main_results.tex`.
   Examples: SC-FAC 3757/5404/7680/13179 at C=800..1200; BFP0.5
   4682/7027/9497/15327; FA 2907/4172/5533/8826.
2. Paired tests (Table 3 at C=1200; full per-C values in STATISTICAL_AUDIT
   §2): SC-FAC-JA positive 4/4 (p 0.0121, 0.0067, <0.0001, 0.0044); IFAC-JA
   positive at 3/4 raw (C=1000 null, p=0.57); SC-FAC vs IFAC: SC-FAC LOWER at
   C=800 (-419.3, p=0.0091); null at the other three.
3. **AUTHOR REVIEW REQUIRED #1**: Holm family correction moves IFAC C=900 to
   adjusted p=0.064 (3/4 raw -> 2/4 corrected). Author chooses reported frame;
   the conclusion sentence must be reconciled with the choice.
4. Avoidable drops 77.0 / 49.5 / 40.4 (JA/IFAC/SC, C=1200, means over 5 seeds).
   **AUTHOR REVIEW REQUIRED #4**: current wording "exactly the failure mode
   ... should remove" is mechanistic consistency, not causal proof — weaken.
5. Conditioning ablation (Table 4; n=3): all CIs include zero; 12951 vs 13235
   vs 13252 (SC-FAC / no-cond / shuf-cond), flush costs 571/545/579.
6. Cross-k (Fig. 4): describe as deployment capability + asymmetry
   (6->24 weak, 4433 example cell); **AUTHOR REVIEW REQUIRED #3**: no k=24
   deficit claim (failed-seed dependence; 9190/13785/13610).
7. Switching (Table 5; n=3; six scenarios): BFP zero avoidable drops; learned
   56.0 / 28.3 / 28.3 (JA/IFAC/SC); naive rules 143.8 / 148.4. **AUTHOR
   REVIEW REQUIRED #2**: SC-FAC vs BFP not significant (drops p=0.088; Money
   Holm p=0.069). Do not write p<0.01 for SC-FAC.
8. Parameter/output efficiency: outputs 625 -> 50; actor parameters
   245,874 -> 98,099 (IFAC); set variants 135,949 independent of k; latencies
   Table 1 (0.42-1.11 ms per step, CPU).
9. BFP dominance: 11/12 main contrasts significant; exception BFP-vs-IFAC
   C=1000 (+2545, p=0.057, CI [-119,5210], 5/5 wins). 5/5 wins must be
   labeled descriptive, not a test.

General writing constraints:
- Never use 2400 (or any episode count) as the statistical n; n=5 or n=3.
- Do not float output_scaling.pdf or switching_drops.pdf unless the author
  removes another same-size element (no space).
- The word "significant" may appear ONLY next to the named test and p-value.

## Discussion and limitations

Keep the honest framing; decisions for the author:
- "near-optimal" (threshold on balanced workload) — no optimality proof
  exists; remove or replace with a statement about oracle-feasible gap
  comparisons actually computed (oracle feasible values exist per regime;
  cite only if the manuscript reports the computed gap).
- "robust" — replace with scope: tested switch scenarios only; heterogeneous
  environments deliberately not instantiated.
- "sufficient statistic" — technical claim; justify or paraphrase.
- The speculative explanation (SC-FAC extra flushing aligned with future
  work) must stay explicitly labeled as a candidate explanation.
- Keep concrete limitations list (one flush/step, finite horizon, single fee,
  no lookahead, homogeneous wallets, single-process PPO).
- Do not add promises ("will generalize", "future work will show").

## Conclusion

Immutable numbers present: positive two points (factorization gains;
equivariant zero-shot deployment), null one (conditioning path), sobering one
(BFP benchmark). If the author adopts Holm reporting, the "three of four"
phrase changes per AUTHOR REVIEW REQUIRED #1. Keep last sentence at the same
level of generality; no new claims.

---

## Flagged-term decision table (author must resolve each)

| term | location | issue |
|---|---|---|
| partially-specified MDP | abstract | what is unspecified? define or remove |
| every few milliseconds | intro | removed; no timing source — do not restore |
| sufficient statistic | abstract, switching, discussion | formal term; justify or paraphrase |
| near-optimal | experiments, discussion | no proof; remove or replace |
| significant | abstract, experiments, conclusion | only with named test + p |
| adaptation | switching, discussion | no learning-based adaptation observed; describe scope only |
| robust | contributions, switching | scope-limited; prefer descriptive wording |

## After the author finishes

1. `pytest -q` (37/37 or better).
2. Clean rebuild (rm -rf build; pdflatex x3 with bibtex).
3. Full Final PDF QA per FINAL_SUBMISSION_GATE.md; refresh
   SUBMISSION_SNAPSHOT.md and SUBMISSION_ARTIFACT_SHA256.json.
4. Metadata fields (separate BLOCKED list) must be filled before QA can pass.
