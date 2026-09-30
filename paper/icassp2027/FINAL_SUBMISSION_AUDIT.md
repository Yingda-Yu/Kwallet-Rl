# FINAL SUBMISSION AUDIT — ICASSP 2027 submission candidate (freeze pass)

Commit being prepared: **"paper: freeze ICASSP 2027 submission candidate"**,
on branch `work/icassp2027-reproduce-improve`, on top of `a3d91f8`
(readability pass) and `bc36d3b` (finalization). This is a submission-freeze,
presentation/precision pass: **no experiment was run, no frozen scientific
result changed, no conceptual figure redrawn or regenerated, nothing pushed**.

## 0. What changed in this pass

1. Fig.1 is now the **author-designated ChatGPT PNG**, byte-for-byte copy,
   single column (Section 1 below).
2. BFP description rewritten against the actual implementation; validation
   pool structure code-verified (Section 4).
3. Added a code-verified "Implementation details" paragraph; Table 1 enlarged
   for readability (Section 5).
4. Abstract / Introduction / Discussion tone fixes required by the authors
   (failed seed out of abstract; positive novelty positioning; neutral
   cross-$k$ wording; venue-fit sentence) (Sections 6–8).
5. Prior-manuscript status investigated and language corrected (Section 9).
6. References 23 → 25 with two newly verified 2025 PCN papers; two further
   candidates verified but rejected (Section 10).
7. AI disclosure made factual (Section 11); title options documented but not
   changed (Section 12); EDICS recommendation retained (Section 13).
8. All build gates re-verified (Section 14) and six-criterion review audit
   (Section 15).

## 1. Exact Fig.1 file used

- Source (author-designated):
  `assets/figs/ChatGPT Image 2026年9月23日 07_41_35.png` (1837×856, 1.14 MB).
- Used file: `assets/figs/fig1_chatgpt.png`, produced by a **single
  byte-for-byte `cp`** (`cmp` confirms identity). No matplotlib/PIL/ImageMagick
  redraw, no trim, no in-figure caption, no pixel change.
- Inclusion: single column `[t]`, `\includegraphics[width=0.98\columnwidth]`
  (within the permitted 0.95–0.99 range; not moved). Caption lives in LaTeX
  (5 lines: flush-first with fee $\tau$/cooldown $F$, settlement second,
  accept $p x_t$, drop categories, availability not drawn).
- Legibility at 100% reading size: essential labels ($x_t$, $s_t$, $a_f$,
  $a_s$, fee $-\tau$, $F{=}3$, accept $+p x_t$, oversize/frozen/avoidable)
  are crisp (source is ~550 dpi effective in column); minor panel sub-text
  (~5 pt) is small but readable; per instruction the image is not altered.
  `fig1_compact.pdf` from the previous pass exists on disk but **is not
  referenced anywhere** (grep-verified).
- Fig.2 unchanged: the same conceptual PNG, two columns, 0.92 textwidth,
  3-line caption, panel text verified legible.

## 2. Page count / occupancy measurements

Measured after the Fig.1 swap (before any text was added), and re-measured
after all edits:

- **main.pdf = exactly 5 pages**, clean full rebuild (pdflatex×3 + bibtex).
- Page 1: abstract, index terms, Introduction through first two
  contributions bullets; bottom whitespace minimal.
- Page 2: rest of contributions, Sec. 2, single-column Fig.1 (top of right
  column), Sec. 3, start of Sec. 4; both columns filled to the bottom.
- Page 3: two-column Fig.2 (top), precise BFP paragraph + implementation
  details, Table 1 (footnotesize), Sec. 4.2 start; both columns full.
- Page 4: Tables 2–4, remaining results, Sec. 5 Discussion and Conclusion,
  Acknowledgment (incl. AI disclosure) — all end on page 4. Post-edit
  bottom whitespace: left column ~7%, right column ~20% (normal, no hacks
  used: no negative vspace, no margin/font-size changes).
- Page 5: **References only**, 25 entries ending at ~88% of the right
  column; 27 entries overflowed to page 6 in a test, which is why exactly
  two of four verified candidates were retained (Section 10).
- 0 LaTeX errors, 0 undefined refs/citations, 0 BibTeX warnings, 0 Overfull
  hboxes; 5 benign Underfull hboxes (badness 1005–1983); 0 Type 3 fonts.
- `pdftotext` grep: no TODO/placeholder/internal-draft/markdown markers.
- `python -m pytest`: **37 passed**.

