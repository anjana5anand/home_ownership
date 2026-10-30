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
from sklearn.tree import DecisionTreeClassifier, plot_tree
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

    fig, ax = plt.subplots(figsize=(5.2, 4.6), dpi=170)
    fig.patch.set_facecolor(SURFACE)
    ax.set_facecolor(SURFACE)
    im = ax.imshow(cm, cmap="Oranges")
    ax.set_xticks(range(len(CLASSES))); ax.set_yticks(range(len(CLASSES)))
    ax.set_xticklabels(CLASSES, fontsize=9, color=INK)
    ax.set_yticklabels(CLASSES, fontsize=9, color=INK)
    ax.set_xlabel("predicted class", fontsize=10, color=INK)
    ax.set_ylabel("true class", fontsize=10, color=INK)
    for i in range(len(CLASSES)):
        for j in range(len(CLASSES)):
            val = cm[i, j]
            color = "white" if val > cm.max() / 2 else INK
            ax.text(j, i, str(val), ha="center", va="center", color=color, fontsize=12, fontweight="bold")
    short = name.split(" (")[0].replace(" ", "-").lower()
    ax.set_title(f"{name}\naccuracy = {acc:.1%}", fontsize=11.5, color=INK, pad=10)
    for spine in ax.spines.values():
        spine.set_visible(False)
    fig.tight_layout()
    fig.savefig(f"{IMG_DIR}/dt-confusion-{short}.png", facecolor=SURFACE)
    plt.close(fig)

results = pd.DataFrame(rows, columns=["tree", "test_accuracy", "depth", "n_leaves"])
results.to_csv(f"{OUT_DIR}/dt-results-table.csv", index=False)

# ---------------------------------------------------------------- tree diagrams (A and B, depth-3, fully readable)
# Readability pass: friendly feature names instead of raw column names, and
# impurity=False to drop the gini/entropy number from every box. That number
# is already worked through once, by hand, in the table above (the actual
# root split's gini and entropy, before and after); repeating it in all 15
# boxes of every tree added clutter without adding information for a reader
# who isn't going to re-derive the splits themselves.
display_title = {
    "Tree A (gini, depth=3)": "Tree A — split using gini impurity, max depth 3",
    "Tree B (entropy, depth=3)": "Tree B — split using entropy, max depth 3",
}
for name, fname in [("Tree A (gini, depth=3)", "dt-tree-gini.png"), ("Tree B (entropy, depth=3)", "dt-tree-entropy.png")]:
    clf = trees[name]
    fig, ax = plt.subplots(figsize=(16, 7.5), dpi=160)
    fig.patch.set_facecolor(SURFACE)
    plot_tree(clf, feature_names=FRIENDLY_LABELS, class_names=CLASSES, filled=True, rounded=True,
               impurity=False, fontsize=11, ax=ax, proportion=False)
    ax.set_title(display_title[name], fontsize=15, color=INK, pad=14)
    fig.tight_layout()
    fig.savefig(f"{IMG_DIR}/{fname}", facecolor=SURFACE)
    plt.close(fig)

# unpruned tree is too large to render legibly in full; show just the top 2 levels for comparison
clf_c = trees["Tree C (gini, unpruned)"]
fig, ax = plt.subplots(figsize=(13, 6), dpi=160)
fig.patch.set_facecolor(SURFACE)
plot_tree(clf_c, feature_names=FRIENDLY_LABELS, class_names=CLASSES, filled=True, rounded=True,
           impurity=False, fontsize=11, ax=ax, max_depth=2)
ax.set_title(f"Tree C — unpruned, top 2 levels shown of {clf_c.get_depth()} actual levels and {clf_c.get_n_leaves()} leaves",
             fontsize=14, color=INK, pad=14)
fig.tight_layout()
fig.savefig(f"{IMG_DIR}/dt-tree-unpruned-top.png", facecolor=SURFACE)
plt.close(fig)

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
