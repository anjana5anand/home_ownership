"""
Conceptual illustration figures for the AdaBoost Overview section
(not computed from the project data, purely explanatory diagrams).
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

IMG_DIR = "docs/images"
BLUE = "#2a78d6"
ORANGE = "#eb6834"
GREEN = "#4ea35a"
SURFACE = "#fcfcfb"
INK = "#0b0b0b"
MUTED = "#5a544c"
GRID = "#e7e3dc"

# ---------------------------------------------------------------- bagging vs boosting
fig, axes = plt.subplots(1, 2, figsize=(10.6, 4.6), dpi=170)
fig.patch.set_facecolor(SURFACE)

def tree_box(ax, x, y, label, color=BLUE, w=1.05, h=0.6, fontsize=9.5):
    ax.add_patch(plt.Rectangle((x - w / 2, y - h / 2), w, h, facecolor=color, edgecolor="none", zorder=3))
    ax.text(x, y, label, ha="center", va="center", color="white", fontsize=fontsize, fontweight="bold", zorder=4)

ax = axes[0]
ax.set_facecolor(SURFACE); ax.axis("off")
ax.set_xlim(0, 10); ax.set_ylim(0, 6.6)
ax.text(5, 6.1, "Bagging: independent trees, same full data\nvote or average at the end", ha="center",
        fontsize=10.5, color=INK, linespacing=1.4)
ax.text(5, 5.1, "full training data", ha="center", fontsize=8.5, color=MUTED)
for i, x in enumerate([2, 5, 8]):
    ax.annotate("", xy=(x, 3.9), xytext=(5, 4.85), arrowprops=dict(arrowstyle="-", color=MUTED, linewidth=1.1))
    tree_box(ax, x, 3.55, f"Tree {i+1}", BLUE)
    ax.annotate("", xy=(5, 1.65), xytext=(x, 3.2), arrowprops=dict(arrowstyle="-", color=MUTED, linewidth=1.1))
tree_box(ax, 5, 1.2, "final vote", GREEN, w=1.5)

ax = axes[1]
ax.set_facecolor(SURFACE); ax.axis("off")
ax.set_xlim(0, 10); ax.set_ylim(0, 6.6)
ax.text(5, 6.1, "Boosting: trees built one after another,\neach reweighting the last one's mistakes", ha="center",
        fontsize=10.5, color=INK, linespacing=1.4)
xs = [1.3, 3.7, 6.1, 8.6]
labels = ["Stump 1", "Stump 2", "Stump 3", "⋯"]
for i in range(3):
    tree_box(ax, xs[i], 4.4, labels[i], ORANGE, w=1.05)
    ax.annotate("", xy=(xs[i + 1] - 0.56, 4.4), xytext=(xs[i] + 0.56, 4.4),
                arrowprops=dict(arrowstyle="-|>", color=MUTED, linewidth=1.1))
    ax.text((xs[i] + xs[i + 1]) / 2, 4.75, "reweight\nmisses", fontsize=7, color=MUTED, ha="center", va="bottom", linespacing=1.2)
ax.text(xs[-1], 4.4, labels[-1], ha="center", va="center", fontsize=14, color=MUTED)
for x in xs[:3]:
    ax.annotate("", xy=(5, 1.65), xytext=(x, 4.1), arrowprops=dict(arrowstyle="-", color=MUTED, linewidth=1.1))
tree_box(ax, 5, 1.2, "weighted vote\n(αᵢ per stump)", GREEN, w=2.1, fontsize=9)

fig.tight_layout()
fig.savefig(f"{IMG_DIR}/theory-bagging-vs-boosting.png", facecolor=SURFACE, bbox_inches="tight")
plt.close(fig)

# ---------------------------------------------------------------- decision stump + reweighting illustration
rng = np.random.default_rng(11)
fig, axes = plt.subplots(1, 3, figsize=(11.6, 4), dpi=170)
fig.patch.set_facecolor(SURFACE)

x0 = rng.normal(3, 1.1, 18); y0 = rng.normal(3, 1.1, 18)
x1 = rng.normal(7, 1.1, 18); y1 = rng.normal(6, 1.1, 18)
sizes = np.full(18, 40.0)

titles = ["Round 1: equal weights\nstump misses a few points",
          "Round 2: missed points up-weighted\n(drawn bigger), stump adapts",
          "Round 3: still-missed points\nup-weighted again"]
miss_idx = [3, 9, 14]
for k, ax in enumerate(axes):
    ax.set_facecolor(SURFACE)
    s0 = sizes.copy(); s1 = sizes.copy()
    if k > 0:
        s0[miss_idx] *= 2.6
    if k > 1:
        s0[miss_idx[:2]] *= 1.6
    ax.scatter(x0, y0, s=s0, color=BLUE, alpha=0.75, zorder=3, edgecolor="white", linewidth=0.6)
    ax.scatter(x1, y1, s=s1, color=ORANGE, alpha=0.75, zorder=3, edgecolor="white", linewidth=0.6)
    thresh = 4.6 - 0.25 * k
    ax.axvline(thresh, color=INK, linestyle="--", linewidth=1.6, zorder=2)
    ax.set_title(titles[k], fontsize=9.5, color=INK, pad=8)
    ax.set_xticks([]); ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

fig.suptitle("A decision stump is a depth-1 tree: one split, two leaves", fontsize=12.5, color=INK, y=1.04)
fig.tight_layout()
fig.savefig(f"{IMG_DIR}/theory-stump-reweighting.png", facecolor=SURFACE, bbox_inches="tight")
plt.close(fig)

print("wrote theory-bagging-vs-boosting.png, theory-stump-reweighting.png")