## 3. Figures and tables inventory (final)

- Figures: Fig.1 `fig1_chatgpt.png` (single column, author artwork);
  Fig.2 `fig2.png` (two columns, author artwork). No tiny/non-legible figure
  remains; the 0.42-column heatmap stays replaced by Table 3.
- Tables, one claim each: T1 main stationary Money; T2 conditioning
  ablation; T3 cross-$k$ transfer (auto-generated `transfer_compact.tex`
  from frozen `kscale_transfer_long.csv`); T4 switching streams.

## 4. BFP definition — verified line-by-line against code

Source: `src/kwallet/baselines/rules_strong.py::bestfit_proactive_action`,
`src/kwallet/baselines/rules.py::get_rule_fn`, `src/kwallet/envs/kwallet.py`
(`balance` initialised to `wallet_size`, decremented by settlements,
restored to full after refill; hence balance = **remaining free balance**).

Precise semantics now stated in the paper:
- settle: among usable (cooldown-free) wallets with $b_i \ge x_t$, choose the
  smallest $b_i$ (best fit);
- flush: in the same step, consider usable wallets other than the settle
  wallet, take the one with smallest $b_i$ (the fullest in occupancy terms),
  and flush it iff $b_i < \theta\,C/k$;
- fallback: if nothing fits, flush the most depleted usable wallet and drop
  the current transaction.
This removes the earlier ambiguous phrase "flushes the fullest usable
wallet… below a fraction of wallet capacity" while keeping the same meaning.

Threshold provenance (`docs/DECISIONS.md`, 2026-09-10 entry; `rules.py`
`RULE_NAMES`): sweep over $\theta\in\{0.3,0.5,0.8\}$ on validation only;
BFP0.5 best (validation Money $15290\pm135$ at $C{=}1200$); chosen once,
frozen, used unchanged at all four capacities ($800,900,1000,1200$); test
pools never used for tuning. The paper now says exactly this.

**Validation-pool correction (code-verified):** the proposed phrasing
"300 validation episodes per regime (3,600 total)" is **false** and was not
used. `src/kwallet/data/pools.py::build_pools` builds one MIX12_EQ pool of
**300 total validation episodes, allocated equally across 12 regimes (25
per regime)**; test pools are separate, **200 episodes per regime** (2,400
total). The paper now says "the 300-episode mixed validation pool (25
episodes per regime)"; the existing "200 test episodes per regime" is
correct.

## 5. Space on page 4 used for science (not filler)

1. **Implementation-details paragraph (new, ~11 lines), every value from
   code** (`src/kwallet/training/ppo.py::PPOConfig`, `scripts/run_experiments.py`,
   `src/kwallet/data/pools.py`, switching CSVs): two-layer trunk, 256 hidden
   units; 32-d settle embedding (SC-FAC); Adam $3\times10^{-4}$;
   $\gamma{=}0.99$; GAE $\lambda{=}0.95$; clip $\epsilon{=}0.2$; value
   coefficient 0.5; entropy 0.02→0.001 linear anneal; grad-norm clip 1.0;
   3000 training episodes; 8-episode rollouts; 10 update epochs; 512
   transition minibatches; validation-selected checkpoints; deterministic
   $\arg\max$ evaluation; main seeds 123, 323, 532, 777, 999; ablation and
   switching seeds 123, 323, 532 (verified in ablation long CSV and
   `runs/sw_ifac/switch_learned.csv`).
2. **Table 1 `\scriptsize` → `\footnotesize`** (tabcolsep 3.2→3.6 pt); it
   stays within its float, no overflow, and mean±SE entries are clearly more
   legible. No other font/margin/spacing change was made.
3. Exact protocol already present (5000/300/200 pools, seeds) kept.

## 6. Abstract change (F)

The failed-seed detail was removed from the headline: "…with asymmetric
transfer and one training failure at the largest $k$." → "…although transfer
quality is asymmetric." The failure (seed 532, Money 0) remains fully
reported in Results (Table 3 + text), Discussion, and limitations.

## 7. Positive novelty positioning (G) and venue-fit language (K)

- The defensive "We claim neither factorization nor set encoding as new
  primitives" was replaced by: "Building on these established primitives, we
  conduct a controlled empirical audit of which structural biases improve
  streaming collateral control: matched mechanism ablations, zero-shot
  cross-$k$ deployment, a strong validation-selected feedback baseline, and
  paired multi-seed evaluation, with null results reported alongside
  positive ones."
