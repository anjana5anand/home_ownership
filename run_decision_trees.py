"""
Decision Trees on the same labeled affordability-class dataset used for
Naive Bayes.
=======================================================================
Unlike Naive Bayes, trees need no binning or scaling: splits compare
one feature to a threshold directly, on whatever scale the feature is
already in. Three trees are built to show how the same data can
produce very different trees:
  Tree A: criterion="gini",    max_depth=3   (shallow, gini)
  Tree B: criterion="entropy", max_depth=3   (shallow, entropy)
  Tree C: criterion="gini",    max_depth=None (unpruned, grown to purity)
Because a tree can keep splitting until every leaf is pure (or splits
run out of data), and there is no single rule for which feature to
split on first when several give a similar improvement, an essentially
unlimited number of different, equally "valid" trees can be grown from
the same data by varying depth, splitting criterion, or which ties get
broken which way.

Run: python3 run_decision_trees.py   (after prep_supervised_data.py)
Writes figures to docs/images/, a results table to data_clean/.
"""
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix, accuracy_score

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os

OUT_DIR = "data_clean"
IMG_DIR = "docs/images"
os.makedirs(IMG_DIR, exist_ok=True)

BLUE = "#2a78d6"
ORANGE = "#eb6834"
GREEN = "#4ea35a"
SURFACE = "#fcfcfb"
INK = "#0b0b0b"
MUTED = "#5a544c"
GRID = "#e7e3dc"

PREDICTORS = [
    "zhvi_yoy_pct", "zhvi_3yr_pct", "zhvi_5yr_pct", "zhvi_volatility_5yr",
]
FRIENDLY_NAMES = {
    "zhvi_yoy_pct": "1yr price chg %",
    "zhvi_3yr_pct": "3yr price chg %",
    "zhvi_5yr_pct": "5yr price chg %",
    "zhvi_volatility_5yr": "5yr price volatility",
}
FRIENDLY_LABELS = [FRIENDLY_NAMES[p] for p in PREDICTORS]
CLASSES = ["Affordable", "Moderate", "Burdened"]

train = pd.read_csv(f"{OUT_DIR}/metro_2025_supervised_train.csv")
test = pd.read_csv(f"{OUT_DIR}/metro_2025_supervised_test.csv")

X_train, y_train = train[PREDICTORS], train["affordability_class"]
X_test, y_test = test[PREDICTORS], test["affordability_class"]

trees = {
    "Tree A (gini, depth=3)": DecisionTreeClassifier(criterion="gini", max_depth=3, random_state=42),
    "Tree B (entropy, depth=3)": DecisionTreeClassifier(criterion="entropy", max_depth=3, random_state=42),
    "Tree C (gini, unpruned)": DecisionTreeClassifier(criterion="gini", max_depth=None, random_state=42),
}

