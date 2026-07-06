-- rent_to_income.sql
-- Rent-to-income ratios by geography, with change over time and a
-- flag for areas exceeding the 30% affordability threshold.

WITH by_year AS (
    SELECT
        geo_name,
        geo_level,
        year,
        rent_to_income_ratio,
        median_gross_rent,
        median_household_income
    FROM acs_housing
),
first_last AS (
    SELECT
        geo_name,
        geo_level,
        MIN(year) AS first_year,
        MAX(year) AS last_year
    FROM by_year
    GROUP BY geo_name, geo_level
)
SELECT
    b.geo_name,
    b.geo_level,
    b.year,
    ROUND(b.rent_to_income_ratio * 100, 1) AS rent_to_income_pct,
    ROUND(b.median_gross_rent, 0)          AS median_rent,
    ROUND(b.median_household_income, 0)    AS median_income,
    CASE WHEN b.rent_to_income_ratio >= 0.30 THEN 1 ELSE 0 END AS exceeds_30pct_threshold,
    ROUND(
        (b.rent_to_income_ratio
         - FIRST_VALUE(b.rent_to_income_ratio) OVER (
               PARTITION BY b.geo_name, b.geo_level ORDER BY b.year
           )) * 100, 1
    ) AS change_vs_first_year_pts
FROM by_year b
JOIN first_last f
  ON b.geo_name = f.geo_name AND b.geo_level = f.geo_level
ORDER BY b.geo_level, b.geo_name, b.year;
