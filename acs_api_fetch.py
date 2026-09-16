"""
ACS API collection script  -  Gen Z Homeownership project
==========================================================
Satisfies the API requirement: pulls American Community Survey 1-year
estimates from the Census Bureau API at the metropolitan-statistical-area
level and writes them to tidy CSVs.

API SOURCE   : U.S. Census Bureau, American Community Survey 1-Year Data API
BASE URL     : https://api.census.gov/data/{year}/acs/acs1
DOCS         : https://www.census.gov/data/developers/data-sets/acs-1year.html
KEY SIGNUP   : https://api.census.gov/data/key_signup.html   (free, instant)

EXAMPLE GET ENDPOINT (this is the one to paste into the DataPrep_EDA tab):
  https://api.census.gov/data/2023/acs/acs1
      ?get=NAME,B25007_001E,B25007_004E,B25007_014E
      &for=metropolitan%20statistical%20area/micropolitan%20statistical%20area:*
      &key=YOUR_KEY

TABLES REQUESTED
  B25007  Tenure by Age of Householder   -> owner/renter counts per age bracket
  B19049  Median Household Income by Age of Householder
  B25077  Median Value (owner-occupied housing units)
  B25064  Median Gross Rent

NOTE ON 2020: the Census Bureau did not release standard ACS 1-year estimates
for 2020 because pandemic disruption pushed response rates below their quality
standards. The script skips it automatically; the gap is real, not a bug.

SETUP
  1. Request a key at the URL above (takes about a minute).
  2. Save it in a file next to this script called  census_api_key.txt
     containing nothing but the key.
  3. python3 acs_api_fetch.py

Nothing here needs a third-party package; it uses only the standard library.
"""

import csv
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request

OUT_DIR   = "data_raw/acs"
RAW_DIR   = "data_raw/acs"          # untouched API responses, for the "link to raw data" requirement
KEY_FILE  = "census_api_key.txt"
YEARS     = [y for y in range(2005, 2025) if y != 2020]   # 2020 not published
GEO       = "metropolitan statistical area/micropolitan statistical area:*"

TABLES = ["B25007", "B19049", "B25077", "B25064"]

# Labels are matched rather than hard-coding variable numbers, because the
# Census Bureau has renumbered variables between vintages before.
WANTED_LABELS = {
    "B25007": [
        ("owner_total",      ["owner occupied"]),
        ("owner_15_24",      ["owner occupied", "15 to 24"]),
        ("owner_25_34",      ["owner occupied", "25 to 34"]),
        ("renter_total",     ["renter occupied"]),
        ("renter_15_24",     ["renter occupied", "15 to 24"]),
        ("renter_25_34",     ["renter occupied", "25 to 34"]),
    ],
    "B19049": [
        ("median_hh_income_all",      ["total"]),
        ("median_hh_income_under25",  ["under 25"]),
        ("median_hh_income_25_44",    ["25 to 44"]),
    ],
    "B25077": [("median_home_value", ["total"])],
    "B25064": [("median_gross_rent", ["total"])],
}


def read_key():
    if not os.path.exists(KEY_FILE):
        raise SystemExit(
            "No {} found.\nRequest a free key at "
            "https://api.census.gov/data/key_signup.html and save it in that "
            "file (the key alone, nothing else).".format(KEY_FILE)
        )
    key = open(KEY_FILE).read().strip()
    if not key:
        raise SystemExit("{} is empty.".format(KEY_FILE))
    return key


def get_json(url, tries=3):
    for attempt in range(tries):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                return json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None                      # vintage/table not published
            if attempt == tries - 1:
                raise
        except Exception:
            if attempt == tries - 1:
                raise
        time.sleep(2 * (attempt + 1))
    return None


def normalise(label):
    return label.lower().replace("!!", " ").replace(":", " ")


def resolve_variables(year, table):
    """Return {friendly_name: census_variable_id} by matching label text."""
    meta = get_json(
        "https://api.census.gov/data/{}/acs/acs1/groups/{}.json".format(year, table)
    )
    if not meta:
        return {}
    variables = meta.get("variables", {})
    resolved = {}
    for friendly, needles in WANTED_LABELS[table]:
        best = None
        for var_id, info in variables.items():
            if not var_id.endswith("E"):
                continue
            label = normalise(info.get("label", ""))
            if all(n in label for n in needles):
                # prefer the shortest matching label: the least-nested cell
                if best is None or len(label) < best[1]:
                    best = (var_id, len(label))
        if best:
            resolved[friendly] = best[0]
    return resolved


def fetch_year(year, key):
    os.makedirs(RAW_DIR, exist_ok=True)
    per_metro = {}
    for table in TABLES:
        varmap = resolve_variables(year, table)
        if not varmap:
            print("  {} {}: not available".format(year, table))
            continue

        var_ids = list(varmap.values())
        url = "https://api.census.gov/data/{}/acs/acs1?{}".format(
            year,
            urllib.parse.urlencode(
                {"get": "NAME," + ",".join(var_ids), "for": GEO, "key": key}
            ),
        )
        data = get_json(url)
        if not data:
            print("  {} {}: no data returned".format(year, table))
            continue

        with open("{}/{}_{}.json".format(RAW_DIR, table, year), "w") as f:
            json.dump(data, f)

        header, rows = data[0], data[1:]
        idx = {col: i for i, col in enumerate(header)}
        reverse = {v: k for k, v in varmap.items()}

        for row in rows:
            cbsa = row[idx["metropolitan statistical area/micropolitan statistical area"]]
            rec = per_metro.setdefault(cbsa, {"cbsa": cbsa, "name": row[idx["NAME"]], "year": year})
            for var_id in var_ids:
                val = row[idx[var_id]]
                try:
                    num = float(val)
                except (TypeError, ValueError):
                    num = None
                # Census uses large negative sentinels for suppressed cells
                if num is not None and num < 0:
                    num = None
                rec[reverse[var_id]] = num

        print("  {} {}: {} metros".format(year, table, len(rows)))
        time.sleep(0.4)
    return list(per_metro.values())


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    key = read_key()
    all_rows = []
    for year in YEARS:
        print(year)
        all_rows.extend(fetch_year(year, key))

    if not all_rows:
        raise SystemExit("Nothing fetched. Check the key and network.")

    fields = ["cbsa", "name", "year"]
    for table in TABLES:
        for friendly, _ in WANTED_LABELS[table]:
            if friendly not in fields:
                fields.append(friendly)
    fields += ["ownership_rate_25_34_pct", "ownership_rate_all_pct"]

    for r in all_rows:
        o, rt = r.get("owner_25_34"), r.get("renter_25_34")
        r["ownership_rate_25_34_pct"] = (
            round(o / (o + rt) * 100, 2) if o is not None and rt is not None and (o + rt) else None
        )
        o, rt = r.get("owner_total"), r.get("renter_total")
        r["ownership_rate_all_pct"] = (
            round(o / (o + rt) * 100, 2) if o is not None and rt is not None and (o + rt) else None
        )

    all_rows.sort(key=lambda r: (r["name"], r["year"]))
    out = os.path.join(OUT_DIR, "acs_metro_annual.csv")
    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(all_rows)

    metros = len({r["cbsa"] for r in all_rows})
    years = sorted({r["year"] for r in all_rows})
    print("\nWrote {}".format(out))
    print("{} rows | {} metros | {}-{} ({} years, 2020 absent)".format(
        len(all_rows), metros, years[0], years[-1], len(years)))
    print("Raw API responses saved in {}/".format(RAW_DIR))


if __name__ == "__main__":
    main()
