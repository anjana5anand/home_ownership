import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

IMG_DIR = "docs/images"
SURFACE = "#fcfcfb"
INK = "#0b0b0b"
MUTED = "#5a544c"
BLUE = "#2a78d6"
ORANGE = "#eb6834"
GREEN = "#4ea35a"

fig, ax = plt.subplots(figsize=(8, 5), dpi=170)
fig.patch.set_facecolor(SURFACE)
ax.set_facecolor(SURFACE)
ax.axis("off")
ax.set_xlim(0, 10); ax.set_ylim(0, 6)

def node(x, y, text, color, w=2.6, h=0.9):
    ax.add_patch(plt.Rectangle((x - w/2, y - h/2), w, h, facecolor=color, edgecolor="none", alpha=0.85, zorder=3))
    ax.text(x, y, text, ha="center", va="center", fontsize=9.5, color="white" if color != "#fce8d8" else INK, zorder=4, fontweight="bold")

node(5, 5, "root: split on\nfeature A ≤ t", "#5a544c")
node(2.2, 3, "split on\nfeature B ≤ t2", BLUE)
node(7.8, 3, "leaf: class = Burdened", ORANGE)
node(0.9, 1, "leaf: Affordable", "#9bc6f0")
node(3.5, 1, "leaf: Moderate", "#f5c9a3")

for (x1, y1, x2, y2) in [(5, 4.55, 2.2, 3.45), (5, 4.55, 7.8, 3.45), (2.2, 2.55, 0.9, 1.45), (2.2, 2.55, 3.5, 1.45)]:
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle="-", color=MUTED, linewidth=1.3), zorder=2)

ax.text(3.6, 3.9, "yes", fontsize=9, color=MUTED, style="italic")
ax.text(6.4, 3.9, "no", fontsize=9, color=MUTED, style="italic")
ax.text(1.55, 1.9, "yes", fontsize=9, color=MUTED, style="italic")
ax.text(2.85, 1.9, "no", fontsize=9, color=MUTED, style="italic")

ax.set_title("A decision tree is a sequence of yes/no splits\nending in a predicted class at each leaf", fontsize=12.5, color=INK, pad=14)
fig.tight_layout()
fig.savefig(f"{IMG_DIR}/theory-decision-tree-concept.png", facecolor=SURFACE)
print("wrote theory-decision-tree-concept.png")
