# Housing Affordability and Policy Analysis

**Aug 2025 – Oct 2025**

End-to-end analysis of U.S. housing affordability using public datasets (U.S. Census ACS, HUD). The project collects, cleans, and merges data with SQL and Python, analyzes cost burden and demographic trends, visualizes results in Tableau, and summarizes findings in a policy-style report for non-technical decision-makers.

## Key Questions

1. Where is housing cost burden (30%+ of income on housing) most severe, and how has it changed?
2. How do rent-to-income ratios vary by region and metro area?
3. Which demographic groups (by income bracket, race/ethnicity, age, tenure) are most affected?
4. What data-backed policy levers could improve affordability?

## Tech Stack

- **Python** (pandas, requests, SQLAlchemy) — data collection via Census API, cleaning, merging
- **SQL (SQLite)** — storage, transformation, and analysis queries
- **Tableau** — interactive dashboards (regional affordability, rent-to-income, demographics)
- **Data sources** — American Community Survey (ACS 5-Year), HUD Fair Market Rents, HUD Income Limits

## Project Structure

```
housing-affordability-analysis/
├── data/
│   ├── raw/               # Downloaded source data (gitignored)
│   └── processed/         # Cleaned, analysis-ready CSVs
├── scripts/
│   ├── 01_fetch_acs_data.py       # Pull ACS variables via Census API
│   ├── 02_fetch_hud_data.py       # Download HUD FMR data
│   ├── 03_clean_merge.py          # Clean, standardize, merge into SQLite
│   └── 04_analysis.py             # Compute metrics, export Tableau extracts
├── sql/
│   ├── schema.sql                 # Database schema
│   ├── cost_burden_analysis.sql   # Cost burden by state/metro
│   ├── rent_to_income.sql         # Rent-to-income ratio queries
│   └── demographic_trends.sql     # Affordability by demographic group
├── tableau/
│   └── dashboard_notes.md         # Dashboard design + published link
├── reports/
│   └── policy_report.md           # Policy-style summary report
└── requirements.txt
```

## How to Run

```bash
pip install -r requirements.txt

# 1. Get a free Census API key: https://api.census.gov/data/key_signup.html
export CENSUS_API_KEY="your_key_here"

# 2. Run the pipeline
python scripts/01_fetch_acs_data.py
python scripts/02_fetch_hud_data.py
python scripts/03_clean_merge.py
python scripts/04_analysis.py
```

Outputs land in `data/processed/` and are used as Tableau data sources.

## Key Findings (Summary)

- Renters are disproportionately cost-burdened relative to homeowners, with the gap widest in coastal metros.
- Median rent-to-income ratios exceed the 30% affordability threshold in a growing share of metro areas.
- Cost burden falls hardest on households earning under $50K, where a majority of renters are moderately or severely burdened.
- Full findings and recommendations: [`reports/policy_report.md`](reports/policy_report.md)

## Author

Julia — B.S. Computer Science & Financial Economics, UMBC
