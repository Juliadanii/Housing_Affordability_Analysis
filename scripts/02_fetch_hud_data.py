"""
02_fetch_hud_data.py
Download HUD Fair Market Rent (FMR) data for benchmarking local rents.

HUD publishes FMR files at:
  https://www.huduser.gov/portal/datasets/fmr.html

This script expects the county-level FMR CSV to be downloaded manually
(HUD occasionally changes direct URLs) and placed in data/raw/ as
`hud_fmr.csv`. It then standardizes column names for merging.

Alternatively, register for the HUD API at https://www.huduser.gov/hudapi/
and set HUD_API_TOKEN to pull FMRs programmatically.
"""

import os
import pandas as pd

RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
IN_PATH = os.path.join(RAW_DIR, "hud_fmr.csv")
OUT_PATH = os.path.join(RAW_DIR, "hud_fmr_clean.csv")

COLUMN_MAP = {
    # common HUD FMR column names -> standardized names
    "fmr_0": "fmr_studio",
    "fmr_1": "fmr_1br",
    "fmr_2": "fmr_2br",
    "fmr_3": "fmr_3br",
    "fmr_4": "fmr_4br",
    "state_alpha": "state_abbr",
    "countyname": "county_name",
    "metro_name": "metro_name",
}


def main():
    if not os.path.exists(IN_PATH):
        print(f"Missing {IN_PATH}")
        print("Download the latest county-level FMR file from")
        print("https://www.huduser.gov/portal/datasets/fmr.html and save it there.")
        return

    df = pd.read_csv(IN_PATH)
    df.columns = [c.strip().lower() for c in df.columns]
    df = df.rename(columns={k: v for k, v in COLUMN_MAP.items() if k in df.columns})

    keep = [c for c in ["state_abbr", "county_name", "metro_name",
                        "fmr_studio", "fmr_1br", "fmr_2br", "fmr_3br", "fmr_4br"]
            if c in df.columns]
    df = df[keep].drop_duplicates()

    df.to_csv(OUT_PATH, index=False)
    print(f"Saved {len(df):,} rows -> {OUT_PATH}")


if __name__ == "__main__":
    main()
