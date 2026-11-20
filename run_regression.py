"""
Linear regression (continuous payment-to-income target) and logistic
regression (binary Burdened/Not-Burdened target), on the same four
price-growth/volatility predictors used throughout this project, plus
a refit of Part 3's Bernoulli NB collapsed to the same binary target
so logistic regression can be compared against it fairly.

Run: python3 run_regression.py   (after prep_regression_data.py)
Writes figures to docs/images/, results tables to data_clean/.
"""
import json
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.naive_bayes import BernoulliNB
from sklearn.metrics import (
    mean_squared_error, mean_absolute_error, r2_score,
    confusion_matrix, accuracy_score,
)

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
FRIENDLY = {
    "zhvi_yoy_pct": "1yr price chg %", "zhvi_3yr_pct": "3yr price chg %",
    "zhvi_5yr_pct": "5yr price chg %", "zhvi_volatility_5yr": "5yr price volatility",
}

train = pd.read_csv(f"{OUT_DIR}/metro_2025_regression_train.csv")
test = pd.read_csv(f"{OUT_DIR}/metro_2025_regression_test.csv")

X_train, X_test = train[PREDICTORS], test[PREDICTORS]

# =================================================================== linear regression
y_train_lin = train["payment_to_income_pct_25_34"]
y_test_lin = test["payment_to_income_pct_25_34"]

lin = LinearRegression().fit(X_train, y_train_lin)
lin_pred = lin.predict(X_test)

rmse = float(np.sqrt(mean_squared_error(y_test_lin, lin_pred)))
mae = float(mean_absolute_error(y_test_lin, lin_pred))
r2 = float(r2_score(y_test_lin, lin_pred))

print("--- linear regression ---")
print(f"RMSE={rmse:.3f}  MAE={mae:.3f}  R2={r2:.3f}")
print("intercept:", round(lin.intercept_, 4))
for feat, coef in zip(PREDICTORS, lin.coef_):
    print(f"  {feat}: {coef:.4f}")

lin_results = {
    "rmse": round(rmse, 3), "mae": round(mae, 3), "r2": round(r2, 3),
    "intercept": round(float(lin.intercept_), 4),
    "coefficients": {f: round(float(c), 4) for f, c in zip(PREDICTORS, lin.coef_)},
}
with open(f"{OUT_DIR}/regression-linear-results.json", "w") as f:
    json.dump(lin_results, f, indent=2)

# predicted vs actual figure
fig, ax = plt.subplots(figsize=(6, 5.6), dpi=170)
fig.patch.set_facecolor(SURFACE)
ax.set_facecolor(SURFACE)
ax.scatter(y_test_lin, lin_pred, s=18, color=BLUE, alpha=0.55, edgecolor="none", zorder=3)
lims = [min(y_test_lin.min(), lin_pred.min()) - 2, max(y_test_lin.max(), lin_pred.max()) + 2]
ax.plot(lims, lims, color=ORANGE, linestyle="--", linewidth=1.6, zorder=2, label="perfect prediction (y = x)")
ax.set_xlim(lims); ax.set_ylim(lims)
ax.set_xlabel("actual payment-to-income %", fontsize=10.5, color=INK)
ax.set_ylabel("predicted payment-to-income %", fontsize=10.5, color=INK)
ax.set_title(f"Linear regression: predicted vs. actual\ntest set (n=224), R² = {r2:.2f}", fontsize=12, color=INK, pad=10)
ax.legend(fontsize=9, frameon=False, loc="upper left")
ax.grid(color=GRID, linewidth=0.8, zorder=0)
for spine in ("top", "right"):
    ax.spines[spine].set_visible(False)
ax.spines["bottom"].set_color(GRID); ax.spines["left"].set_color(GRID)
fig.tight_layout()
fig.savefig(f"{IMG_DIR}/regression-pred-vs-actual.png", facecolor=SURFACE)
plt.close(fig)

# coefficient bar chart
fig, ax = plt.subplots(figsize=(7, 4.2), dpi=170)
fig.patch.set_facecolor(SURFACE)
ax.set_facecolor(SURFACE)
labels = [FRIENDLY[f] for f in PREDICTORS]
colors = [BLUE if c >= 0 else ORANGE for c in lin.coef_]
ax.barh(labels, lin.coef_, color=colors, height=0.55, zorder=3)
ax.axvline(0, color=INK, linewidth=1, zorder=2)
span = max(lin.coef_.max(), 0) - min(lin.coef_.min(), 0)
pad = span * 0.05
ax.set_xlim(min(lin.coef_.min(), 0) - span * 0.22, max(lin.coef_.max(), 0) + span * 0.14)
for y, c in enumerate(lin.coef_):
    ax.text(c + (pad if c >= 0 else -pad), y, f"{c:+.3f}", va="center",
            ha="left" if c >= 0 else "right", fontsize=10, color=INK, fontweight="bold")
ax.set_xlabel("coefficient (change in predicted payment-to-income % per 1-unit increase)", fontsize=9.5, color=INK)
ax.set_title("Linear regression coefficients", fontsize=12.5, color=INK, pad=10)
ax.grid(axis="x", color=GRID, linewidth=0.8, zorder=0)
for spine in ("top", "right"):
    ax.spines[spine].set_visible(False)
ax.spines["bottom"].set_color(GRID); ax.spines["left"].set_color(GRID)
fig.tight_layout()
fig.savefig(f"{IMG_DIR}/regression-coefficients.png", facecolor=SURFACE)
plt.close(fig)

