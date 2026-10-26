"""
Module 3 data prep: a labeled, numeric table for Naive Bayes and Decision
Trees.
=======================================================================
Naive Bayes and Decision Trees are supervised methods, so they require
labeled data: every row needs a class to predict, and the data must be
split into a disjoint Training Set (used to fit the model) and Testing
Set (used only to check accuracy on rows the model never saw).

LABEL
  The 894 metros from the 2025 cross-section are split into three
  affordability classes by payment_to_income_pct_25_34 (the share of a
  young worker's income a monthly mortgage payment would consume),
  using tertiles so the three classes are of roughly equal size:
    Affordable  - bottom third of payment burden
    Moderate    - middle third
    Burdened    - top third

PREDICTORS
  Only 4 of the 11 engineered features are used as predictors:
  zhvi_yoy_pct, zhvi_3yr_pct, zhvi_5yr_pct, zhvi_volatility_5yr.
  Every other feature is excluded because, within a single year, each
  metro's national income and national mortgage rate benchmark are the
  same constant, so price_to_income_25_34, monthly_payment_usd,
  years_to_down_payment_25_34, payment_to_income_pct_25_34 (the label
  source), zhvi_vs_national, and even zhvi_pctile_in_year are all just
  monotonic rescalings of zhvi itself. An early version of this script
  included zhvi and zhvi_pctile_in_year as predictors and the resulting
  tree hit 100% test accuracy by splitting once on zhvi_pctile_in_year,
  which is not a model learning anything, it is the label's own
  definition leaking back in through a renamed copy of the same price
  level. Excluding every price-level feature leaves only price-growth
  and volatility measures, a genuinely separate question: do the recent
  trajectory and stability of a metro's prices predict its current
  payment-burden class, without being told the price level itself?

INPUT
  data_clean/metro_2025_unsupervised.csv   written by prep_unsupervised_data.py

OUTPUTS
  data_clean/metro_2025_supervised.csv            labeled, raw predictor values
  data_clean/metro_2025_supervised_train.csv      training split (75%)
  data_clean/metro_2025_supervised_test.csv       testing split (25%)

Run: python3 prep_supervised_data.py
"""
import pandas as pd
from sklearn.model_selection import train_test_split

IN = "data_clean/metro_2025_unsupervised.csv"
OUT_DIR = "data_clean"

PREDICTORS = [
    "zhvi_yoy_pct",
    "zhvi_3yr_pct",
    "zhvi_5yr_pct",
    "zhvi_volatility_5yr",
]
LABEL_SOURCE = "payment_to_income_pct_25_34"

df = pd.read_csv(IN)

labels, bin_edges = pd.qcut(
    df[LABEL_SOURCE], q=3, labels=["Affordable", "Moderate", "Burdened"], retbins=True
)
df["affordability_class"] = labels

keep_cols = ["region_name", "state_name"] + PREDICTORS + [LABEL_SOURCE, "affordability_class"]
out = df[keep_cols].copy()
out.to_csv(f"{OUT_DIR}/metro_2025_supervised.csv", index=False)

train, test = train_test_split(
    out, test_size=0.25, random_state=42, stratify=out["affordability_class"]
)
train.to_csv(f"{OUT_DIR}/metro_2025_supervised_train.csv", index=False)
test.to_csv(f"{OUT_DIR}/metro_2025_supervised_test.csv", index=False)

print("label cut points (payment_to_income_pct_25_34):", bin_edges.round(2))
print("class counts (full):", out["affordability_class"].value_counts().to_dict())
print("train shape:", train.shape, "test shape:", test.shape)
print("train class counts:", train["affordability_class"].value_counts().to_dict())
print("test class counts:", test["affordability_class"].value_counts().to_dict())
