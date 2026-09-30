"""Draw the two conceptual/schematic figures for the ICASSP 2027 paper.

Data-free and deterministic: no experimental results are used or drawn.
The only quantities shown are definitional ones already in the manuscript:
k wallets, capacity C/k, fee tau, cooldown F=3, (k+1)^2 = 625 vs 2(k+1) = 50.

Outputs (vector PDF, TrueType fonts, grayscale-legible):
    paper/icassp2027/assets/figs/overview.pdf
    paper/icassp2027/assets/figs/structures.pdf
"""
from pathlib import Path

import matplotlib
matplotlib.use("pdf")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle

# embed fonts as TrueType (no Type 3, no bitmap)
matplotlib.rcParams["pdf.fonttype"] = 42
matplotlib.rcParams["ps.fonttype"] = 42
matplotlib.rcParams["font.family"] = "DejaVu Sans"
matplotlib.rcParams["font.size"] = 8

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "paper" / "icassp2027" / "assets" / "figs"

BLACK = "#111111"
GRAY = "#555555"
FILL = "#d6d6d6"
FILL_EDGE = "#333333"


def _box(ax, x, y, w, h, text, fs=7, bold=False, hatch=None, fc="white",
         ec=BLACK, lw=0.9, ls="-"):
    """Rectangle with centred text; (x, y) is the lower-left corner."""
    ax.add_patch(Rectangle((x, y), w, h, facecolor=fc, edgecolor=ec, lw=lw,
                           linestyle=ls, hatch=hatch))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs,
            fontweight="bold" if bold else "normal", linespacing=1.05)


def _arrow(ax, p0, p1, color=BLACK, ls="-", lw=1.0, ms=7, rad=0.0):
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle="-|>", mutation_scale=ms,
                                 lw=lw, color=color, linestyle=ls, shrinkA=0,
                                 shrinkB=0,
                                 connectionstyle="arc3,rad=%s" % rad))


def _line(ax, xs, ys, color=BLACK, lw=0.8, ls="-"):
    ax.plot(xs, ys, color=color, lw=lw, linestyle=ls, solid_capstyle="round")


# ---------------------------------------------------------------------------
# Fig. 1 -- overview of the streaming collateral-control problem
# ---------------------------------------------------------------------------
def overview():
    fig, ax = plt.subplots(figsize=(3.4, 2.0))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    # -- streaming arrivals on a horizontal time axis --
    _arrow(ax, (0.03, 0.90), (0.47, 0.90), lw=1.0)
    for xx, lab in [(0.055, "$x_1$"), (0.135, "$x_2$"), (0.215, "$\\dots$")]:
        _box(ax, xx, 0.845, 0.062, 0.085, lab, fs=7)
    _box(ax, 0.32, 0.845, 0.07, 0.085, "$x_t$", fs=7.5, bold=True, fc=FILL)
    ax.text(0.03, 0.965, "streaming transactions", fontsize=7,
            style="italic", color=GRAY)

    # current transaction descends
    _arrow(ax, (0.355, 0.845), (0.355, 0.74), lw=1.0)

    # -- stack of k wallets (subset drawn; label says k) --
    x0, ww, hh = 0.55, 0.22, 0.078
    gap = 0.024
    fills = [0.9, 0.45, 0.72, 0.0, 0.58, 0.85]
    cooling_idx = 3
    ys = []
    for j in range(6):
        yy = 0.165 + j * (hh + gap)
        ys.append(yy)
        _box(ax, x0, yy, ww, hh, "", ec=FILL_EDGE)
        if j == cooling_idx:
            _box(ax, x0, yy, ww, hh, "", ec=GRAY, hatch="////", lw=0.8)
        else:
            f = fills[j]
            if f > 0:
                ax.add_patch(Rectangle((x0 + 0.006, yy + 0.006),
                                       (ww - 0.012) * f, hh - 0.012,
                                       facecolor=FILL, edgecolor="none"))
    ax.text(0.55, 0.855, "$k$ wallets,", fontsize=7, ha="left", va="center")
    ax.text(0.55, 0.818, "capacity $C/k$", fontsize=7, ha="left", va="center")

    # settle arrow: x_t into a wallet that fits, payoff +p x_t
    _arrow(ax, (0.355, 0.74), (x0, ys[4] + hh / 2), rad=-0.22, lw=1.1)
    ax.text(0.40, 0.80, "settle", fontsize=7, color=BLACK)
    ax.text(0.40, 0.755, "$+p\\,x_t$", fontsize=7, color=BLACK)

    # flush arrow into a three-line annotation box on the right
    fx, fy, fw, fh = 0.80, 0.425, 0.185, 0.15
    _arrow(ax, (x0 + ww, ys[cooling_idx] + hh / 2), (fx, fy + fh / 2),
           color=GRAY, ls=(0, (4, 2)), lw=1.0, ms=6)
    _box(ax, fx, fy, fw, fh, "flush\n$-\\tau$\ncooldown $F=3$", fs=5.6,
         ec=GRAY)

    # -- rejected transactions: structural vs avoidable --
    ax.plot([0.045, 0.105], [0.305, 0.355], color=GRAY, lw=0.9)
    ax.plot([0.045, 0.105], [0.355, 0.305], color=GRAY, lw=0.9)
    ax.text(0.12, 0.33, "oversize drop: $x_t>C/k$", fontsize=7, va="center",
            color=GRAY)
    ax.plot([0.045, 0.105], [0.16, 0.21], color=GRAY, lw=0.9)
    ax.plot([0.045, 0.105], [0.21, 0.16], color=GRAY, lw=0.9)
    ax.text(0.12, 0.225, "avoidable drop (balance,", fontsize=6.8,
            va="center", color=GRAY)
    ax.text(0.12, 0.18, "flush$-$settle conflict)", fontsize=6.8,
            va="center", color=GRAY)

    # single-step coupling note
    ax.text(0.5, 0.045, "flush executes before settle within a step",
            ha="center", fontsize=7, style="italic", color=BLACK)

    fig.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
    fig.savefig(FIG / "overview.pdf")
    plt.close(fig)


