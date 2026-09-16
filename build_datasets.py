"""
Data preparation and cleaning pipeline  -  Gen Z Homeownership project
=======================================================================
Reads every raw source, cleans each one, and writes tidy analysis tables to
data_clean/. Also writes a data-quality report so the cleaning is auditable.

RAW INPUTS (all under data_raw/)
  histtab12.xlsx  Census HVS Table 12 - household counts by age of householder,
                  annual, 1982-present. Repeating year-block layout.
  Metro_zhvi_*.csv  Zillow ZHVI - typical home value by metro, monthly, wide.
  data_raw/fred/fred_annual.csv  written by fred_api_fetch.py (optional; skipped if absent)
  data_raw/acs/acs_metro_annual.csv  written by acs_api_fetch.py (optional; skipped if absent)

OUTPUTS (data_clean/)
  ownership_by_age_annual.csv       year x age bracket, counts + rate
  zhvi_metro_annual.csv             metro x year, typical home value
  national_annual.csv               year, all national series joined
  metro_year_panel.csv              metro x year with engineered features
  _data_quality_report.txt          row counts, missing values, ranges

Run: python3 build_datasets.py
"""

import os
import re
import warnings

import numpy as np
import pandas as pd

warnings.simplefilter("ignore")

RAW = "data_raw"
OUT = "data_clean"
SAVINGS_RATE = 0.15      # ASSUMPTION - a modelling choice, not measured. State it on the site.
DOWN_PAYMENT = 0.20

os.makedirs(OUT, exist_ok=True)
report = []


def log(msg):
    print(msg)
    report.append(msg)



def monthly_payment(price, annual_rate_pct, ltv=1 - DOWN_PAYMENT, years=30):
    """Monthly principal+interest on a standard fixed-rate mortgage.
    Needed because price-to-income ignores the cost of borrowing: a 2020 house
    at 3.1% and a 2000 house at 8.1% are not comparable on price alone."""
    principal = price * ltv
    r = annual_rate_pct / 100.0 / 12.0
    n = years * 12
    return principal * r * (1 + r) ** n / ((1 + r) ** n - 1)


# --------------------------------------------------------------------------
# 1. HVS Table 12  -  household counts by age of householder (annual)
# --------------------------------------------------------------------------

def clean_label(s):
    if s is None:
        return None
    return re.sub(r"[.\s]+$", "", str(s)).strip().lstrip(".").strip()


def parse_histtab12(path=f"{RAW}/histtab12.xlsx"):
    import openpyxl
    ws = openpyxl.load_workbook(path, data_only=True)["Sheet1"]
    rows = list(ws.iter_rows(values_only=True))

    targets = {"less than 25 years": "<25", "25 to 29 years": "25-29",
               "30 to 34 years": "30-34", "35 to 39 years": "35-39",
               "40 to 44 years": "40-44"}

    records, i, n = [], 0, len(rows)
    while i < n:
        if rows[i][0] and str(rows[i][0]).strip() == "Age of Householder":
            header = rows[i]
            years = [(c, re.sub(r"[a-zA-Z]", "", str(header[c])))
                     for c in range(1, len(header), 2) if header[c] is not None]
            j = i + 3
            while j < n and not (rows[j][0] and str(rows[j][0]).strip() == "Age of Householder"):
                label = clean_label(rows[j][0]) if rows[j][0] else None
                if label:
                    key = label.lower()
                    for tlabel, code in targets.items():
                        if tlabel in key:
                            for col, y in years:
                                total = rows[j][col] if col < len(rows[j]) else None
                                owner = rows[j][col + 1] if col + 1 < len(rows[j]) else None
                                if total is not None:
                                    records.append((y, code, total, owner))
                j += 1
            i = j
        else:
            i += 1

    df = pd.DataFrame(records, columns=["year_raw", "age_bracket", "total", "owner"])
    df["year"] = pd.to_numeric(df["year_raw"].str.extract(r"(\d{4})")[0], errors="coerce")
    df = df.dropna(subset=["year"])
    df["year"] = df["year"].astype(int)
    # revised vintages repeat a year; the later block supersedes the earlier one
    df = df.drop_duplicates(subset=["year", "age_bracket"], keep="last")
    df["total"] = pd.to_numeric(df["total"], errors="coerce")
    df["owner"] = pd.to_numeric(df["owner"], errors="coerce")
    df["ownership_rate_pct"] = (df["owner"] / df["total"] * 100).round(2)
    df = df[["year", "age_bracket", "total", "owner", "ownership_rate_pct"]]
    df.columns = ["year", "age_bracket", "total_households_thousands",
                  "owner_households_thousands", "ownership_rate_pct"]
    return df.sort_values(["year", "age_bracket"]).reset_index(drop=True)


