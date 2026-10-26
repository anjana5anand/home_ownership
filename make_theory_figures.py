"""
Conceptual illustration figures for the Naive Bayes and Decision Trees
Overview sections (not computed from the project data, purely
explanatory diagrams).
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

# ---------------------------------------------------------------- NB: multinomial vs bernoulli feature view
fig, axes = plt.subplots(1, 2, figsize=(10, 4.4), dpi=170)
fig.patch.set_facecolor(SURFACE)

rng = np.random.default_rng(7)
ax = axes[0]
ax.set_facecolor(SURFACE)
counts = rng.integers(0, 6, size=(5, 4))
im = ax.imshow(counts, cmap="Oranges", vmin=0, vmax=6)
for i in range(5):
    for j in range(4):
        ax.text(j, i, counts[i, j], ha="center", va="center", fontsize=10,
                color="white" if counts[i, j] > 3 else INK)
ax.set_xticks(range(4)); ax.set_xticklabels([f"bin {k}" for k in range(4)], fontsize=9, color=MUTED)
ax.set_yticks(range(5)); ax.set_yticklabels([f"metro {k+1}" for k in range(5)], fontsize=9, color=MUTED)
ax.set_title("Multinomial NB\nfeatures are counts (how many / which bin)", fontsize=11.5, color=INK)

ax = axes[1]
ax.set_facecolor(SURFACE)
bins = rng.integers(0, 2, size=(5, 4))
im = ax.imshow(bins, cmap="Blues", vmin=0, vmax=1)
for i in range(5):
    for j in range(4):
        ax.text(j, i, bins[i, j], ha="center", va="center", fontsize=10,
                color="white" if bins[i, j] == 1 else INK)
ax.set_xticks(range(4)); ax.set_xticklabels([f"feature {k+1}" for k in range(4)], fontsize=9, color=MUTED)
ax.set_yticks(range(5)); ax.set_yticklabels([f"metro {k+1}" for k in range(5)], fontsize=9, color=MUTED)
ax.set_title("Bernoulli NB\nfeatures are 0/1 (present / absent, above / below)", fontsize=11.5, color=INK)

fig.suptitle("Two ways Naive Bayes can see the same data", fontsize=13, color=INK, y=1.04)
fig.tight_layout()
fig.savefig(f"{IMG_DIR}/theory-nb-feature-types.png", facecolor=SURFACE, bbox_inches="tight")
plt.close(fig)

# ---------------------------------------------------------------- NB: independence assumption diagram
fig, ax = plt.subplots(figsize=(7.4, 4.2), dpi=170)
fig.patch.set_facecolor(SURFACE)
ax.set_facecolor(SURFACE)
ax.axis("off")
ax.text(0.5, 0.92, "class C", ha="center", fontsize=14, color=INK, fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.4", fc=ORANGE, ec="none", alpha=0.85))
feat_x = [0.12, 0.37, 0.62, 0.87]
labels = ["1yr chg %", "3yr chg %", "5yr chg %", "volatility"]
for x, lab in zip(feat_x, labels):
    ax.annotate("", xy=(x, 0.55), xytext=(0.5, 0.86),
                arrowprops=dict(arrowstyle="-|>", color=MUTED, linewidth=1.3))
    ax.text(x, 0.45, lab, ha="center", fontsize=10.5, color=INK,
            bbox=dict(boxstyle="round,pad=0.35", fc=BLUE, ec="none", alpha=0.18))
ax.text(0.5, 0.08, "Naive Bayes assumes every feature is conditionally\nindependent of the others, given the class",
        ha="center", fontsize=11, color=MUTED, style="italic")
fig.tight_layout()
fig.savefig(f"{IMG_DIR}/theory-nb-independence.png", facecolor=SURFACE)
plt.close(fig)

# ---------------------------------------------------------------- DT: gini/entropy impurity curves
p = np.linspace(0.001, 0.999, 400)
gini_curve = 1 - (p**2 + (1 - p)**2)
entropy_curve = -(p * np.log2(p) + (1 - p) * np.log2(1 - p))

fig, ax = plt.subplots(figsize=(7.2, 4.6), dpi=170)
fig.patch.set_facecolor(SURFACE)
ax.set_facecolor(SURFACE)
ax.plot(p, gini_curve, color=BLUE, linewidth=2.3, label="Gini impurity: 1 − Σ pᵢ²")
ax.plot(p, entropy_curve, color=ORANGE, linewidth=2.3, label="Entropy: −Σ pᵢ log₂ pᵢ")
ax.set_xlabel("p (fraction of class 1 in a node, two-class case)", fontsize=10.5, color=INK)
ax.set_ylabel("impurity", fontsize=11, color=INK)
ax.set_title("Gini impurity and entropy both peak at a 50/50 split\nand fall to zero when a node is pure", fontsize=12.5, color=INK, pad=10)
ax.legend(fontsize=10, frameon=False)
ax.grid(axis="y", color=GRID, linewidth=0.8, zorder=0)
for spine in ("top", "right"):
    ax.spines[spine].set_visible(False)
ax.spines["bottom"].set_color(GRID); ax.spines["left"].set_color(GRID)
fig.tight_layout()
fig.savefig(f"{IMG_DIR}/theory-gini-entropy.png", facecolor=SURFACE)
plt.close(fig)

print("wrote theory-nb-feature-types.png, theory-nb-independence.png, theory-gini-entropy.png")
