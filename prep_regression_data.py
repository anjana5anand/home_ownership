"""
Builds the regression/AdaBoost dataset for Module 4, reusing the exact
same 894-metro table and the exact same 75/25 stratified train/test
split already built in prep_supervised_data.py for Part 3, so all
three supervised methods (Naive Bayes, Decision Trees, Regression,
AdaBoost) are compared on identical rows.

Two new target columns are added on top of the existing
affordability_class label:
  payment_to_income_pct_25_34  -- already present, used directly as
                                   the continuous target for linear
                                   regression (predict the actual
                                   payment-to-income ratio, not just
                                   which tertile it falls in).
  is_burdened                  -- a new binary 0/1 column, 1 when
                                   affordability_class == "Burdened",
                                   used as the two-class target for
                                   logistic regression.

Predictors are unchanged from Part 3: zhvi_yoy_pct, zhvi_3yr_pct,
zhvi_5yr_pct, zhvi_volatility_5yr. All four are already numeric
(continuous), so no categorical encoding is needed for this project's
own predictors; see the Data Prep write-up for why that would be
needed if a column like state were included instead.

Run: python3 prep_regression_data.py   (after prep_supervised_data.py)
Writes data_clean/metro_2025_regression.csv, _train.csv, _test.csv.
"""
import pandas as pd

OUT_DIR = "data_clean"

full = pd.read_csv(f"{OUT_DIR}/metro_2025_supervised.csv")
train = pd.read_csv(f"{OUT_DIR}/metro_2025_supervised_train.csv")
test = pd.read_csv(f"{OUT_DIR}/metro_2025_supervised_test.csv")

for df in (full, train, test):
    df["is_burdened"] = (df["affordability_class"] == "Burdened").astype(int)

full.to_csv(f"{OUT_DIR}/metro_2025_regression.csv", index=False)
train.to_csv(f"{OUT_DIR}/metro_2025_regression_train.csv", index=False)
test.to_csv(f"{OUT_DIR}/metro_2025_regression_test.csv", index=False)

print("rows: full =", len(full), " train =", len(train), " test =", len(test))
print("is_burdened rate, train:", round(train["is_burdened"].mean(), 3),
      " test:", round(test["is_burdened"].mean(), 3))
print("DONE")
