"""Compact single-column Fig.1 for the ICASSP manuscript: data-flow sketch of
one collateral-control decision. Redrawn natively (not a resize of the
two-column concept PNG). Labels are protocol facts only; no result numbers.

Writes paper/icassp2027/assets/figs/fig1_compact.pdf
"""
from pathlib import Path

import matplotlib
matplotlib.use("pdf")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle

matplotlib.rcParams["pdf.fonttype"] = 42
matplotlib.rcParams["ps.fonttype"] = 42

OUT = (Path(__file__).resolve().parents[1]
       / "paper" / "icassp2027" / "assets" / "figs" / "fig1_compact.pdf")

BLUE = "#dbe7f6"; BLUE_E = "#3b6ea5"
GREY = "#eef0f3"; GREY_E = "#5a6572"
PURP = "#e7e2f3"; PURP_E = "#5b4b9c"
ORNG = "#fde7d3"; ORNG_E = "#c96f1b"
GREEN = "#dcefdf"; GREEN_E = "#2e7d4f"

fig, ax = plt.subplots(figsize=(3.42, 2.5))
ax.set_xlim(0, 100); ax.set_ylim(0, 68); ax.axis("off")


def box(x, y, w, h, text, fc, ec, fs=7.2):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                 boxstyle="round,pad=0.5,rounding_size=2.0",
                 fc=fc, ec=ec, lw=1.1))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
            fontsize=fs, linespacing=1.3)


def arrow(x1, y1, x2, y2, color="#333333", lw=1.3):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2),
                 arrowstyle="-|>", mutation_scale=9, lw=lw, color=color))


def badge(x, y, n, ec):
    ax.add_patch(Circle((x, y), 2.4, fc="white", ec=ec, lw=1.3, zorder=5))
    ax.text(x, y, n, ha="center", va="center", fontsize=7.0,
            color=ec, weight="bold", zorder=6)


# ---- top row: arrival -> state -> policy -> planned actions ----
box(8, 48, 12, 11, r"$x_t$", BLUE, BLUE_E, fs=9)
box(24, 48, 12, 11, r"state $s_t$", GREY, GREY_E)
box(40, 48, 12, 11, "policy\n" + r"$\pi(a\mid s)$", PURP, PURP_E)
box(56, 48, 24, 11, r"$a_s,\ a_f$ planned", GREY, GREY_E, fs=7.4)
arrow(20.2, 53.5, 23.7, 53.5)
arrow(36.2, 53.5, 39.7, 53.5)
arrow(52.2, 53.5, 55.7, 53.5)

# ---- execution: 1st flush, then 2nd settle ----
arrow(66, 47.8, 66, 42.4, color=ORNG_E, lw=1.5)
box(56, 30, 24, 12, "flush $a_f$\nfee $-\\tau$\ncooldown $F{=}3$",
    ORNG, ORNG_E, fs=7.0)
badge(78.5, 42.6, "1", ORNG_E)
arrow(55.7, 36, 52.3, 36, color=ORNG_E, lw=1.5)
box(38, 30, 14, 12, "settle $a_s$", GREEN, GREEN_E, fs=7.4)
badge(50.5, 42.6, "2", ORNG_E)
arrow(37.7, 36, 35.3, 36)

# ---- outcomes ----
box(2, 27, 33, 14,
    "accept:  $+p\\,x_t$\n"
    "drop: oversize $\\cdot$ frozen\n"
    "avoidable (no penalty)",
    "#fbfbfb", "#777777", fs=6.8)

# ---- feedback s_{t+1} routed on the left ----
ax.add_patch(FancyArrowPatch((6.5, 41.2), (7.8, 52.8),
             arrowstyle="-|>", mutation_scale=9, lw=1.1, color=GREY_E,
             connectionstyle="arc3,rad=0.45"))
ax.text(1.6, 46.6, r"$s_{t+1}$", fontsize=7.2, style="italic")

fig.tight_layout(pad=0.2)
fig.savefig(OUT)
print("wrote", OUT)
