"""
FRED API collection script  -  Gen Z Homeownership project
===========================================================
Satisfies the API requirement. Replaces the manual CSV downloads of the two
earnings series with programmatic calls, and adds series that the manual
download route made too tedious to bother with.

API SOURCE : Federal Reserve Bank of St. Louis, FRED API
BASE URL   : https://api.stlouisfed.org/fred/series/observations
DOCS       : https://fred.stlouisfed.org/docs/api/fred/
KEY SIGNUP : https://fredaccount.stlouisfed.org/apikeys   (free, instant)

EXAMPLE GET ENDPOINT (paste this into the DataPrep_EDA tab):
  https://api.stlouisfed.org/fred/series/observations
      ?series_id=MORTGAGE30US
      &observation_start=2000-01-01
      &file_type=json
      &api_key=YOUR_KEY

SETUP
  1. Request a key at the URL above.
  2. Save it in  fred_api_key.txt  next to this script (the key alone).
  3. python3 fred_api_fetch.py

Standard library only.
"""

import csv
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict

KEY_FILE = "fred_api_key.txt"
RAW_DIR  = "data_raw/fred"
OUT_DIR  = "data_raw/fred"
START    = "2000-01-01"

# series_id -> (friendly column name, how to collapse sub-annual readings to a year)
SERIES = {
    "LEU0252887100Q": ("median_weekly_earnings_20_24", "mean"),
    "LEU0252888500Q": ("median_weekly_earnings_25_34", "mean"),
    "MORTGAGE30US":   ("mortgage_rate_30yr_pct",       "mean"),
    "RHORUSQ156N":    ("homeownership_rate_us_pct",    "mean"),
    "MSPUS":          ("median_sales_price_usd",       "mean"),
    "CSUSHPINSA":     ("case_shiller_home_price_index","mean"),
    "CPIAUCSL":       ("cpi_all_urban",                "mean"),
    "HOUST":          ("housing_starts_thousands",     "mean"),
}


def read_key():
    if not os.path.exists(KEY_FILE):
        raise SystemExit(
            "No {} found.\nRequest a free key at "
            "https://fredaccount.stlouisfed.org/apikeys and save it in that "
            "file (the key alone, nothing else).".format(KEY_FILE)
        )
    key = open(KEY_FILE).read().strip()
    if not key:
        raise SystemExit("{} is empty.".format(KEY_FILE))
    return key


def api_get(path, params, tries=3):
    url = "https://api.stlouisfed.org/fred/{}?{}".format(path, urllib.parse.urlencode(params))
    for attempt in range(tries):
        try:
            with urllib.request.urlopen(url, timeout=45) as r:
                return json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            if e.code == 400:
                print("    bad request:", e.read().decode()[:200])
                return None
            if attempt == tries - 1:
                raise
        except Exception:
            if attempt == tries - 1:
                raise
        time.sleep(2 * (attempt + 1))
    return None


def fetch_series(series_id, key):
    """Return (metadata_dict, {year: [values]})."""
    meta_payload = api_get("series", {"series_id": series_id, "api_key": key, "file_type": "json"})
    meta = {}
    if meta_payload and meta_payload.get("seriess"):
        s = meta_payload["seriess"][0]
        meta = {
            "series_id": series_id,
            "title": s.get("title"),
            "units": s.get("units"),
            "frequency": s.get("frequency"),
            "seasonal_adjustment": s.get("seasonal_adjustment"),
            "last_updated": s.get("last_updated"),
        }

    obs = api_get("series/observations", {
        "series_id": series_id, "api_key": key, "file_type": "json",
        "observation_start": START,
    })
    if not obs:
        return meta, {}

    os.makedirs(RAW_DIR, exist_ok=True)
    with open("{}/{}.json".format(RAW_DIR, series_id), "w") as f:
        json.dump(obs, f)

    by_year = defaultdict(list)
    for o in obs.get("observations", []):
        if o["value"] in (".", "", None):
            continue                      # FRED marks missing readings with "."
        by_year[int(o["date"][:4])].append(float(o["value"]))
    return meta, by_year


def main():
    key = read_key()
    annual = defaultdict(dict)
    metadata = []
    counts = {}

    for series_id, (col, _how) in SERIES.items():
        print("fetching", series_id)
        meta, by_year = fetch_series(series_id, key)
        if meta:
            metadata.append(meta)
        for year, values in by_year.items():
            annual[year][col] = round(sum(values) / len(values), 3)
        counts[series_id] = (len(by_year), sum(len(v) for v in by_year.values()))
        time.sleep(0.3)

    if not annual:
        raise SystemExit("Nothing fetched. Check the key and network.")

    cols = ["year"] + [c for c, _ in SERIES.values()]
    years = sorted(annual)
    rows = []
    for y in years:
        row = {"year": y}
        row.update(annual[y])
        # derived: annual earnings, and a real-dollar version using CPI
        for bracket in ("20_24", "25_34"):
            weekly = row.get("median_weekly_earnings_" + bracket)
            if weekly is not None:
                row["annual_earnings_" + bracket] = round(weekly * 52, 0)
        rows.append(row)

    base_cpi = annual.get(2025, {}).get("cpi_all_urban")
    if base_cpi:
        for row in rows:
            cpi = row.get("cpi_all_urban")
            if cpi:
                for bracket in ("20_24", "25_34"):
                    nominal = row.get("annual_earnings_" + bracket)
                    if nominal is not None:
                        row["annual_earnings_{}_real2025".format(bracket)] = round(nominal * base_cpi / cpi, 0)

    for extra in ["annual_earnings_20_24", "annual_earnings_25_34",
                  "annual_earnings_20_24_real2025", "annual_earnings_25_34_real2025"]:
        if any(extra in r for r in rows):
            cols.append(extra)

    os.makedirs(OUT_DIR, exist_ok=True)
    with open(f"{OUT_DIR}/fred_annual.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)

    with open(f"{OUT_DIR}/fred_series_metadata.csv", "w", newline="") as f:
        if metadata:
            w = csv.DictWriter(f, fieldnames=list(metadata[0].keys()))
            w.writeheader()
            w.writerows(metadata)

    print("\nWrote {}/fred_annual.csv  ({} years, {}-{})".format(OUT_DIR, len(rows), years[0], years[-1]))
    print("Wrote {}/fred_series_metadata.csv  ({} series documented)".format(OUT_DIR, len(metadata)))
    print("Raw API responses in {}/\n".format(RAW_DIR))
    for sid, (nyears, nobs) in counts.items():
        print("  {:16s} {:3d} years, {:5d} raw observations".format(sid, nyears, nobs))


if __name__ == "__main__":
    main()