rows = []
for name, clf in trees.items():
    clf.fit(X_train, y_train)
    pred = clf.predict(X_test)
    acc = accuracy_score(y_test, pred)
    cm = confusion_matrix(y_test, pred, labels=CLASSES)
    depth = clf.get_depth()
    leaves = clf.get_n_leaves()
    print(f"{name}: accuracy={acc:.3f}, depth={depth}, leaves={leaves}")
    print(cm)
    rows.append([name, acc, depth, leaves])
    trees[name] = clf  # fitted

    # row-normalize: each row sums to 100%, so color intensity shows what
    # share of a true class landed in each predicted class, not the raw
    # count (which is pulled around by any class-size imbalance in the
    # 224-metro test set).
    cm_pct = cm / cm.sum(axis=1, keepdims=True) * 100
    recall = np.diag(cm_pct)  # the diagonal, pulled out as its own chart

    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(9.8, 4.8), dpi=170, gridspec_kw={"width_ratios": [1.3, 1]})
    fig.patch.set_facecolor(SURFACE)
    ax.set_facecolor(SURFACE)
    im = ax.imshow(cm_pct, cmap="Oranges", vmin=0, vmax=100)
    ax.set_xticks(range(len(CLASSES))); ax.set_yticks(range(len(CLASSES)))
    ax.set_xticklabels(CLASSES, fontsize=9, color=INK)
    ax.set_yticklabels(CLASSES, fontsize=9, color=INK)
    ax.set_xlabel("predicted class", fontsize=10, color=INK)
    ax.set_ylabel("true class", fontsize=10, color=INK)
    for i in range(len(CLASSES)):
        for j in range(len(CLASSES)):
            pct = cm_pct[i, j]
            color = "white" if pct > 50 else INK
            ax.text(j, i, f"{cm[i, j]}\n{pct:.0f}%", ha="center", va="center", color=color,
                    fontsize=11, fontweight="bold", linespacing=1.6)
            if i == j:
                # outline the "correct prediction" cells so the eye lands there first
                ax.add_patch(plt.Rectangle((j - 0.5, i - 0.5), 1, 1, fill=False,
                                            edgecolor=INK, linewidth=2.6, zorder=5))
    short = name.split(" (")[0].replace(" ", "-").lower()
    ax.set_title(f"{name}\naccuracy = {acc:.1%}", fontsize=11.5, color=INK, pad=10)
    for spine in ax.spines.values():
        spine.set_visible(False)
    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label("% of that row's true class", fontsize=8.5, color=MUTED)
    cbar.ax.tick_params(labelsize=8, colors=MUTED)

    # right panel: the outlined diagonal, pulled out as a simple recall-per-class bar chart
    ax2.set_facecolor(SURFACE)
    y_pos = np.arange(len(CLASSES))
    ax2.barh(y_pos, recall, color=ORANGE, height=0.55, zorder=3)
    ax2.set_yticks(y_pos)
    ax2.set_yticklabels(CLASSES, fontsize=9.5, color=INK)
    ax2.invert_yaxis()
    ax2.set_xlim(0, 100)
    ax2.set_xlabel("% of this true class correctly predicted", fontsize=9, color=INK)
    ax2.set_title("Recall by class\n(the diagonal, pulled out)", fontsize=11, color=INK, pad=10)
    for y, val in zip(y_pos, recall):
        ax2.text(val + 2, y, f"{val:.0f}%", va="center", fontsize=10, color=INK, fontweight="bold")
    ax2.axvline(100 / 3, color=MUTED, linestyle="--", linewidth=1, zorder=2)
    for spine in ("top", "right"):
        ax2.spines[spine].set_visible(False)
    ax2.spines["bottom"].set_color(GRID)
    ax2.spines["left"].set_color(GRID)
    ax2.grid(axis="x", color=GRID, linewidth=0.8, zorder=0)

    fig.tight_layout()
    fig.savefig(f"{IMG_DIR}/dt-confusion-{short}.png", facecolor=SURFACE)
    plt.close(fig)

results = pd.DataFrame(rows, columns=["tree", "test_accuracy", "depth", "n_leaves"])
results.to_csv(f"{OUT_DIR}/dt-results-table.csv", index=False)

# ---------------------------------------------------------------- tree diagrams, redrawn by hand for readability
# plot_tree's default boxes (raw column names, a gini number, a full
# value=[...] array, all in default-size text) were too dense to read at a
# glance. Each tree is redrawn here as simple yes/no question boxes with
# True/False branches and solid, color-coded leaf boxes, the same style as a
# textbook decision-tree diagram: what matters for a reader is the question
# asked at each step and the class predicted at the end, not the internal
# gini bookkeeping (which the worked example table above shows once,
# concretely, for the real root split).
CLASS_COLOR = {"Affordable": BLUE, "Moderate": GREEN, "Burdened": ORANGE}

def _leaf_label(tree_, node, classes_):
    counts = tree_.value[node][0]
    cls = classes_[int(np.argmax(counts))]
    n = int(tree_.n_node_samples[node])
    return cls, n

def _layout(tree_, node, depth, leaf_x, positions, max_depth=None):
    """Assigns each node an (x, y) position: x by leaf order, y by -depth."""
    left, right = tree_.children_left[node], tree_.children_right[node]
    is_leaf = (left == -1) or (max_depth is not None and depth == max_depth)
    if is_leaf:
        x = leaf_x[0]
        leaf_x[0] += 1
        positions[node] = (x, -depth, True)
        return x
    xl = _layout(tree_, left, depth + 1, leaf_x, positions, max_depth)
    xr = _layout(tree_, right, depth + 1, leaf_x, positions, max_depth)
    x = (xl + xr) / 2
    positions[node] = (x, -depth, False)
    return x

