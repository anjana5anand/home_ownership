# Gen Z Homeownership — Module 1 Project

Research topic: how the likelihood of homeownership for Americans in their
twenties and early thirties has changed relative to earnings, home prices and
borrowing costs over the past two decades.

## Layout

```
.
├── acs_api_fetch.py      Census ACS API pull  → data_clean/acs_metro_annual.csv
├── fred_api_fetch.py     FRED API pull        → data_clean/fred_annual.csv
├── build_datasets.py     cleaning pipeline    → data_clean/*.csv
├── data_raw/             raw sources, never edited
│   ├── histtab12.xlsx    HVS households by age of householder, annual
│   ├── LEU02528*.csv     FRED earnings, original manual downloads
│   ├── Metro_zhvi_*.csv  Zillow ZHVI, monthly by metro
│   ├── fred/             FRED API responses (JSON) + fred_annual.csv
│   └── acs/              ACS API responses (JSON) + acs_metro_annual.csv
├── data_clean/           pipeline output — safe to delete, `build_datasets.py` rebuilds it
├── docs/                 the website (GitHub Pages serves from here)
└── archive/              first-pass scripts, and HVS tables 17/19 (parsed once, cut as off-topic)
```

## Running it

```bash
python3 fred_api_fetch.py     # needs fred_api_key.txt
python3 acs_api_fetch.py      # needs census_api_key.txt
python3 build_datasets.py     # reads data_raw/ + data_clean/, writes data_clean/
```

`build_datasets.py` runs with or without the API files — it falls back to the
manual downloads in `data_raw/` and says so in its output.

## Data sources

| Source | Access | Coverage |
|---|---|---|
| Census Housing Vacancy Survey, Table 12 | download | 1982–2025 |
| BLS via FRED, 8 series | **API** | 2000–2026 |
| Zillow ZHVI, metro | download | 2000–2026, 894 metros |
| Census ACS 1-year, metro | **API** | 2005–2024, no 2020 |

## Notes

- API keys live in `fred_api_key.txt` / `census_api_key.txt`, both gitignored.
  Never commit them.
- Census did not publish standard ACS 1-year estimates for 2020; the gap is real.
- `data_clean/_data_quality_report.txt` records row counts and missing values
  for every generated table.
