"""
Conceptual illustration figures for the Regression Overview section
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

# ---------------------------------------------------------------- linear vs logistic concept
fig, axes = plt.subplots(1, 2, figsize=(10.4, 4.4), dpi=170)
fig.patch.set_facecolor(SURFACE)

rng = np.random.default_rng(3)
ax = axes[0]
ax.set_facecolor(SURFACE)
x = np.linspace(0, 10, 40)
y = 2.2 * x + 3 + rng.normal(0, 2.4, size=40)
ax.scatter(x, y, s=16, color=BLUE, alpha=0.6, zorder=3)
xx = np.linspace(0, 10, 100)
ax.plot(xx, 2.2 * xx + 3, color=ORANGE, linewidth=2.2, zorder=4)
ax.set_title("Linear regression\npredicts a number", fontsize=12.5, color=INK, pad=8)
ax.set_xlabel("predictor", fontsize=9.5, color=MUTED)
ax.set_ylabel("continuous target", fontsize=9.5, color=MUTED)
ax.tick_params(labelsize=8, colors=MUTED)
for spine in ("top", "right"):
    ax.spines[spine].set_visible(False)
ax.spines["bottom"].set_color(GRID); ax.spines["left"].set_color(GRID)

ax = axes[1]
ax.set_facecolor(SURFACE)
x0 = rng.normal(2.5, 1.3, 20); x1 = rng.normal(7.5, 1.3, 20)
ax.scatter(x0, np.zeros(20) + rng.normal(0, 0.02, 20), s=16, color=BLUE, alpha=0.7, zorder=3, label="class 0")
ax.scatter(x1, np.ones(20) + rng.normal(0, 0.02, 20), s=16, color=ORANGE, alpha=0.7, zorder=3, label="class 1")
xx = np.linspace(-1, 11, 200)
sig = 1 / (1 + np.exp(-(xx - 5)))
ax.plot(xx, sig, color=INK, linewidth=2.2, zorder=4)
ax.axhline(0.5, color=MUTED, linestyle="--", linewidth=1, zorder=2)
ax.set_title("Logistic regression\npredicts a probability, then a class", fontsize=12.5, color=INK, pad=8)
ax.set_xlabel("predictor", fontsize=9.5, color=MUTED)
ax.set_ylabel("P(class = 1)", fontsize=9.5, color=MUTED)
ax.set_ylim(-0.15, 1.15)
ax.legend(fontsize=8.5, frameon=False, loc="center left")
ax.tick_params(labelsize=8, colors=MUTED)
for spine in ("top", "right"):
    ax.spines[spine].set_visible(False)
ax.spines["bottom"].set_color(GRID); ax.spines["left"].set_color(GRID)

fig.tight_layout()
fig.savefig(f"{IMG_DIR}/theory-linear-vs-logistic.png", facecolor=SURFACE, bbox_inches="tight")
plt.close(fig)

# ---------------------------------------------------------------- sigmoid curve, labeled
fig, ax = plt.subplots(figsize=(7.4, 4.6), dpi=170)
fig.patch.set_facecolor(SURFACE)
ax.set_facecolor(SURFACE)
z = np.linspace(-8, 8, 300)
sig = 1 / (1 + np.exp(-z))
ax.plot(z, sig, color=BLUE, linewidth=2.4, zorder=3)
ax.axhline(0.5, color=MUTED, linestyle="--", linewidth=1, zorder=2)
ax.axvline(0, color=MUTED, linestyle="--", linewidth=1, zorder=2)
ax.annotate("predict class 1\nabove this line", xy=(4, 0.5), xytext=(2.6, 0.18),
            fontsize=9.5, color=INK, ha="center",
            arrowprops=dict(arrowstyle="-|>", color=MUTED, linewidth=1.1))
ax.set_xlabel("z = linear score (intercept + weighted sum of predictors)", fontsize=10, color=INK)
ax.set_ylabel("sigmoid(z) = 1 / (1 + e⁻ᶻ)  =  P(class = 1)", fontsize=10, color=INK)
ax.set_title("The sigmoid function turns any linear score into a 0-1 probability", fontsize=12.5, color=INK, pad=12)
ax.grid(color=GRID, linewidth=0.8, zorder=0)
for spine in ("top", "right"):
    ax.spines[spine].set_visible(False)
ax.spines["bottom"].set_color(GRID); ax.spines["left"].set_color(GRID)
fig.tight_layout()
fig.savefig(f"{IMG_DIR}/theory-sigmoid.png", facecolor=SURFACE)
plt.close(fig)

print("wrote theory-linear-vs-logistic.png, theory-sigmoid.png")