- Venue-fit sentence added to the Introduction: the task "combines streaming
  observations, structured discrete actions, and online resource allocation
  under nonstationary transaction arrivals." Keywords and abstract already
  carry streaming resource allocation / online sequential decision making /
  payment-channel / nonstationary streams; "signal processing" is not
  claimed without basis.

## 8. Cross-$k$ wording de-defensived (H)

- Results now state plainly: at $k{=}24$ the primary all-seed Set-SC-FAC
  mean is 9190 vs 13610 flat, including the retained failed run (seed 532,
  Money 0); the 13785 figure over the two nonfailed runs is labeled a
  sensitivity calculation only.
- Discussion: "…strongly affected by one failed training run, which is
  retained in the primary aggregate; this indicates training instability and
  prevents a claim of matched-scale superiority." The apologetic "dominated
  by one failure rather than a true deficit" phrasing was removed. No value
  changed.

## 9. Prior-manuscript status (I) — investigated, not guessed

`paper/old paper.pdf`: 10-page TeX/PDFTeX document, produced 2026-09-08,
titled "Settle-Conditioned Policy Learning for Streaming Transaction
Collateral Control", by **"Anonymous Authors"**, with no venue, copyright
line, proceedings identifier, or arXiv ID anywhere in the text. This is an
**unpublished, anonymous internal manuscript (Situation B)**, not a citable
publication. Actions taken:
- no bibliographic citation was fabricated;
- vague "prior environment" / "prior manuscript" mentions now read "the
  original K-Wallet environment" and "the original (anonymous, unpublished)
  K-Wallet specification";
- authors must still confirm the document's exact status (under review?
  withdrawn?) before submission, since self-overlap rules depend on it
  (Section 16).

## 10. References: 23 → 25 this pass (16 → 25 total)

Added (metadata verified on publisher/authoritative pages, both cited):
- `valko2025hybrid` — Valko & Kudenko, "Hybrid Pathfinding Optimization for
  the Lightning Network with Reinforcement Learning", *Engineering
  Applications of Artificial Intelligence* 146:110225, 2025,
  DOI 10.1016/j.engappai.2025.110225 (RL for PCN pathfinding).
- `chatterjee2025boosting` — Chatterjee, Křišťan, Schmid, Svoboda & Yeo,
  "Boosting Payment Channel Network Liquidity with Topology Optimization and
  Transaction Selection", DISC 2025, LIPIcs 356:4:1–4:22,
  DOI 10.4230/LIPIcs.DISC.2025.4 (streaming accept/reject under locked
  capacity — closest formal kin to our admission decisions).

Verified but **rejected** to protect relevance and the 5-page limit:
- Castro et al., "Estimating Policy Functions in Payment Systems Using
  Reinforcement Learning", ACM TEACM 13(1):1–31, 2025, DOI 10.1145/3691326 —
  real and verified, but targets high-value (bank) payment systems, not PCNs;
  too tangential for a 4-page paper.
- Flavin & Sen, "Revisiting Action Factorization for Complex Action Spaces",
  arXiv:2606.26574 (25 Jun 2026) — thematically close (empirical
  factorization audit), but an unrefereed preprint and its clause plus entry
  pushed references to a 6th page; can be re-added at a venue with more
  space. No padding reference was kept.

## 11. AI disclosure compliance (M)

- The generic "an AI coding assistant" is now identified as **the Trae AI
  coding assistant** (the environment in which all code development and
  visualization for this project was performed; ChatGPT is already named for
  drafting and the two conceptual figures).
- AUTHOR CONFIRMATION REQUIRED: the exact underlying model/version of the
  Trae assistant cannot be confirmed from project files; authors should
  verify the precise system name/version required by ICASSP/IEEE disclosure
  rules.
- "produced by the released code" → **"produced by the project code"**: the
  code is not publicly released (local repository, open PR draft, no public
  URL), so "released" was factually unsupported.

## 12. Title (L) — options documented, not changed

The author title "Auditing Structured Policy Learning for Streaming
Transaction Collateral Control: Factorization, Conditioning, and Cross-Scale
Transfer" (3 lines) was **kept**, because the freeze brief did not authorize
  changing the author title and it preserves all three study axes.
