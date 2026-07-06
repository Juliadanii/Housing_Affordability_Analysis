# Tableau Dashboard Notes

**Data sources:** the three extracts in `data/processed/`
(`tableau_cost_burden.csv`, `tableau_rent_to_income.csv`, `tableau_demographics.csv`).

## Dashboard 1 — Regional Housing Affordability
- Filled map of states colored by `pct_burdened`
- Year filter (2019 / 2021 / 2023) to show change over time
- Tooltip: median rent, median income, severe burden %

## Dashboard 2 — Rent-to-Income Ratios
- Bar chart of top 20 metros by `rent_to_income_pct` with a 30% reference line
- Line chart of ratio over time for selected geographies
- Highlight flag for areas exceeding the 30% threshold

## Dashboard 3 — Demographic Patterns
- Scatter: renter share (x) vs. % renters burdened (y), sized by population
- Quartile breakdown: burden rate by income quartile
- Segment filter (High / Moderate / Low renter share)

## Publishing
Publish to Tableau Public and paste the link here + in the README:
`https://public.tableau.com/app/profile/<your-profile>`