def draw_custom_tree(clf, feature_names, title, fname, max_depth=None, figsize=(15, 7.5)):
    tree_ = clf.tree_
    classes_ = list(clf.classes_)
    positions = {}
    _layout(tree_, 0, 0, [0], positions, max_depth=max_depth)

    fig, ax = plt.subplots(figsize=figsize, dpi=160)
    fig.patch.set_facecolor(SURFACE)
    ax.set_facecolor(SURFACE)
    ax.axis("off")

    box_w, box_h = 0.9, 0.62
    x_scale = 1.15

    def xy(node):
        x, y, _ = positions[node]
        return x * x_scale, y * 1.5

    # edges first, so boxes draw on top
    for node, (x, y, is_leaf) in positions.items():
        if is_leaf:
            continue
        left, right = tree_.children_left[node], tree_.children_right[node]
        px, py = xy(node)
        for child, branch_true in [(left, False), (right, True)]:
            if child not in positions:
                continue
            cx, cy = xy(child)
            ax.annotate("", xy=(cx, cy + box_h / 2), xytext=(px, py - box_h / 2),
                        arrowprops=dict(arrowstyle="-", color=MUTED, linewidth=1.4), zorder=2)
            mx, my = (px + cx) / 2, (py + cy) / 2 - box_h * 0.1
            label, color = ("True", ORANGE) if branch_true else ("False", "#8a8176")
            ax.text(mx, my, label, fontsize=11, color=color, fontweight="bold",
                    ha="center", va="center", zorder=3,
                    bbox=dict(boxstyle="round,pad=0.15", fc=SURFACE, ec="none"))

    # boxes
    for node, (x, y, is_leaf) in positions.items():
        px, py = xy(node)
        if is_leaf:
            cls, n = _leaf_label(tree_, node, classes_)
            color = CLASS_COLOR.get(cls, MUTED)
            ax.add_patch(plt.Rectangle((px - box_w / 2, py - box_h / 2), box_w, box_h,
                                        facecolor=color, edgecolor="none", zorder=4,
                                        joinstyle="round", capstyle="round"))
            ax.text(px, py + 0.08, cls, ha="center", va="center", fontsize=12.5,
                    color="white", fontweight="bold", zorder=5)
            ax.text(px, py - 0.18, f"{n} metros", ha="center", va="center", fontsize=9,
                    color="white", zorder=5, alpha=0.9)
        else:
            feat = feature_names[tree_.feature[node]]
            thresh = tree_.threshold[node]
            ax.add_patch(plt.Rectangle((px - box_w / 2, py - box_h / 2), box_w, box_h,
                                        facecolor="white", edgecolor=ORANGE, linewidth=1.8,
                                        zorder=4))
            ax.text(px, py, f"{feat}\n> {thresh:.1f} ?", ha="center", va="center", fontsize=11.5,
                    color=INK, fontweight="bold", zorder=5, linespacing=1.4)

    # "..." markers where the tree was truncated
    if max_depth is not None:
        for node, (x, y, is_leaf) in positions.items():
            if is_leaf and tree_.children_left[node] != -1:
                px, py = xy(node)
                for dx in (-0.28, 0.28):
                    ax.add_patch(plt.Rectangle((px + dx - 0.16, py - box_h * 1.55 - 0.1), 0.32, 0.42,
                                                facecolor="#d8d3c8", edgecolor="none", zorder=4))
                    ax.text(px + dx, py - box_h * 1.55 + 0.1, "⋯", ha="center", va="center",
                            fontsize=13, color=MUTED, zorder=5)
                    ax.annotate("", xy=(px + dx, py - box_h * 1.55 + 0.31), xytext=(px, py - box_h / 2),
                                arrowprops=dict(arrowstyle="-", color=MUTED, linewidth=1.2), zorder=2)

    xs = [xy(n)[0] for n in positions]
    ys = [xy(n)[1] for n in positions]
    pad_x, pad_y = box_w, box_h * 1.3
    extra_bottom = 1.0 if max_depth is not None else 0.3
    ax.set_xlim(min(xs) - pad_x, max(xs) + pad_x)
    ax.set_ylim(min(ys) - pad_y - extra_bottom, max(ys) + pad_y)
    ax.set_title(title, fontsize=16, color=INK, pad=16, fontweight="bold")
    fig.tight_layout()
    fig.savefig(f"{IMG_DIR}/{fname}", facecolor=SURFACE)
    plt.close(fig)

draw_custom_tree(trees["Tree A (gini, depth=3)"], FRIENDLY_LABELS,
                  "Tree A — split using gini impurity, max depth 3", "dt-tree-gini.png")
draw_custom_tree(trees["Tree B (entropy, depth=3)"], FRIENDLY_LABELS,
                  "Tree B — split using entropy, max depth 3", "dt-tree-entropy.png")

clf_c = trees["Tree C (gini, unpruned)"]
draw_custom_tree(clf_c, FRIENDLY_LABELS,
                  f"Tree C — unpruned, top 2 levels shown of {clf_c.get_depth()} actual levels and {clf_c.get_n_leaves()} leaves",
                  "dt-tree-unpruned-top.png", max_depth=2, figsize=(11, 6))