# =================================================================== logistic regression
y_train_log = train["is_burdened"]
y_test_log = test["is_burdened"]
LOG_CLASSES = ["Not Burdened", "Burdened"]

log = LogisticRegression().fit(X_train, y_train_log)
log_pred = log.predict(X_test)
log_acc = accuracy_score(y_test_log, log_pred)
log_cm = confusion_matrix(y_test_log, log_pred, labels=[0, 1])

print("\n--- logistic regression ---")
print(f"accuracy={log_acc:.3f}")
print("confusion matrix (rows=true, cols=pred, order=Not Burdened/Burdened):\n", log_cm)
print("intercept:", round(log.intercept_[0], 4))
for feat, coef in zip(PREDICTORS, log.coef_[0]):
    print(f"  {feat}: coef={coef:.4f}  odds ratio={np.exp(coef):.4f}")

# =================================================================== Bernoulli NB, refit and collapsed to binary, for comparison
medians = X_train.median()
X_train_bin = (X_train >= medians).astype(int)
X_test_bin = (X_test >= medians).astype(int)
bnb = BernoulliNB().fit(X_train_bin, train["affordability_class"])
bnb_pred_3class = bnb.predict(X_test_bin)
bnb_pred_binary = (bnb_pred_3class == "Burdened").astype(int)
bnb_binary_acc = accuracy_score(y_test_log, bnb_pred_binary)

print("\n--- Bernoulli NB (Part 3), collapsed to binary Burdened/Not-Burdened ---")
print(f"binary-equivalent accuracy={bnb_binary_acc:.3f}  (vs. logistic regression={log_acc:.3f})")

log_results = {
    "accuracy": round(float(log_acc), 4),
    "intercept": round(float(log.intercept_[0]), 4),
    "coefficients": {f: round(float(c), 4) for f, c in zip(PREDICTORS, log.coef_[0])},
    "odds_ratios": {f: round(float(np.exp(c)), 4) for f, c in zip(PREDICTORS, log.coef_[0])},
    "confusion_matrix": log_cm.tolist(),
    "nb_bernoulli_binary_accuracy": round(float(bnb_binary_acc), 4),
}
with open(f"{OUT_DIR}/regression-logistic-results.json", "w") as f:
    json.dump(log_results, f, indent=2)

# confusion matrix figure: outlined diagonal + recall-by-class bar chart (house style)
cm_pct = log_cm / log_cm.sum(axis=1, keepdims=True) * 100
recall = np.diag(cm_pct)

fig, (ax, ax2) = plt.subplots(1, 2, figsize=(9.2, 4.6), dpi=170, gridspec_kw={"width_ratios": [1.15, 1]})
fig.patch.set_facecolor(SURFACE)
ax.set_facecolor(SURFACE)
im = ax.imshow(cm_pct, cmap="Oranges", vmin=0, vmax=100)
ax.set_xticks(range(2)); ax.set_yticks(range(2))
ax.set_xticklabels(LOG_CLASSES, fontsize=9.5, color=INK)
ax.set_yticklabels(LOG_CLASSES, fontsize=9.5, color=INK)
ax.set_xlabel("predicted", fontsize=10, color=INK)
ax.set_ylabel("true", fontsize=10, color=INK)
for i in range(2):
    for j in range(2):
        pct = cm_pct[i, j]
        color = "white" if pct > 50 else INK
        ax.text(j, i, f"{log_cm[i, j]}\n{pct:.0f}%", ha="center", va="center", color=color,
                fontsize=12, fontweight="bold", linespacing=1.6)
        if i == j:
            ax.add_patch(plt.Rectangle((j - 0.5, i - 0.5), 1, 1, fill=False, edgecolor=INK, linewidth=2.6, zorder=5))
ax.set_title(f"Logistic regression\naccuracy = {log_acc:.1%}", fontsize=12, color=INK, pad=10)
for spine in ax.spines.values():
    spine.set_visible(False)
cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
cbar.set_label("% of that row's true class", fontsize=8.5, color=MUTED)
cbar.ax.tick_params(labelsize=8, colors=MUTED)

ax2.set_facecolor(SURFACE)
y_pos = np.arange(2)
ax2.barh(y_pos, recall, color=ORANGE, height=0.5, zorder=3)
ax2.set_yticks(y_pos); ax2.set_yticklabels(LOG_CLASSES, fontsize=9.5, color=INK)
ax2.invert_yaxis()
ax2.set_xlim(0, 100)
ax2.set_xlabel("% of this true class correctly predicted", fontsize=9, color=INK)
ax2.set_title("Recall by class", fontsize=11.5, color=INK, pad=10)
for y, val in zip(y_pos, recall):
    ax2.text(val + 2, y, f"{val:.0f}%", va="center", fontsize=10, color=INK, fontweight="bold")
ax2.axvline(50, color=MUTED, linestyle="--", linewidth=1, zorder=2)
for spine in ("top", "right"):
    ax2.spines[spine].set_visible(False)
ax2.spines["bottom"].set_color(GRID); ax2.spines["left"].set_color(GRID)
ax2.grid(axis="x", color=GRID, linewidth=0.8, zorder=0)
fig.tight_layout()
fig.savefig(f"{IMG_DIR}/regression-logistic-confusion.png", facecolor=SURFACE)
plt.close(fig)

print("\nDONE")
