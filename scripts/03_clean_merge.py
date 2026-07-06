"""
03_clean_merge.py
Clean the raw ACS data, compute derived affordability fields, and load
everything into a SQLite database (data/processed/housing.db).
"""

import os
import sqlite3
import pandas as pd

BASE = os.path.join(os.path.dirname(__file__), "..")
RAW = os.path.join(BASE, "data", "raw")
PROCESSED = os.path.join(BASE, "data", "processed")
DB_PATH = os.path.join(PROCESSED, "housing.db")

NUMERIC_COLS = [
    "median_household_income", "median_gross_rent", "median_home_value",
    "renters_total", "rent_burden_30_34", "rent_burden_35_39",
    "rent_burden_40_49", "rent_burden_50_plus",
    "occupied_units_total", "owner_occupied", "renter_occupied",
    "total_population",
]


def clean_acs(df: pd.DataFrame) -> pd.DataFrame:
    # Census uses large negative sentinels for missing values
    for col in NUMERIC_COLS:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        df.loc[df[col] < 0, col] = pd.NA

    # Drop rows missing the core metrics
    df = df.dropna(subset=["median_household_income", "median_gross_rent"])

    # Derived metrics
    df["rent_to_income_ratio"] = (df["median_gross_rent"] * 12) / df["median_household_income"]
    df["cost_burdened_renters"] = (
        df[["rent_burden_30_34", "rent_burden_35_39",
            "rent_burden_40_49", "rent_burden_50_plus"]].sum(axis=1)
    )
    df["pct_renters_cost_burdened"] = df["cost_burdened_renters"] / df["renters_total"]
    df["pct_severely_burdened"] = df["rent_burden_50_plus"] / df["renters_total"]
    df["renter_share"] = df["renter_occupied"] / df["occupied_units_total"]
    df["price_to_income_ratio"] = df["median_home_value"] / df["median_household_income"]

    return df


def main():
    os.makedirs(PROCESSED, exist_ok=True)

    acs = pd.read_csv(os.path.join(RAW, "acs_housing_raw.csv"))
    acs = clean_acs(acs)

    conn = sqlite3.connect(DB_PATH)
    acs.to_sql("acs_housing", conn, if_exists="replace", index=False)

    fmr_path = os.path.join(RAW, "hud_fmr_clean.csv")
    if os.path.exists(fmr_path):
        fmr = pd.read_csv(fmr_path)
        fmr.to_sql("hud_fmr", conn, if_exists="replace", index=False)
        print(f"Loaded hud_fmr ({len(fmr):,} rows)")

    conn.close()

    acs.to_csv(os.path.join(PROCESSED, "acs_housing_clean.csv"), index=False)
    print(f"Loaded acs_housing ({len(acs):,} rows) -> {DB_PATH}")


if __name__ == "__main__":
    main()
