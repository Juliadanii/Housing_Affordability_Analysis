-- demographic_trends.sql
-- Tenure and demographic patterns: renter share, population, and how
-- affordability pressure correlates with renter concentration.

SELECT
    geo_name,
    geo_level,
    year,
    total_population,
    ROUND(renter_share * 100, 1)               AS pct_renter_households,
    ROUND(pct_renters_cost_burdened * 100, 1)  AS pct_renters_burdened,
    ROUND(price_to_income_ratio, 2)            AS home_price_to_income,
    CASE
        WHEN renter_share >= 0.45 THEN 'High renter share'
        WHEN renter_share >= 0.30 THEN 'Moderate renter share'
        ELSE 'Low renter share'
    END AS renter_segment,
    NTILE(4) OVER (
        PARTITION BY year, geo_level
        ORDER BY median_household_income
    ) AS income_quartile
FROM acs_housing
WHERE total_population IS NOT NULL
ORDER BY year, geo_level, pct_renters_burdened DESC;
