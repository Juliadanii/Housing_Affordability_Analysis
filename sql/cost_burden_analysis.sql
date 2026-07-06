-- cost_burden_analysis.sql
-- Cost burden by geography and year: share of renters paying 30%+ and 50%+
-- of income on housing, ranked by severity within each year.

SELECT
    geo_name,
    geo_level,
    year,
    renters_total,
    cost_burdened_renters,
    ROUND(pct_renters_cost_burdened * 100, 1)  AS pct_burdened,
    ROUND(pct_severely_burdened * 100, 1)      AS pct_severely_burdened,
    ROUND(median_gross_rent, 0)                AS median_rent,
    ROUND(median_household_income, 0)          AS median_income,
    RANK() OVER (
        PARTITION BY year, geo_level
        ORDER BY pct_renters_cost_burdened DESC
    ) AS burden_rank
FROM acs_housing
WHERE renters_total > 1000        -- filter out tiny geographies
ORDER BY year, geo_level, burden_rank;
