"""
Module 2 data prep: the single, unlabeled, numeric table that clustering
and PCA both run on.
=======================================================================
Clustering and PCA both require unlabeled numeric data on comparable
scales. This script takes the 2025 cross-section of metro_year_panel.csv
(one row per metropolitan area, 894 of them) rather than pooling all 26
years, because pooling years would mostly cluster by year (prices trend
up for nearly everyone over time) rather than by what actually
distinguishes one housing market from another in a given year.

Standardizing (z-score) is required before either method because the
input columns are on very different scales (dollars in the hundreds of
thousands vs. percentages vs. small ratios). Without it, zhvi would
dominate distance and variance purely because of its units, not because
it is more important.

INPUT
  data_clean/metro_year_panel.csv   written by build_datasets.py

OUTPUTS
  data_clean/metro_2025_unsupervised.csv          raw values, 894 x 11
  data_clean/metro_2025_unsupervised_scaled.csv   z-scored, same shape

Run: python3 prep_unsupervised_data.py
"""
import pandas as pd
from sklearn.preprocessing import StandardScaler

IN = "data_clean/metro_year_panel.csv"
OUT_DIR = "data_clean"

FEATURES = [
    "zhvi",
    "zhvi_yoy_pct",
    "zhvi_3yr_pct",
    "zhvi_5yr_pct",
    "zhvi_volatility_5yr",
    "zhvi_vs_national",
    "zhvi_pctile_in_year",
    "price_to_income_25_34",
    "years_to_down_payment_25_34",
    "monthly_payment_usd",
    "payment_to_income_pct_25_34",
]

panel = pd.read_csv(IN)
d25 = panel[(panel.year == 2025) & (panel.region_type == "msa")].copy()
d25 = d25.dropna(subset=FEATURES)
d25 = d25.reset_index(drop=True)

assert d25.shape[0] == 894, d25.shape

raw = d25[["region_id", "region_name", "state_name"] + FEATURES].copy()
raw.to_csv(f"{OUT_DIR}/metro_2025_unsupervised.csv", index=False)

scaler = StandardScaler()
X = scaler.fit_transform(d25[FEATURES])
scaled = pd.DataFrame(X, columns=FEATURES)
scaled.insert(0, "region_name", d25["region_name"].values)
scaled.insert(1, "state_name", d25["state_name"].values)
scaled.to_csv(f"{OUT_DIR}/metro_2025_unsupervised_scaled.csv", index=False)

print("shape:", raw.shape)
print("wrote:", f"{OUT_DIR}/metro_2025_unsupervised.csv")
print("wrote:", f"{OUT_DIR}/metro_2025_unsupervised_scaled.csv")
