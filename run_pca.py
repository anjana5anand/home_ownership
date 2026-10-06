"""
PCA on the same standardized 2025 metro panel used for clustering.
=======================================================================
Reports eigenvalues/eigenvectors (via sklearn's explained_variance_ and
components_, which are exactly the eigenvalues and eigenvectors of the
feature correlation matrix once the inputs are standardized), a scree
plot, and a biplot relating the original variables to the first two
components.

Run: python3 run_pca.py   (after prep_unsupervised_data.py)
Writes figures to docs/images/, a loadings table to data_clean/.
"""
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os

OUT_DIR = "data_clean"
IMG_DIR = "docs/images"
os.makedirs(IMG_DIR, exist_ok=True)

BLUE = "#2a78d6"
ORANGE = "#eb6834"
SURFACE = "#fcfcfb"
INK = "#0b0b0b"
MUTED = "#5a544c"
GRID = "#e7e3dc"

LABELS = {
    "zhvi": "Home value",
    "zhvi_yoy_pct": "1yr price chg",
    "zhvi_3yr_pct": "3yr price chg",
    "zhvi_5yr_pct": "5yr price chg",
    "zhvi_volatility_5yr": "Price volatility",
    "zhvi_vs_national": "Price vs national",
    "zhvi_pctile_in_year": "Price percentile",
    "price_to_income_25_34": "Price-to-income",
    "years_to_down_payment_25_34": "Years to down pmt",
    "monthly_payment_usd": "Monthly payment",
    "payment_to_income_pct_25_34": "Payment % income",
}

scaled = pd.read_csv(f"{OUT_DIR}/metro_2025_unsupervised_scaled.csv")
feature_cols = [c for c in scaled.columns if c not in ("region_name", "state_name")]
X = scaled[feature_cols].to_numpy()
n_features = len(feature_cols)

pca = PCA(n_components=n_features, random_state=42)
coords = pca.fit_transform(X)

eigenvalues = pca.explained_variance_          # eigenvalues of the correlation matrix
eigenvectors = pca.components_                 # rows are eigenvectors (loadings), already unit length
explained = pca.explained_variance_ratio_
cum_explained = np.cumsum(explained)

load_df = pd.DataFrame(eigenvectors[:2].T, index=feature_cols, columns=["PC1", "PC2"]).round(3)
load_df.to_csv(f"{OUT_DIR}/pca-loadings-pc1-pc2.csv")

n_pc_for_90 = int(np.searchsorted(cum_explained, 0.90) + 1)
print("eigenvalues:", np.round(eigenvalues, 3))
print("explained variance ratio:", np.round(explained, 3))
print(f"components needed for 90% variance: {n_pc_for_90} (of {n_features} original features)")

# ------------------------------------------------------------------ scree plot
fig, ax1 = plt.subplots(figsize=(7.4, 4.6), dpi=170)
fig.patch.set_facecolor(SURFACE)
ax1.set_facecolor(SURFACE)
pcs = np.arange(1, n_features + 1)
ax1.bar(pcs, explained * 100, color=BLUE, alpha=0.85, zorder=2)
ax1.set_xlabel("principal component", fontsize=11, color=INK)
ax1.set_ylabel("% variance explained", fontsize=11, color=BLUE)
ax1.set_xticks(pcs)
ax1.tick_params(axis="y", colors=BLUE)
ax1.spines["top"].set_visible(False)
ax1.spines["left"].set_color(GRID)
ax1.spines["bottom"].set_color(GRID)
ax1.spines["right"].set_visible(False)
ax1.grid(axis="y", color=GRID, linewidth=0.8, zorder=0)

ax2 = ax1.twinx()
ax2.plot(pcs, cum_explained * 100, color=ORANGE, marker="o", markersize=5, linewidth=2, zorder=3)
ax2.axhline(90, color=MUTED, linestyle="--", linewidth=1)
ax2.set_ylabel("cumulative % variance", fontsize=11, color=ORANGE)
ax2.tick_params(axis="y", colors=ORANGE)
ax2.set_ylim(0, 105)
ax2.spines["top"].set_visible(False)

fig.suptitle("Scree plot: eigenvalues of the 11-feature correlation matrix, by component", fontsize=12.5, color=INK)
fig.tight_layout()
fig.savefig(f"{IMG_DIR}/pca-scree.png", facecolor=SURFACE)
plt.close(fig)

# ------------------------------------------------------------------ biplot
fig, ax = plt.subplots(figsize=(7.8, 7.0), dpi=170)
fig.patch.set_facecolor(SURFACE)
ax.set_facecolor(SURFACE)

xs = coords[:, 0] / coords[:, 0].std()
ys = coords[:, 1] / coords[:, 1].std()
ax.scatter(xs, ys, s=10, color=BLUE, alpha=0.35, linewidths=0, zorder=2)

scale = 4.0
vecs = eigenvectors[:2, :].T * scale  # (n_features, 2)

# Several engineered columns are near-perfectly collinear with zhvi itself
# (price-to-income, monthly payment, etc. are all simple rescalings of the
# same home-value number against a national income/rate that's constant
# across metros in a single year) so their arrows land on almost the same
# point. Group those together rather than stacking unreadable labels.
groups = []
used = set()
for i in range(len(feature_cols)):
    if i in used:
        continue
    group = [i]
    used.add(i)
    for j in range(i + 1, len(feature_cols)):
        if j in used:
            continue
        if np.linalg.norm(vecs[i] - vecs[j]) < 0.4:
            group.append(j)
            used.add(j)
    groups.append(group)

for group in groups:
    vx, vy = vecs[group[0]]
    ax.annotate("", xy=(vx, vy), xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color=ORANGE, linewidth=1.6), zorder=4)
    names = [LABELS.get(feature_cols[i], feature_cols[i]) for i in group]
    label_text = "\n".join(names)
    tx, ty = vx * 1.18, vy * 1.18
    ha = "left" if vx >= 0 else "right"
    va = "bottom" if vy >= 0 else "top"
    ax.text(tx, ty, label_text, fontsize=9, color="#7a4530",
            ha=ha, va=va, fontweight="medium", zorder=5, linespacing=1.5)

ax.axhline(0, color=GRID, linewidth=0.8, zorder=1)
ax.axvline(0, color=GRID, linewidth=0.8, zorder=1)
ax.set_xlabel(f"PC1 ({explained[0]*100:.1f}% of variance)", fontsize=11, color=INK)
ax.set_ylabel(f"PC2 ({explained[1]*100:.1f}% of variance)", fontsize=11, color=INK)
ax.set_title("Biplot: metro areas and variable loadings on PC1/PC2", fontsize=13, color=INK, pad=18)

ymin, ymax = ax.get_ylim()
ax.set_ylim(ymin, ymax + 0.22 * (ymax - ymin))

for spine in ("top", "right"):
    ax.spines[spine].set_visible(False)
ax.spines["left"].set_color(GRID)
ax.spines["bottom"].set_color(GRID)
fig.tight_layout()
fig.subplots_adjust(top=0.90)
fig.savefig(f"{IMG_DIR}/pca-biplot.png", facecolor=SURFACE)
plt.close(fig)

print("DONE")
print("n_pc_for_90 =", n_pc_for_90)
