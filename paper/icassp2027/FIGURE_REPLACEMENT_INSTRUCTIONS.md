# Instructions to replace Fig. 1 and Fig. 2 placeholders

Scope: produce two **schematic/concept** vector figures and swap them into
`main.tex` for the two framed placeholders. These figures contain NO
experimental results (no new runs); the only numbers allowed are the
definitional ones already in the paper ($625$ vs $50$ outputs, $C/k$, $F{=}3$,
$\tau$, $p$). Keep every statistic in the paper coming from the frozen CSVs; do
not invent curves/bars. Match the existing figure style produced by
`scripts/make_paper_assets.py` (matplotlib, `figsize` ~3.4 in wide,
`tight_layout`, vector PDF saved under `assets/figs/`).

Outputs to create:
- `paper/icassp2027/assets/figs/overview.pdf`
- `paper/icassp2027/assets/figs/structures.pdf`

Recommended implementation: add one deterministic, data-free script
`scripts/make_concept_figures.py` (matplotlib only) that draws both figures and
writes the two PDFs above. Run it with the `kwallet` env. Do not wire it into
the experiment aggregation; it is purely conceptual artwork.

Style requirements (both figures)
- `figsize` close to the placeholder footprint so layout does not reflow much:
  overview `(3.4, 2.0)` inches; structures `(3.4, 2.3)` inches.
- Font sizes 8-9 pt for labels, 7-8 pt for annotations (readable after column
  scaling). Use math text consistent with the paper: $k$, $C/k$, $a_s$, $a_f$,
  $\tau$, $F{=}3$, $(k{+}1)^2$, $2(k{+}1)$.
- Black/dark-gray strokes; if color is used, keep it sparse and consistent
  with capacity_curve/transfer colors, and ensure it is legible in grayscale.
- White background, no matplotlib frame around the whole figure (the LaTeX
  `\fbox` placeholder goes away when replaced).
- Vector PDF, `bbox_inches='tight'`/`tight_layout()`; target each file well
  under ~150 KB.

Fig. 1 — overview.pdf (`fig:overview`)
- Left: a horizontal time axis with discrete arrivals $x_1,x_2,\dots,x_t$
  (arrows/boxes from the left) feeding a vertical row of $k$ wallets drawn as
  capacity bars/tanks of equal capacity $C/k$, each showing a current fill
  level (different levels across wallets).
- One "settle" arrow: $x_t \to$ one wallet, label accept payoff $+p\,x_t$ when
  free balance $\ge x_t$.
- One "flush" arrow on a (different) wallet: label fee $-\tau$, cooldown
  $F{=}3$ (small clock/hatch on the flushed wallet), then refills to full.
- Annotation near a rejected large arrow: drop, with two short tags
  "oversize $x_t>C/k$" (structural) vs "avoidable" (insufficient/conflict a
  proactive flush could prevent). Keep these conceptual, not numeric.
- A small note "flush executes before settle" to capture the single-step
  coupling.
- Reading order top-left to bottom-right; no paragraph of text inside the
  figure (short labels only).

Fig. 2 — structures.pdf (`fig:structures`)
- Four compact panels sharing one "state $s$ (per-wallet balance/avail/cooldown
  + $x_t$)" input block at top (draw the shared trunk once and branch to the 4).
  1. JA-PPO: trunk -> ONE joint softmax over $(a_s,a_f)$ -> big output block
     labelled $(k{+}1)^2 = 625$; optionally fade a few cells marked invalid
     (same-wallet flush+settle) to motivate factorization.
  2. IFAC: trunk -> two parallel independent heads, $\pi_s(a_s|s)$ and
     $\pi_f(a_f|s)$ -> two small output blocks, total $2(k{+}1)=50$.
  3. SC-FAC: same two heads, plus a dashed directed edge from the chosen
     settle action $a_s$ into the flush head; label settle$\to$flush.
  4. Set: wallets -> shared $\phi(\cdot)$ per wallet -> symmetric pooling
     ($\Sigma$/mean symbol) -> per-wallet logits; annotate "no $k$-shaped
     weight / permutation equivariant", and the same $50$ outputs.
- Put the big output-count contrast ($625$ vs $50$) in bold where natural.
- Keep panels aligned in a 2x2 or 1x4 grid that still stays legible at single
  column width (2x2 preferred given the 3.4-in width).

LaTeX swap (in paper/icassp2027/main.tex)
- Keep the exact `figure` environments, `\caption{...}` and `\label{...}` so
  every in-text reference and the table/figure numbering remain unchanged.
- Replace ONLY the entire `\figplaceholder{title}{height}{description}` command (its third argument spans several lines), keeping the surrounding figure/caption/label unchanged:

Fig. 1:
  \figplaceholder{Problem / environment overview}{1.45in}{...}
becomes
  \figpdf{overview.pdf}{0.95\columnwidth}

Fig. 2:
  \figplaceholder{Policy-structure comparison}{1.75in}{...}
becomes
  \figpdf{structures.pdf}{0.95\columnwidth}

- The `\figplaceholder` macro may stay defined but unused; delete it only if
  the author prefers. Do not change any caption text, label, number, or result.

Build + verification (after swapping)
1. `python scripts/make_concept_figures.py` -> confirm both PDFs exist and are
   non-trivial in size.
2. Clean rebuild in `paper/icassp2027/`: pdflatex, bibtex, pdflatex x2;
   require rc=0, still 4 technical pages + references-only p.5,
   0 undefined refs/cites, 0 overfull.
3. `pdffonts main.pdf`: all fonts embedded (avoid Type3 if practical; embed
   matplotlib fonts as TrueType, e.g. pdf.fonttype=42/ps.fonttype=42).
4. Render every page with pdftoppm and inspect Fig.1/Fig.2: labels legible at
   print size, no clipped text, boxes aligned, no overlap with captions/text.
5. Confirm the literal string "Figure placeholder" no longer appears:
   `pdftotext main.pdf - | grep -i "figure placeholder"` must return nothing.
6. Update FINAL_SUBMISSION_GATE.md section 6 to mark both figures real, then
   rebuild the FINAL submission PDF only after author metadata is filled.

Acceptance: both PDFs are self-explanatory without the paper, contain no
experimental numbers beyond the definitional $625/50$ and $C/k$/$F$/$\tau$,
match the notation in Sections 2-3, and the document remains a clean 4+1 page
build with zero undefined references.