# --------------------------------------------------------------------------
# 2. Zillow ZHVI  -  wide monthly to long annual
# --------------------------------------------------------------------------

def parse_zhvi(path=f"{RAW}/Metro_zhvi_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv"):
    wide = pd.read_csv(path)
    id_cols = ["RegionID", "SizeRank", "RegionName", "RegionType", "StateName"]
    date_cols = [c for c in wide.columns if c not in id_cols]

    long = wide.melt(id_vars=id_cols, value_vars=date_cols,
                     var_name="month", value_name="zhvi").dropna(subset=["zhvi"])
    long["year"] = long["month"].str.slice(0, 4).astype(int)
    long["month_num"] = long["month"].str.slice(5, 7).astype(int)

    # one value per metro-year: the latest month reported that year
    long = long.sort_values(["RegionID", "year", "month_num"])
    # StateName is empty for the national row; without dropna=False groupby
    # silently discards it and the whole national series disappears.
    long["StateName"] = long["StateName"].fillna("")
    annual = long.groupby(["RegionID", "RegionName", "RegionType", "StateName", "year"],
                          as_index=False, dropna=False).last()
    annual = annual[["RegionID", "RegionName", "RegionType", "StateName",
                     "year", "zhvi", "month_num"]]
    annual.columns = ["region_id", "region_name", "region_type", "state_name",
                      "year", "zhvi", "as_of_month"]
    annual["zhvi"] = annual["zhvi"].round(0)
    return annual.sort_values(["region_name", "year"]).reset_index(drop=True)


# --------------------------------------------------------------------------
# run
# --------------------------------------------------------------------------

log("=" * 68)
log("DATA PREPARATION REPORT")
log("=" * 68)

own_annual = parse_histtab12()
own_annual.to_csv(f"{OUT}/ownership_by_age_annual.csv", index=False)
log(f"\nownership_by_age_annual.csv       {len(own_annual):>6,} rows  "
    f"{own_annual.year.min()}-{own_annual.year.max()}  "
    f"{own_annual.age_bracket.nunique()} age brackets")

zhvi = parse_zhvi()
zhvi.to_csv(f"{OUT}/zhvi_metro_annual.csv", index=False)
log(f"zhvi_metro_annual.csv             {len(zhvi):>6,} rows  "
    f"{zhvi.region_name.nunique()} regions  {zhvi.year.min()}-{zhvi.year.max()}")

# ---- national annual table -------------------------------------------------

if os.path.exists(f"{RAW}/fred/fred_annual.csv"):
    fred = pd.read_csv(f"{RAW}/fred/fred_annual.csv")
    log("\nfred_annual.csv found - using API-sourced earnings and rates")
else:
    e1 = pd.read_csv(f"{RAW}/LEU0252887100Q.csv")
    e2 = pd.read_csv(f"{RAW}/LEU0252888500Q.csv")
    for d, col in ((e1, "median_weekly_earnings_20_24"), (e2, "median_weekly_earnings_25_34")):
        d.columns = ["observation_date", col]
        d["year"] = d["observation_date"].str.slice(0, 4).astype(int)
    fred = (e1.groupby("year")["median_weekly_earnings_20_24"].mean().round(2).reset_index()
            .merge(e2.groupby("year")["median_weekly_earnings_25_34"].mean().round(2).reset_index(),
                   on="year"))
    fred["annual_earnings_20_24"] = (fred["median_weekly_earnings_20_24"] * 52).round(0)
    fred["annual_earnings_25_34"] = (fred["median_weekly_earnings_25_34"] * 52).round(0)
    log("\nfred_annual.csv NOT found - falling back to the downloaded CSVs.")
    log("  Run fred_api_fetch.py to satisfy the API requirement and add mortgage rates.")

own_wide = own_annual.pivot(index="year", columns="age_bracket",
                            values="ownership_rate_pct").reset_index()
own_wide.columns = ["year"] + [f"ownership_rate_{c.replace('<', 'lt').replace('-', '_')}_pct"
                               for c in own_wide.columns[1:]]

national_zhvi = (zhvi[zhvi.region_type == "country"][["year", "zhvi"]]
                 .rename(columns={"zhvi": "national_zhvi"}))

national = own_wide.merge(fred, on="year").merge(national_zhvi, on="year")
national["price_to_income_25_34"] = (national["national_zhvi"] /
                                     national["annual_earnings_25_34"]).round(2)
national["years_to_down_payment_25_34"] = (
    (DOWN_PAYMENT * national["national_zhvi"]) /
    (national["annual_earnings_25_34"] * SAVINGS_RATE)).round(1)
if "mortgage_rate_30yr_pct" in national.columns:
    national["monthly_payment_usd"] = national.apply(
        lambda r: monthly_payment(r["national_zhvi"], r["mortgage_rate_30yr_pct"]), axis=1).round(0)
    national["payment_to_income_pct_25_34"] = (
        national["monthly_payment_usd"] * 12 / national["annual_earnings_25_34"] * 100).round(1)
