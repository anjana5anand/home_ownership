"""
Naive Bayes on the labeled affordability-class dataset.
=======================================================================
Multinomial NB (required) models features as counts, so it needs
non-negative, count-like input. The 7 predictors here are continuous
and include negative values (e.g. zhvi_yoy_pct can be negative), so
each predictor is discretized into 4 quantile bins (0-3, an ordinal
"count" of which quarter of that feature's distribution a metro falls
into), with bin edges fit on the Training Set only and then applied to
the Test Set, so no information from the test rows leaks into how the
bins are drawn.

Bernoulli NB (described, and run here too) instead wants binary
features, so each predictor is separately thresholded at its own
training-set median into 0/1 ("below" / "at-or-above" the median).

Run: python3 run_naive_bayes.py   (after prep_supervised_data.py)
Writes figures to docs/images/, a results table to data_clean/.
"""
import numpy as np
import pandas as pd
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.preprocessing import KBinsDiscretizer
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
SURFACE = "#fcfcfb"
INK = "#0b0b0b"
MUTED = "#5a544c"
GRID = "#e7e3dc"

PREDICTORS = [
    "zhvi_yoy_pct", "zhvi_3yr_pct", "zhvi_5yr_pct", "zhvi_volatility_5yr",
]
CLASSES = ["Affordable", "Moderate", "Burdened"]

train = pd.read_csv(f"{OUT_DIR}/metro_2025_supervised_train.csv")
test = pd.read_csv(f"{OUT_DIR}/metro_2025_supervised_test.csv")

X_train, y_train = train[PREDICTORS], train["affordability_class"]
X_test, y_test = test[PREDICTORS], test["affordability_class"]

# ---------------------------------------------------------------- Multinomial NB
binner = KBinsDiscretizer(n_bins=4, encode="ordinal", strategy="quantile")
X_train_binned = binner.fit_transform(X_train)
X_test_binned = binner.transform(X_test)

mnb = MultinomialNB()
mnb.fit(X_train_binned, y_train)
mnb_pred = mnb.predict(X_test_binned)
mnb_acc = accuracy_score(y_test, mnb_pred)
mnb_cm = confusion_matrix(y_test, mnb_pred, labels=CLASSES)

print("MultinomialNB accuracy:", round(mnb_acc, 3))
print("MultinomialNB confusion matrix (rows=true, cols=pred):\n", mnb_cm)

# ---------------------------------------------------------------- Bernoulli NB
medians = X_train.median()
X_train_bin = (X_train >= medians).astype(int)
X_test_bin = (X_test >= medians).astype(int)

bnb = BernoulliNB()
bnb.fit(X_train_bin, y_train)
bnb_pred = bnb.predict(X_test_bin)
bnb_acc = accuracy_score(y_test, bnb_pred)
bnb_cm = confusion_matrix(y_test, bnb_pred, labels=CLASSES)

print("BernoulliNB accuracy:", round(bnb_acc, 3))
print("BernoulliNB confusion matrix (rows=true, cols=pred):\n", bnb_cm)

# ---------------------------------------------------------------- confusion matrix figures
def plot_cm(cm, acc, title, fname):
    fig, ax = plt.subplots(figsize=(5.4, 4.8), dpi=170)
    fig.patch.set_facecolor(SURFACE)
    ax.set_facecolor(SURFACE)
    im = ax.imshow(cm, cmap="Oranges")
    ax.set_xticks(range(len(CLASSES)))
    ax.set_yticks(range(len(CLASSES)))
    ax.set_xticklabels(CLASSES, fontsize=10, color=INK)
    ax.set_yticklabels(CLASSES, fontsize=10, color=INK)
    ax.set_xlabel("predicted class", fontsize=11, color=INK)
    ax.set_ylabel("true class", fontsize=11, color=INK)
    for i in range(len(CLASSES)):
        for j in range(len(CLASSES)):
            val = cm[i, j]
            color = "white" if val > cm.max() / 2 else INK
            ax.text(j, i, str(val), ha="center", va="center", color=color, fontsize=13, fontweight="bold")
    ax.set_title(f"{title}\naccuracy = {acc:.1%}", fontsize=12.5, color=INK, pad=12)
    for spine in ax.spines.values():
        spine.set_visible(False)
    fig.tight_layout()
    fig.savefig(f"{IMG_DIR}/{fname}", facecolor=SURFACE)
    plt.close(fig)

plot_cm(mnb_cm, mnb_acc, "Multinomial NB: confusion matrix (test set, n=224)", "nb-confusion-multinomial.png")
plot_cm(bnb_cm, bnb_acc, "Bernoulli NB: confusion matrix (test set, n=224)", "nb-confusion-bernoulli.png")

# ---------------------------------------------------------------- bin-edge illustration figure
fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.2), dpi=170)
fig.patch.set_facecolor(SURFACE)
for ax, feat in zip(axes, ["zhvi_yoy_pct", "zhvi_volatility_5yr"]):
    ax.set_facecolor(SURFACE)
    vals = X_train[feat].values
    edges = np.quantile(vals, [0, 0.25, 0.5, 0.75, 1.0])
    ax.hist(vals, bins=30, color=BLUE, alpha=0.75, zorder=2)
    for e in edges[1:-1]:
        ax.axvline(e, color=ORANGE, linestyle="--", linewidth=1.4, zorder=3)
    ax.set_title(f"{feat}: 4 quantile bins", fontsize=11, color=INK)
    ax.set_xlabel(feat, fontsize=9, color=MUTED)
    ax.tick_params(labelsize=8, colors=MUTED)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    ax.spines["left"].set_color(GRID)
fig.suptitle("Turning continuous predictors into counts: quantile-bin edges (training set)", fontsize=12, color=INK, y=1.03)
fig.tight_layout()
fig.savefig(f"{IMG_DIR}/nb-binning-illustration.png", facecolor=SURFACE, bbox_inches="tight")
plt.close(fig)

# results table
results = pd.DataFrame(
    [["Multinomial NB (quantile-binned)", mnb_acc], ["Bernoulli NB (median-binarized)", bnb_acc]],
    columns=["model", "test_accuracy"],
)
results.to_csv(f"{OUT_DIR}/nb-results-table.csv", index=False)

print("\nDONE")
print("mnb_acc =", round(mnb_acc, 3))
print("bnb_acc =", round(bnb_acc, 3))