# ---------------------------------------------------------------------------
# Fig. 2 -- comparison of policy parameterizations (2x2)
# ---------------------------------------------------------------------------
def structures():
    fig, ax = plt.subplots(figsize=(3.4, 2.3))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    frames = [(0.02, 0.46, 0.46, 0.26), (0.52, 0.46, 0.46, 0.26),
              (0.02, 0.05, 0.46, 0.31), (0.52, 0.05, 0.46, 0.31)]
    for fx, fy, fw, fh in frames:
        ax.add_patch(Rectangle((fx, fy), fw, fh, facecolor="none",
                               edgecolor="#999999", lw=0.7))

    # shared state block
    _box(ax, 0.29, 0.90, 0.42, 0.095,
         "state $s$: wallet balances,\navailability, cooldown, $x_t$", fs=6.5)

    # branch via the central inter-column gutter; entries avoid title text
    jl, jr = (0.42, 0.745), (0.95, 0.745)
    _arrow(ax, (0.5, 0.90), jl, lw=0.9, ms=6)
    _arrow(ax, (0.5, 0.90), jr, lw=0.9, ms=6)
    _arrow(ax, jl, (0.42, 0.72), lw=0.8, ms=5)
    _arrow(ax, jr, (0.95, 0.72), lw=0.8, ms=5)
    # left bottom entry, routed through the center gutter
    _line(ax, [0.42, 0.50], [0.745, 0.745])
    _line(ax, [0.50, 0.50], [0.745, 0.41])
    _line(ax, [0.50, 0.445], [0.41, 0.41])
    _arrow(ax, (0.445, 0.41), (0.445, 0.36), lw=0.8, ms=5)
    # right bottom entry
    _line(ax, [0.95, 0.50], [0.745, 0.745])
    _line(ax, [0.50, 0.95], [0.41, 0.41])
    _arrow(ax, (0.95, 0.41), (0.95, 0.36), lw=0.8, ms=5)

    # ---- JA-PPO (top-left) ----
    ax.text(0.032, 0.70, "JA-PPO: joint head", fontsize=7.5,
            fontweight="bold", ha="left", va="top")
    _box(ax, 0.04, 0.535, 0.085, 0.07, "trunk", fs=6.5)
    _arrow(ax, (0.125, 0.57), (0.155, 0.57), lw=0.8, ms=5)
    gx, gy, gw, gh = 0.155, 0.51, 0.16, 0.13
    ax.add_patch(Rectangle((gx, gy), gw, gh, facecolor="white", edgecolor=BLACK,
                           lw=0.9))
    for r in range(4):
        for c in range(4):
            ccx = gx + 0.008 + c * (gw - 0.016) / 4
            ccy = gy + 0.008 + r * (gh - 0.016) / 4
            ax.add_patch(Rectangle((ccx, ccy), (gw - 0.016) / 4,
                                   (gh - 0.016) / 4, facecolor="none",
                                   edgecolor="#888888", lw=0.4))
    for r, c in [(1, 1), (2, 3)]:
        ccx = gx + 0.008 + c * (gw - 0.016) / 4
        ccy = gy + 0.008 + r * (gh - 0.016) / 4
        ax.add_patch(Rectangle((ccx, ccy), (gw - 0.016) / 4,
                               (gh - 0.016) / 4, facecolor=FILL,
                               edgecolor="none", hatch="///"))
    ax.text(0.25, 0.485,
            "joint softmax: $\\mathbf{(k{+}1)^2 = 625}$",
            ha="center", va="center", fontsize=6.2)
    ax.text(0.435, 0.575, "invalid", fontsize=5.5, color=GRAY,
            ha="center", va="center", rotation=90)

    # ---- IFAC (top-right) ----
    ax.text(0.532, 0.70, "IFAC: independent heads", fontsize=7.5,
            fontweight="bold", ha="left", va="top")
    _box(ax, 0.54, 0.545, 0.085, 0.07, "trunk", fs=6.5)
    _box(ax, 0.67, 0.62, 0.135, 0.062, "$\\pi_s(a_s\\mid s)$", fs=6.2)
    _box(ax, 0.67, 0.50, 0.135, 0.062, "$\\pi_f(a_f\\mid s)$", fs=6.2)
    _arrow(ax, (0.625, 0.58), (0.67, 0.651), lw=0.8, ms=5, rad=-0.15)
    _arrow(ax, (0.625, 0.58), (0.67, 0.531), lw=0.8, ms=5, rad=0.15)
    ax.text(0.905, 0.56, "$\\mathbf{2(k{+}1) = 50}$", fontsize=6.5,
            ha="center", va="center")

    # ---- SC-FAC (bottom-left) ----
    ax.text(0.032, 0.345, "SC-FAC: conditioned heads", fontsize=7.5,
            fontweight="bold", ha="left", va="top")
    _box(ax, 0.04, 0.17, 0.085, 0.07, "trunk", fs=6.5)
    _box(ax, 0.16, 0.24, 0.135, 0.062, "$\\pi_s(a_s\\mid s)$", fs=6.2)
    _box(ax, 0.16, 0.095, 0.135, 0.062, "$\\pi_f(a_f\\mid s,a_s)$", fs=5.8)
    _arrow(ax, (0.125, 0.205), (0.16, 0.271), lw=0.8, ms=5, rad=-0.15)
    _arrow(ax, (0.125, 0.205), (0.16, 0.126), lw=0.8, ms=5, rad=0.15)
    _arrow(ax, (0.227, 0.24), (0.227, 0.157), color=GRAY, ls=(0, (3, 2)),
           lw=0.9, ms=5)
    ax.text(0.40, 0.215, "$\\mathbf{50}$ outputs", fontsize=6.5,
            ha="center", va="center")
    ax.text(0.40, 0.172, "settle$\\to$flush", fontsize=5.8, color=GRAY,
            ha="center", va="center")

    # ---- Set encoder (bottom-right) ----
    ax.text(0.532, 0.345, "Set: equivariant encoder", fontsize=7.5,
            fontweight="bold", ha="left", va="top")
    _box(ax, 0.54, 0.24, 0.06, 0.052, "$w_1$", fs=6)
    _box(ax, 0.54, 0.15, 0.06, 0.052, "$w_2$", fs=6)
    _box(ax, 0.63, 0.14, 0.072, 0.14, "shared\n$\\phi(\\cdot)$", fs=6)
    _arrow(ax, (0.60, 0.266), (0.63, 0.245), lw=0.7, ms=4)
    _arrow(ax, (0.60, 0.176), (0.63, 0.19), lw=0.7, ms=4)
    _box(ax, 0.735, 0.188, 0.048, 0.055, "$\\mathbf{\\Sigma}$", fs=8)
    _arrow(ax, (0.702, 0.21), (0.735, 0.216), lw=0.8, ms=5)
    _box(ax, 0.805, 0.175, 0.16, 0.066, "per-wallet\nlogits", fs=5.5)
    _arrow(ax, (0.783, 0.216), (0.805, 0.21), lw=0.8, ms=5)
    ax.text(0.54, 0.085, "no $k$-shaped weight;", fontsize=6, color=GRAY,
            ha="left", va="center")
    ax.text(0.54, 0.052, "symmetric pooling", fontsize=6, color=GRAY,
            ha="left", va="center")
    ax.text(0.93, 0.062, "$\\mathbf{50}$", fontsize=7, ha="center",
            va="center")

    fig.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
    fig.savefig(FIG / "structures.pdf")
    plt.close(fig)


def main():
    FIG.mkdir(parents=True, exist_ok=True)
    overview()
    structures()
    for name in ("overview.pdf", "structures.pdf"):
        p = FIG / name
        print("%s  %d bytes" % (p, p.stat().st_size))


if __name__ == "__main__":
    main()