national.to_csv(f"{OUT}/national_annual.csv", index=False)
log(f"national_annual.csv               {len(national):>6,} rows  "
    f"{national.year.min()}-{national.year.max()}  {national.shape[1]} columns")

# ---- metro-year panel with engineered features -----------------------------

panel = zhvi[zhvi.region_type == "msa"].copy()
panel = panel[panel.year.between(2000, 2025)].sort_values(["region_id", "year"])

g = panel.groupby("region_id")["zhvi"]
panel["zhvi_yoy_pct"]   = (g.pct_change(1) * 100).round(2)
panel["zhvi_3yr_pct"]   = (g.pct_change(3) * 100).round(2)
panel["zhvi_5yr_pct"]   = (g.pct_change(5) * 100).round(2)
panel["zhvi_volatility_5yr"] = (panel.groupby("region_id")["zhvi_yoy_pct"]
                                .transform(lambda s: s.rolling(5, min_periods=3).std()).round(2))

carry = ["year", "national_zhvi", "annual_earnings_25_34", "annual_earnings_20_24",
         "ownership_rate_25_29_pct", "ownership_rate_30_34_pct"]
for optional in ["mortgage_rate_30yr_pct", "annual_earnings_25_34_real2025"]:
    if optional in national.columns:
        carry.append(optional)
panel = panel.merge(national[carry], on="year", how="left")
panel["zhvi_vs_national"] = (panel["zhvi"] / panel["national_zhvi"]).round(3)
panel["zhvi_pctile_in_year"] = (panel.groupby("year")["zhvi"]
                                .rank(pct=True).mul(100).round(1))
panel["price_to_income_25_34"] = (panel["zhvi"] / panel["annual_earnings_25_34"]).round(2)
panel["years_to_down_payment_25_34"] = (
    (DOWN_PAYMENT * panel["zhvi"]) /
    (panel["annual_earnings_25_34"] * SAVINGS_RATE)).round(1)
if "mortgage_rate_30yr_pct" in panel.columns:
    panel["monthly_payment_usd"] = (
        panel["zhvi"] * (1 - DOWN_PAYMENT)
        * (panel["mortgage_rate_30yr_pct"] / 1200)
        * (1 + panel["mortgage_rate_30yr_pct"] / 1200) ** 360
        / ((1 + panel["mortgage_rate_30yr_pct"] / 1200) ** 360 - 1)).round(0)
    panel["payment_to_income_pct_25_34"] = (
        panel["monthly_payment_usd"] * 12 / panel["annual_earnings_25_34"] * 100).round(1)

panel["affordability_quartile"] = (panel.groupby("year")["price_to_income_25_34"]
                                   .transform(lambda s: pd.qcut(s, 4, duplicates="drop",
                                                                labels=False) + 1
                                              if s.notna().sum() >= 4 else pd.Series(index=s.index, dtype="float")))
panel["affordability_quartile"] = panel["affordability_quartile"].map(
    {1: "Q1_most_affordable", 2: "Q2", 3: "Q3", 4: "Q4_least_affordable"})
panel.to_csv(f"{OUT}/metro_year_panel.csv", index=False)
log(f"metro_year_panel.csv              {len(panel):>6,} rows  "
    f"{panel.region_id.nunique()} metros  {panel.shape[1]} columns")

if os.path.exists(f"{RAW}/acs/acs_metro_annual.csv"):
    log("\nacs_metro_annual.csv found - join it for metro-level ownership rates.")
else:
    log("\nacs_metro_annual.csv NOT found - metro-level ownership rate unavailable.")
    log("  Run acs_api_fetch.py if the target for Part 2 should be a real ownership rate.")

# ---- data quality ----------------------------------------------------------

log("\n" + "=" * 68)
log("DATA QUALITY")
log("=" * 68)

for name, df in [("ownership_by_age_annual", own_annual),
                 ("national_annual", national),
                 ("metro_year_panel", panel)]:
    miss = df.isna().sum()
    miss = miss[miss > 0]
    log(f"\n{name}  ({len(df):,} rows x {df.shape[1]} cols)")
    if miss.empty:
        log("  no missing values")
    else:
        for col, n in miss.items():
            log(f"  {col:<34} {n:>6,} missing ({n/len(df)*100:.1f}%)")

log("\nExpected missingness, not errors:")
log("  zhvi_yoy_pct / 3yr / 5yr    first years of each metro have no prior year")
log("  zhvi_volatility_5yr         needs at least 3 yearly changes")

with open(f"{OUT}/_data_quality_report.txt", "w") as f:
    f.write("\n".join(report) + "\n")
print(f"\nReport written to {OUT}/_data_quality_report.txt")
