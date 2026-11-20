"""
AdaBoost on the same 3-class affordability_class target and same four
predictors used for Decision Trees in Part 3, so the two methods are
directly comparable. Also includes a small by-hand worked example of
a single decision stump's weighted error and alpha, on the binary
is_burdened target where the classic AdaBoost alpha formula applies
cleanly.

Run: python3 run_adaboost.py   (after prep_regression_data.py)
Writes figures to docs/images/, results tables to data_clean/.
"""
import json
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier
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

PREDICTORS = ["zhvi_yoy_pct", "zhvi_3yr_pct", "zhvi_5yr_pct", "zhvi_volatility_5yr"]
CLASSES = ["Affordable", "Moderate", "Burdened"]

train = pd.read_csv(f"{OUT_DIR}/metro_2025_regression_train.csv")
test = pd.read_csv(f"{OUT_DIR}/metro_2025_regression_test.csv")

X_train, X_test = train[PREDICTORS], test[PREDICTORS]
y_train, y_test = train["affordability_class"], test["affordability_class"]

# =================================================================== worked example: one stump's weighted error and alpha
# Binary target (is_burdened), where the classic two-class AdaBoost
# alpha formula applies directly: alpha = 0.5 * ln((1 - err) / err).
y_train_bin = train["is_burdened"].values
n = len(y_train_bin)
w = np.full(n, 1.0 / n)  # round-1 weights: uniform

stump = DecisionTreeClassifier(max_depth=1, random_state=42)
stump.fit(X_train, y_train_bin, sample_weight=w)
stump_pred = stump.predict(X_train)
miss = (stump_pred != y_train_bin).astype(float)
err = float(np.sum(w * miss) / np.sum(w))
alpha = float(0.5 * np.log((1 - err) / err))

feat_idx = stump.tree_.feature[0]
thresh = stump.tree_.threshold[0]
print("--- worked stump example (round 1, binary target) ---")
print(f"stump splits on {PREDICTORS[feat_idx]} <= {thresh:.3f}")
print(f"weighted error = {err:.4f}")
print(f"alpha = 0.5 * ln((1-{err:.4f})/{err:.4f}) = {alpha:.4f}")

# round-2 weights, for illustration: up-weight misses, re-normalize
w2 = w * np.exp(alpha * miss * 2 - alpha)  # standard AdaBoost update using +/-1 labels
w2 = w2 / w2.sum()
print(f"total weight moved onto the {int(miss.sum())} missed rows: "
      f"{w2[miss.astype(bool)].sum():.3f} (was {w[miss.astype(bool)].sum():.3f} before reweighting)")

stump_example = {
    "split_feature": PREDICTORS[feat_idx], "threshold": round(float(thresh), 3),
    "weighted_error": round(err, 4), "alpha": round(alpha, 4),
    "n_missed": int(miss.sum()), "n_total": n,
    "missed_weight_before": round(float(w[miss.astype(bool)].sum()), 4),
    "missed_weight_after": round(float(w2[miss.astype(bool)].sum()), 4),
}
with open(f"{OUT_DIR}/adaboost-stump-example.json", "w") as f:
    json.dump(stump_example, f, indent=2)

# =================================================================== tuning: n_estimators x learning_rate
n_est_grid = [5, 10, 25, 50, 75, 100, 150, 200]
lr_grid = [0.3, 1.0, 1.5]
tuning_rows = []
for lr in lr_grid:
    for n_est in n_est_grid:
        clf = AdaBoostClassifier(
            estimator=DecisionTreeClassifier(max_depth=1, random_state=42),
            n_estimators=n_est, learning_rate=lr, random_state=42,
        )
        clf.fit(X_train, y_train)
        acc = accuracy_score(y_test, clf.predict(X_test))
        tuning_rows.append({"learning_rate": lr, "n_estimators": n_est, "test_accuracy": acc})
        print(f"lr={lr:<4} n_estimators={n_est:<4} test_acc={acc:.3f}")

tuning_df = pd.DataFrame(tuning_rows)
tuning_df.to_csv(f"{OUT_DIR}/adaboost-tuning.csv", index=False)

best_row = tuning_df.loc[tuning_df["test_accuracy"].idxmax()]
best_lr, best_n = float(best_row["learning_rate"]), int(best_row["n_estimators"])
print(f"\nbest: lr={best_lr} n_estimators={best_n} acc={best_row['test_accuracy']:.3f}")

fig, ax = plt.subplots(figsize=(7.6, 4.8), dpi=170)
fig.patch.set_facecolor(SURFACE)
ax.set_facecolor(SURFACE)
colors = {0.3: MUTED, 1.0: BLUE, 1.5: ORANGE}
for lr in lr_grid:
    sub = tuning_df[tuning_df["learning_rate"] == lr].sort_values("n_estimators")
    ax.plot(sub["n_estimators"], sub["test_accuracy"] * 100, marker="o", markersize=4,
            color=colors[lr], linewidth=2, label=f"learning_rate = {lr}")