# ---------------------------------------------------------------- feature importance (Tree A)
clf_a = trees["Tree A (gini, depth=3)"]
imp = pd.Series(clf_a.feature_importances_, index=FRIENDLY_LABELS).sort_values(ascending=True)
fig, ax = plt.subplots(figsize=(7, 4.4), dpi=170)
fig.patch.set_facecolor(SURFACE)
ax.set_facecolor(SURFACE)
ax.barh(imp.index, imp.values, color=BLUE, zorder=2)
ax.set_xlabel("importance (share of total impurity reduction)", fontsize=10.5, color=INK)
ax.set_title("Which predictors Tree A actually splits on", fontsize=12.5, color=INK, pad=10)
ax.grid(axis="x", color=GRID, linewidth=0.8, zorder=0)
for spine in ("top", "right"):
    ax.spines[spine].set_visible(False)
ax.spines["bottom"].set_color(GRID); ax.spines["left"].set_color(GRID)
fig.tight_layout()
fig.savefig(f"{IMG_DIR}/dt-feature-importance.png", facecolor=SURFACE)
plt.close(fig)

# ---------------------------------------------------------------- worked GINI / entropy / info gain example
# Use the actual root split of Tree A: zhvi_pctile_in_year at its threshold
root_feat_idx = clf_a.tree_.feature[0]
root_thresh = clf_a.tree_.threshold[0]
root_feat = PREDICTORS[root_feat_idx]

def gini(counts):
    n = counts.sum()
    p = counts / n
    return 1 - np.sum(p ** 2)

def entropy(counts):
    n = counts.sum()
    p = counts[counts > 0] / n
    return -np.sum(p * np.log2(p))

y_arr = y_train.values
x_arr = X_train[root_feat].values
left_mask = x_arr <= root_thresh
right_mask = ~left_mask

def class_counts(mask):
    sub = y_arr[mask]
    return np.array([np.sum(sub == c) for c in CLASSES])

parent_counts = class_counts(np.ones_like(left_mask, dtype=bool))
left_counts = class_counts(left_mask)
right_counts = class_counts(right_mask)

n_total = parent_counts.sum()
n_left, n_right = left_counts.sum(), right_counts.sum()

parent_gini, left_gini, right_gini = gini(parent_counts), gini(left_counts), gini(right_counts)
parent_ent, left_ent, right_ent = entropy(parent_counts), entropy(left_counts), entropy(right_counts)

weighted_gini_after = (n_left / n_total) * left_gini + (n_right / n_total) * right_gini
weighted_ent_after = (n_left / n_total) * left_ent + (n_right / n_total) * right_ent

gini_gain = parent_gini - weighted_gini_after
info_gain = parent_ent - weighted_ent_after

print("\n--- worked split example ---")
print(f"root split: {root_feat} <= {root_thresh:.3f}")
print("parent class counts:", dict(zip(CLASSES, parent_counts)))
print("left (<= thresh) counts:", dict(zip(CLASSES, left_counts)), "n=", n_left)
print("right (> thresh) counts:", dict(zip(CLASSES, right_counts)), "n=", n_right)
print(f"parent gini={parent_gini:.3f}, entropy={parent_ent:.3f}")
print(f"left  gini={left_gini:.3f}, entropy={left_ent:.3f}")
print(f"right gini={right_gini:.3f}, entropy={right_ent:.3f}")
print(f"weighted gini after split={weighted_gini_after:.3f}  -> gini gain={gini_gain:.3f}")
print(f"weighted entropy after split={weighted_ent_after:.3f} -> information gain={info_gain:.3f}")

worked_example = {
    "root_feature": root_feat, "root_threshold": round(float(root_thresh), 3),
    "parent_counts": dict(zip(CLASSES, parent_counts.tolist())),
    "left_counts": dict(zip(CLASSES, left_counts.tolist())),
    "right_counts": dict(zip(CLASSES, right_counts.tolist())),
    "parent_gini": round(parent_gini, 4), "left_gini": round(left_gini, 4), "right_gini": round(right_gini, 4),
    "parent_entropy": round(parent_ent, 4), "left_entropy": round(left_ent, 4), "right_entropy": round(right_ent, 4),
    "gini_gain": round(gini_gain, 4), "information_gain": round(info_gain, 4),
}
import json
with open(f"{OUT_DIR}/dt-worked-split-example.json", "w") as f:
    json.dump(worked_example, f, indent=2)

print("\nDONE")