Tighter candidates if authors want one less line later:
(a) "Structured Policy Learning for Streaming Collateral Control: An
Empirical Audit"; (b) "Auditing Structured Policy Learning for Streaming
Collateral Control". (a) loses the factorization/conditioning/transfer
signposting; (b) is shortest. Recommendation: keep current unless page-1
space becomes critical (it currently does not).

## 13. Recommended EDICS / track note (authors select; nothing submitted)

- Primary: **MLSP — Machine Learning for Signal Processing** (RL algorithms
  and applications / sequential decision making and control).
- Secondary: **SPCOM — Signal Processing for Communications and Networking**
  (resource allocation in networks; payment-channel-style liquidity
  allocation).
Basis: ICASSP review-area naming patterns (2026 program listings checked in
the prior pass; the 2027 classifier was not yet published at audit time).
Authors must confirm against the live ICASSP 2027 CMS EDICS list and make
the selection themselves.

## 14. Final build gates

| Gate | Result |
|---|---|
| Exactly 5 pages | PASS |
| Technical content pages 1–4 | PASS |
| Page 5 references only | PASS (25 entries) |
| Author-specified Fig.1 used, byte copy | PASS (`cmp` identical) |
| Fig.1 single column 0.98 columnwidth | PASS |
| fig1_compact.pdf not referenced | PASS (grep) |
| Fig.2 unchanged artwork, two columns | PASS |
| Markdown artifacts: `grep '\\textbf{\*\*'`, `grep '\\emph{\*'`, `grep '\*\*'` | PASS, zero matches (only `$^{*}$Corresponding author` remains) |
| Undefined refs/cites | PASS (0) |
| Overfull boxes / BibTeX warnings | PASS (0/0) |
| Type 3 fonts / TODO / placeholder | PASS (none) |
| No hand-typed frozen number contradicts CSV | PASS (no number changed; new prose values traced in Section 5) |
| 37 pytest tests | PASS |
| pdftotext + rendered pages double QA | PASS (all 5 pages rendered at 80 dpi; Fig.1 additionally zoom-checked) |

## 15. Six-criterion ICASSP review audit

1. **Language / clarity — PASS.** Compact precise prose; BFP and protocol are
   unambiguous; figures carry captions outside the artwork; tables legible
   (T1 enlarged).
2. **Importance / relevance — PASS (residual reviewer-fit risk).** Framed
   explicitly as streaming resource allocation with online sequential
   decisions under nonstationary financial transaction arrivals; EDICS note
   provided. It is not a signal-processing-methods paper, so MLSP/SPCOM fit
   should be selected deliberately.
3. **Novelty / originality — PASS (residual risk).** Stated positively and
   narrowly as the first controlled empirical boundary audit (factorization
   vs conditioning vs set-encoder deployability vs validation-selected
   feedback) on this testbed; no claim of new primitives; related work now
   spans factored RL, large discrete actions, set architectures, and 2023–
   2025 PCN RL/algorithmic work (25 refs).
4. **Technical correctness — PASS.** Flush-before-settle semantics,
   factorized likelihoods, matched ablations, frozen seeds; code-verified
   hyperparameters and pool sizes in text.
5. **Experimental validation — PASS (residual risk).** Five main seeds,
   paired tests, Holm corrections, null results, switching streams,
   cross-$k$ matrix, failed seeds retained; weaknesses are small $n$ for
   ablations/switching (n=3) and one failed $k{=}24$ seed, both disclosed.
6. **References / prior work — PASS.** 25 verified entries, every new one
   cited with a clear role; no padding; the anonymous source manuscript is
   handled factually.

Boundary framing honored: BFP beating the learned policies is presented as a
result (boundary of when structure helps), not hidden; no overclaim around
the failed seed; all null results (conditioning ablations, SC-FAC-vs-IFAC
intervals, switching contrasts) reported with exact p-values.

## 16. Remaining submission blockers (author actions only)

1. Confirm status of the anonymous 10-page source manuscript and any
   self-overlap/dual-submission implications (Section 9).
2. Corresponding-author email; ORCIDs; funding statement; registration
   track; final author approval of abstract/wording and AI-disclosure text,
   including the exact Trae model/version name (Section 11).
3. Final title decision (Section 12) and live EDICS selection (Section 13).
4. IEEE copyright / PDF eXpress after metadata edits; system upload — not
   performed here and not permitted by this automation.
5. Human sign-off on Fig.1 at full resolution (byte-identical author file)
   and on every numerical claim (all traceable to frozen CSVs).