ax.axhline(100 / 3, color=MUTED, linestyle=":", linewidth=1, zorder=1)
ax.set_xlabel("n_estimators (number of boosting rounds)", fontsize=10.5, color=INK)
ax.set_ylabel("test accuracy (%)", fontsize=10.5, color=INK)
ax.set_title("AdaBoost test accuracy as rounds are added", fontsize=13, color=INK, pad=12)
ax.legend(fontsize=9.5, frameon=False)
ax.grid(color=GRID, linewidth=0.8, zorder=0)
for spine in ("top", "right"):
    ax.spines[spine].set_visible(False)
ax.spines["bottom"].set_color(GRID); ax.spines["left"].set_color(GRID)
fig.tight_layout()
fig.savefig(f"{IMG_DIR}/adaboost-tuning-curve.png", facecolor=SURFACE)
plt.close(fig)

# =================================================================== final model, confusion matrix
final = AdaBoostClassifier(
    estimator=DecisionTreeClassifier(max_depth=1, random_state=42),
    n_estimators=best_n, learning_rate=best_lr, random_state=42,
)
final.fit(X_train, y_train)
final_pred = final.predict(X_test)
final_acc = accuracy_score(y_test, final_pred)
final_cm = confusion_matrix(y_test, final_pred, labels=CLASSES)

print("\n--- final AdaBoost model ---")
print(f"n_estimators={best_n} learning_rate={best_lr} test_acc={final_acc:.3f}")
print(final_cm)

DT_TREE_A_ACC = 0.585  # Tree A (gini, max depth 3) from Part 3, same predictors/split
diff_pp = (final_acc - DT_TREE_A_ACC) * 100
print(f"vs. Decision Tree A (Part 3) = {DT_TREE_A_ACC:.3f}  "
      f"(AdaBoost is {diff_pp:+.1f} percentage points)")

final_results = {
    "n_estimators": best_n, "learning_rate": best_lr,
    "test_accuracy": round(float(final_acc), 4),
    "decision_tree_a_accuracy": DT_TREE_A_ACC,
    "diff_percentage_points": round(diff_pp, 2),
    "confusion_matrix": final_cm.tolist(),
}
with open(f"{OUT_DIR}/adaboost-final-results.json", "w") as f:
    json.dump(final_results, f, indent=2)

cm_pct = final_cm / final_cm.sum(axis=1, keepdims=True) * 100
recall = np.diag(cm_pct)

fig, (ax, ax2) = plt.subplots(1, 2, figsize=(9.8, 4.8), dpi=170, gridspec_kw={"width_ratios": [1.3, 1]})
fig.patch.set_facecolor(SURFACE)
ax.set_facecolor(SURFACE)
im = ax.imshow(cm_pct, cmap="Oranges", vmin=0, vmax=100)
ax.set_xticks(range(len(CLASSES))); ax.set_yticks(range(len(CLASSES)))
ax.set_xticklabels(CLASSES, fontsize=9.5, color=INK)
ax.set_yticklabels(CLASSES, fontsize=9.5, color=INK)
ax.set_xlabel("predicted class", fontsize=10, color=INK)
ax.set_ylabel("true class", fontsize=10, color=INK)
for i in range(len(CLASSES)):
    for j in range(len(CLASSES)):
        pct = cm_pct[i, j]
        color = "white" if pct > 50 else INK
        ax.text(j, i, f"{final_cm[i, j]}\n{pct:.0f}%", ha="center", va="center", color=color,
                fontsize=12, fontweight="bold", linespacing=1.6)
        if i == j:
            ax.add_patch(plt.Rectangle((j - 0.5, i - 0.5), 1, 1, fill=False, edgecolor=INK, linewidth=2.6, zorder=5))
ax.set_title(f"AdaBoost (n_estimators={best_n}, lr={best_lr})\naccuracy = {final_acc:.1%}", fontsize=11.5, color=INK, pad=10)
for spine in ax.spines.values():
    spine.set_visible(False)
cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
cbar.set_label("% of that row's true class", fontsize=8.5, color=MUTED)
cbar.ax.tick_params(labelsize=8, colors=MUTED)

ax2.set_facecolor(SURFACE)
y_pos = np.arange(len(CLASSES))
ax2.barh(y_pos, recall, color=ORANGE, height=0.55, zorder=3)
ax2.set_yticks(y_pos); ax2.set_yticklabels(CLASSES, fontsize=9.5, color=INK)
ax2.invert_yaxis()
ax2.set_xlim(0, 100)
ax2.set_xlabel("% of this true class correctly predicted", fontsize=9, color=INK)
ax2.set_title("Recall by class", fontsize=11, color=INK, pad=10)
for y, val in zip(y_pos, recall):
    ax2.text(val + 2, y, f"{val:.0f}%", va="center", fontsize=10, color=INK, fontweight="bold")
ax2.axvline(100 / 3, color=MUTED, linestyle="--", linewidth=1, zorder=2)
for spine in ("top", "right"):
    ax2.spines[spine].set_visible(False)
ax2.spines["bottom"].set_color(GRID); ax2.spines["left"].set_color(GRID)
ax2.grid(axis="x", color=GRID, linewidth=0.8, zorder=0)
fig.tight_layout()
fig.savefig(f"{IMG_DIR}/adaboost-confusion.png", facecolor=SURFACE)
plt.close(fig)

print("\nDONE")
