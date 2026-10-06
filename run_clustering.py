"""
Clustering: k-means (several k) + hierarchical clustering with cosine
distance, compared via the Silhouette method and the Adjusted Rand Index.
=======================================================================
Run: python3 run_clustering.py   (after prep_unsupervised_data.py)
Writes figures to docs/images/, a cluster-profile table to data_clean/.
"""
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, silhouette_samples, adjusted_rand_score
from sklearn.decomposition import PCA
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster

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
PALETTE = ["#2a78d6", "#eb6834", "#4ea35a", "#a65e3f", "#8858c4", "#c4458e"]

scaled = pd.read_csv(f"{OUT_DIR}/metro_2025_unsupervised_scaled.csv")
feature_cols = [c for c in scaled.columns if c not in ("region_name", "state_name")]
X = scaled[feature_cols].to_numpy()

rng = 42

# ---------------------------------------------------------------- silhouette curve
k_range = list(range(2, 11))
sil_scores = []
for k in k_range:
    labels = KMeans(n_clusters=k, n_init=10, random_state=rng).fit_predict(X)
    sil_scores.append(silhouette_score(X, labels))

best_k = k_range[int(np.argmax(sil_scores))]
print("silhouette scores:", dict(zip(k_range, [round(s, 3) for s in sil_scores])))
print("best k by silhouette:", best_k)

fig, ax = plt.subplots(figsize=(7.2, 4.4), dpi=170)
fig.patch.set_facecolor(SURFACE)
ax.set_facecolor(SURFACE)
ax.plot(k_range, sil_scores, color=BLUE, linewidth=2.2, marker="o", markersize=5, zorder=3)
ax.scatter([best_k], [sil_scores[k_range.index(best_k)]], color=ORANGE, s=90, zorder=4)
ax.annotate(f"best: k={best_k}", (best_k, sil_scores[k_range.index(best_k)]),
            textcoords="offset points", xytext=(10, 8), fontsize=11, color=ORANGE, fontweight="bold")
ax.set_xlabel("k (number of clusters)", fontsize=11, color=INK)
ax.set_ylabel("average silhouette score", fontsize=11, color=INK)
ax.set_title("Silhouette score by k, k-means on the 2025 metro panel", fontsize=13, color=INK, pad=10)
ax.set_xticks(k_range)
ax.grid(axis="y", color=GRID, linewidth=0.8, zorder=0)
for spine in ("top", "right"):
    ax.spines[spine].set_visible(False)
ax.spines["bottom"].set_color(GRID)
ax.spines["left"].set_color(GRID)
fig.tight_layout()
fig.savefig(f"{IMG_DIR}/cluster-silhouette-curve.png", facecolor=SURFACE)
plt.close(fig)

# ---------------------------------------------------------------- per-sample silhouette plot at best k
km_best = KMeans(n_clusters=best_k, n_init=10, random_state=rng).fit(X)
labels_best = km_best.labels_
sample_sil = silhouette_samples(X, labels_best)
avg_sil = silhouette_score(X, labels_best)

fig, ax = plt.subplots(figsize=(7.4, 5.2), dpi=170)
fig.patch.set_facecolor(SURFACE)
ax.set_facecolor(SURFACE)
y_lower = 10
for i in range(best_k):
    vals = np.sort(sample_sil[labels_best == i])
    y_upper = y_lower + len(vals)
    ax.fill_betweenx(np.arange(y_lower, y_upper), 0, vals, color=PALETTE[i % len(PALETTE)], alpha=0.85)
    ax.text(-0.05, y_lower + 0.5 * len(vals), str(i), fontsize=10, color=MUTED, ha="right", va="center")
    y_lower = y_upper + 12
ax.axvline(avg_sil, color=INK, linestyle="--", linewidth=1.3)
ax.text(avg_sil, y_lower * 1.01, f"avg = {avg_sil:.2f}", fontsize=10, color=INK, ha="center")
ax.set_xlabel("silhouette coefficient", fontsize=11, color=INK)
ax.set_ylabel("metro areas, grouped by cluster", fontsize=11, color=INK)
ax.set_title(f"Silhouette plot, k-means k={best_k}", fontsize=13, color=INK, pad=10)
ax.set_yticks([])
for spine in ("top", "right", "left"):
    ax.spines[spine].set_visible(False)
ax.spines["bottom"].set_color(GRID)
fig.tight_layout()
fig.savefig(f"{IMG_DIR}/cluster-silhouette-plot.png", facecolor=SURFACE)
plt.close(fig)

# ---------------------------------------------------------------- k-means at 3 different k, visualized via PCA(2)
pca2 = PCA(n_components=2, random_state=rng)
coords = pca2.fit_transform(X)
k_compare = sorted(set([3, best_k, 6]))
if len(k_compare) < 3:
    k_compare = [3, 4, 5]

