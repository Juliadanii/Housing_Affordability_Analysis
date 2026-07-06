"""
01_fetch_acs_data.py
Fetch housing affordability variables from the U.S. Census ACS 5-Year API
at the state and metro (CBSA) level.

Requires a free Census API key:
  https://api.census.gov/data/key_signup.html
  export CENSUS_API_KEY="your_key"
"""

import os
import time
import requests
import pandas as pd

API_KEY = os.environ.get("CENSUS_API_KEY", "")
BASE_URL = "https://api.census.gov/data"
YEARS = [2019, 2021, 2023]  # ACS 5-year vintages to compare over time
RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")

# ACS variables of interest
VARIABLES = {
    "NAME": "geo_name",
    "B19013_001E": "median_household_income",
    "B25064_001E": "median_gross_rent",
    "B25077_001E": "median_home_value",
    "B25070_001E": "renters_total",           # Gross rent as % of income - total
    "B25070_007E": "rent_burden_30_34",       # 30.0–34.9%
    "B25070_008E": "rent_burden_35_39",       # 35.0–39.9%
    "B25070_009E": "rent_burden_40_49",       # 40.0–49.9%
    "B25070_010E": "rent_burden_50_plus",     # 50%+
    "B25003_001E": "occupied_units_total",
    "B25003_002E": "owner_occupied",
    "B25003_003E": "renter_occupied",
    "B01003_001E": "total_population",
}

GEOGRAPHIES = {
    "state": "state:*",
    "metro": "metropolitan statistical area/micropolitan statistical area:*",
}


def fetch_acs(year: int, geo_label: str, geo_query: str) -> pd.DataFrame:
    """Fetch one geography level for one ACS vintage."""
    var_list = ",".join(VARIABLES.keys())
    url = f"{BASE_URL}/{year}/acs/acs5"
    params = {"get": var_list, "for": geo_query}
    if API_KEY:
        params["key"] = API_KEY

    resp = requests.get(url, params=params, timeout=60)
    resp.raise_for_status()
    rows = resp.json()

    df = pd.DataFrame(rows[1:], columns=rows[0])
    df = df.rename(columns=VARIABLES)
    df["year"] = year
    df["geo_level"] = geo_label
    return df


def main():
    os.makedirs(RAW_DIR, exist_ok=True)
    frames = []

    for year in YEARS:
        for geo_label, geo_query in GEOGRAPHIES.items():
            print(f"Fetching ACS {year} — {geo_label} ...")
            try:
                frames.append(fetch_acs(year, geo_label, geo_query))
            except requests.HTTPError as e:
                print(f"  Skipped ({e})")
            time.sleep(1)  # be polite to the API

    df = pd.concat(frames, ignore_index=True)
    out_path = os.path.join(RAW_DIR, "acs_housing_raw.csv")
    df.to_csv(out_path, index=False)
    print(f"Saved {len(df):,} rows -> {out_path}")


if __name__ == "__main__":
    main()
