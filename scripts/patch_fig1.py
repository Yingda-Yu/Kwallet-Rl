"""Minimal semantic patch for Fig. 1 (user-provided conceptual artwork).

Fixes ONE semantic error only; does not redraw the figure:
  1. Remove the erroneous "-tau" printed under the Drop outcome.
  2. Add a small "flush fee -tau" label inside the Flush module.

Idempotent: always starts from the preserved fig1.original.png.
    python scripts/patch_fig1.py
"""
from pathlib import Path
import numpy as np
from PIL import Image
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

FIG_DIR = Path("paper/icassp2027/assets/figs")
SRC = FIG_DIR / "fig1.original.png"
DST = FIG_DIR / "fig1.png"


def main():
    im = Image.open(SRC).convert("RGB")
    a = np.asarray(im).astype(np.float32)

    # 1. erase "-tau" in the Drop panel (dashed separator y>=655 and red
    #    border x<=1300 excluded)
    # panel background is uniform light pink (253,239,239); solid fill
    # removes glyph and anti-aliased halo without touching the dashed
    # separator (y>=655) or the circle above (y<=614).
    x0, x1, y0, y1 = 1328, 1414, 622, 652
    a[y0:y1, x0:x1] = np.array([253, 239, 239], dtype=np.float32)
    out = Image.fromarray(a.astype(np.uint8))

    # 2. add "flush fee -tau" in the empty band inside the Flush module
    fig = plt.figure(figsize=(2.4, 0.34), dpi=300)
    fig.patch.set_alpha(0.0)
    fig.text(0.5, 0.5, r"$\mathrm{flush\ fee}\ \;-\tau$",
             ha="center", va="center", fontsize=15, color="#1f1a17")
    fig.savefig("/tmp/flush_fee.png", transparent=True, dpi=300,
                bbox_inches="tight", pad_inches=0.02)
    plt.close(fig)
    lab = Image.open("/tmp/flush_fee.png").convert("RGBA")
    th = 23
    lw = int(round(lab.width * th / lab.height))
    lab = lab.resize((lw, th), Image.LANCZOS)
    cx = (629 + 877) // 2
    px, py = cx - lw // 2, 644
    out.paste(lab, (px, py), lab)

    out.save(DST)
    print(f"wrote {DST} {out.size}; label x={px}..{px+lw}, y={py}..{py+th}")


if __name__ == "__main__":
    main()
