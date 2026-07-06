"""
04_analysis.py
Run the SQL analysis queries against housing.db and export
Tableau-ready CSV extracts to data/processed/.
"""

import os
import sqlite3
import pandas as pd

BASE = os.path.join(os.path.dirname(__file__), "..")
DB_PATH = os.path.join(BASE, "data", "processed", "housing.db")
SQL_DIR = os.path.join(BASE, "sql")
OUT_DIR = os.path.join(BASE, "data", "processed")

QUERIES = {
    "cost_burden_analysis.sql": "tableau_cost_burden.csv",
    "rent_to_income.sql": "tableau_rent_to_income.csv",
    "demographic_trends.sql": "tableau_demographics.csv",
}


def main():
    conn = sqlite3.connect(DB_PATH)

    for sql_file, out_csv in QUERIES.items():
        path = os.path.join(SQL_DIR, sql_file)
        with open(path) as f:
            query = f.read()
        df = pd.read_sql_query(query, conn)
        out_path = os.path.join(OUT_DIR, out_csv)
        df.to_csv(out_path, index=False)
        print(f"{sql_file}: {len(df):,} rows -> {out_csv}")

    # Quick headline stats for the report
    summary = pd.read_sql_query(
        """
        SELECT year,
               ROUND(AVG(pct_renters_cost_burdened) * 100, 1) AS avg_pct_burdened,
               ROUND(AVG(rent_to_income_ratio) * 100, 1)      AS avg_rent_to_income_pct
        FROM acs_housing
        WHERE geo_level = 'state'
        GROUP BY year
        ORDER BY year
        """,
        conn,
    )
    print("\nHeadline trends (state-level averages):")
    print(summary.to_string(index=False))

    conn.close()


if __name__ == "__main__":
    main()