fig, axes = plt.subplots(1, len(k_compare), figsize=(5.0 * len(k_compare), 4.6), dpi=170)
fig.patch.set_facecolor(SURFACE)
for ax, k in zip(axes, k_compare):
    labels_k = KMeans(n_clusters=k, n_init=10, random_state=rng).fit_predict(X)
    ax.set_facecolor(SURFACE)
    for c in range(k):
        m = labels_k == c
        ax.scatter(coords[m, 0], coords[m, 1], s=14, color=PALETTE[c % len(PALETTE)], alpha=0.75, linewidths=0)
    ax.set_title(f"k = {k}" + ("  (silhouette best)" if k == best_k else ""), fontsize=12, color=INK)
    ax.set_xlabel("PC1", fontsize=10, color=MUTED)
    ax.set_ylabel("PC2", fontsize=10, color=MUTED)
    ax.tick_params(labelsize=8, colors=MUTED)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    ax.spines["left"].set_color(GRID)
fig.suptitle("k-means clusters at three values of k (projected onto the first two principal components)",
             fontsize=12.5, color=INK, y=1.02)
fig.tight_layout()
fig.savefig(f"{IMG_DIR}/cluster-kmeans-k-compare.png", facecolor=SURFACE, bbox_inches="tight")
plt.close(fig)

# ---------------------------------------------------------------- hierarchical clustering, cosine distance
Z = linkage(X, method="average", metric="cosine")

fig, ax = plt.subplots(figsize=(11, 5.0), dpi=160)
fig.patch.set_facecolor(SURFACE)
ax.set_facecolor(SURFACE)
dendrogram(Z, no_labels=True, color_threshold=0, ax=ax, link_color_func=lambda k: MUTED)
ax.set_title("Hierarchical clustering dendrogram, average linkage, cosine distance", fontsize=13, color=INK, pad=10)
ax.set_xlabel("metro areas (894 leaves)", fontsize=11, color=INK)
ax.set_ylabel("cosine distance", fontsize=11, color=INK)
ax.tick_params(colors=MUTED)
for spine in ("top", "right"):
    ax.spines[spine].set_visible(False)
ax.spines["bottom"].set_color(GRID)
ax.spines["left"].set_color(GRID)
fig.tight_layout()
fig.savefig(f"{IMG_DIR}/cluster-dendrogram.png", facecolor=SURFACE)
plt.close(fig)

# pick hclust k the same way a reader would from the dendrogram: the cut
# that maximizes the gap between consecutive merge heights among the last
# few merges (i.e. the biggest jump before the final merges)
heights = Z[:, 2]
gaps = np.diff(heights[-15:])
cut_idx = len(heights) - 15 + int(np.argmax(gaps)) + 1
n_merges_below_cut = len(heights) - cut_idx
hclust_suggested_k = n_merges_below_cut + 1
print("hclust-suggested k from largest dendrogram gap:", hclust_suggested_k)

hclust_labels = fcluster(Z, t=hclust_suggested_k, criterion="maxclust")

km_same_k = KMeans(n_clusters=hclust_suggested_k, n_init=10, random_state=rng).fit_predict(X)
ari = adjusted_rand_score(km_same_k, hclust_labels)
print(f"ARI between k-means(k={hclust_suggested_k}) and hclust(k={hclust_suggested_k}): {ari:.3f}")

fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.6), dpi=170)
fig.patch.set_facecolor(SURFACE)
for ax, (labels_, title) in zip(axes, [(km_same_k, f"k-means, k={hclust_suggested_k}"),
                                        (hclust_labels - 1, f"hierarchical (cosine), k={hclust_suggested_k}")]):
    ax.set_facecolor(SURFACE)
    uniq = sorted(set(labels_))
    for i, c in enumerate(uniq):
        m = labels_ == c
        ax.scatter(coords[m, 0], coords[m, 1], s=14, color=PALETTE[i % len(PALETTE)], alpha=0.75, linewidths=0)
    ax.set_title(title, fontsize=12, color=INK)
    ax.set_xlabel("PC1", fontsize=10, color=MUTED)
    ax.set_ylabel("PC2", fontsize=10, color=MUTED)
    ax.tick_params(labelsize=8, colors=MUTED)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    ax.spines["left"].set_color(GRID)
fig.suptitle(f"k-means vs. hierarchical clustering at the same k (Adjusted Rand Index = {ari:.2f})",
             fontsize=12.5, color=INK, y=1.03)
fig.tight_layout()
fig.savefig(f"{IMG_DIR}/cluster-kmeans-vs-hclust.png", facecolor=SURFACE, bbox_inches="tight")
plt.close(fig)

# cluster profile table (means of raw features per k-means cluster, best_k)
raw = pd.read_csv(f"{OUT_DIR}/metro_2025_unsupervised.csv")
raw["cluster"] = labels_best
profile = raw.groupby("cluster")[feature_cols].mean().round(2)
profile["n_metros"] = raw.groupby("cluster").size()
profile.to_csv(f"{OUT_DIR}/cluster-profile-table.csv")

print()
print("DONE")
print("best_k =", best_k)
print("k_compare =", k_compare)
print("hclust_suggested_k =", hclust_suggested_k)
print("ari =", round(ari, 3))
