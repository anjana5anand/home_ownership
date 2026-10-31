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
    ax.set_xticks(range(len(CLASSES)))
    ax.set_yticks(range(len(CLASSES)))
    ax.set_xticklabels(CLASSES, fontsize=10, color=INK)
    ax.set_yticklabels(CLASSES, fontsize=10, color=INK)
    ax.set_xlabel("predicted class", fontsize=11, color=INK)
    ax.set_ylabel("true class", fontsize=11, color=INK)
    for i in range(len(CLASSES)):
        for j in range(len(CLASSES)):
            pct = cm_pct[i, j]
            color = "white" if pct > 50 else INK
            ax.text(j, i, f"{cm[i, j]}\n{pct:.0f}%", ha="center", va="center", color=color,
                    fontsize=12, fontweight="bold", linespacing=1.6)
            if i == j:
                # outline the "correct prediction" cells so the eye lands there first
                ax.add_patch(plt.Rectangle((j - 0.5, i - 0.5), 1, 1, fill=False,
                                            edgecolor=INK, linewidth=2.6, zorder=5))
    ax.set_title(f"{title}\naccuracy = {acc:.1%}", fontsize=12, color=INK, pad=12)
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

# ---------------------------------------------------------------- worked example: Bayes' theorem by hand
# Pick one test-set metro and reconstruct BernoulliNB's own posterior from its
# fitted class_log_prior_ and feature_log_prob_, without calling predict_proba,
# to show Bayes' theorem actually being multiplied out.
import json

row_idx = 0
x_row = X_test_bin.iloc[row_idx].values
metro_name = test.iloc[row_idx]["region_name"]
true_label = y_test.iloc[row_idx]

classes_ = list(bnb.classes_)
log_prior = bnb.class_log_prior_
feat_log_prob = bnb.feature_log_prob_

log_joint = log_prior.copy()
per_feature = {}
for j, feat in enumerate(PREDICTORS):
    p1 = np.exp(feat_log_prob[:, j])
    bit = int(x_row[j])
    log_joint = log_joint + (np.log(p1) if bit == 1 else np.log(1 - p1))
    per_feature[feat] = {
        "bit": bit,
        **{c: round(float(p1[ci] if bit == 1 else 1 - p1[ci]), 4) for ci, c in enumerate(classes_)},
    }

posterior = np.exp(log_joint - log_joint.max())
posterior = posterior / posterior.sum()
sk_proba = bnb.predict_proba(X_test_bin.iloc[[row_idx]])[0]
assert np.allclose(posterior, sk_proba, atol=1e-8), "hand calc must match predict_proba exactly"

worked_example = {
    "metro": metro_name,
    "true_class": true_label,
    "predicted_class": classes_[int(np.argmax(posterior))],
    "classes_order": classes_,
    "class_prior": dict(zip(classes_, np.exp(log_prior).round(4).tolist())),
    "per_feature": per_feature,
    "posterior": dict(zip(classes_, posterior.round(4).tolist())),
}
with open(f"{OUT_DIR}/nb-worked-example.json", "w") as f:
    json.dump(worked_example, f, indent=2)

print("\n--- worked Bayes example ---")
print(f"metro: {metro_name} (true class: {true_label})")
print("posterior:", worked_example["posterior"])
print("predicted class:", worked_example["predicted_class"])
print("matches predict_proba:", np.allclose(posterior, sk_proba, atol=1e-8))

print("\nDONE")
print("mnb_acc =", round(mnb_acc, 3))
print("bnb_acc =", round(bnb_acc, 3))
