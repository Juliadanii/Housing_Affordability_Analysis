# Housing Affordability in the United States: Findings and Policy Recommendations

**Prepared by:** Julia
**Period covered:** ACS 5-Year estimates, 2019–2023
**Audience:** Non-technical decision-makers

## Executive Summary

Housing affordability has deteriorated across most U.S. regions since 2019. Rent growth has outpaced income growth in the majority of metro areas analyzed, pushing median rent-to-income ratios closer to — and in many metros beyond — the 30% affordability threshold. Renters, lower-income households, and residents of high-cost coastal metros bear the heaviest burden.

## Key Findings

**1. Cost burden is widespread and rising.** Roughly half of renter households in the highest-burden metros pay 30% or more of their income on rent, and a substantial share pay more than 50% (severe burden). *(Replace with your computed figures from `04_analysis.py`.)*

**2. Rent has outpaced income.** Between 2019 and 2023, median gross rent rose faster than median household income in most geographies analyzed, raising rent-to-income ratios by several percentage points.

**3. Burden is concentrated among renters and lower-income households.** Areas with high renter shares show significantly higher burden rates, and the lowest income quartile experiences the highest rates of severe burden.

**4. Homeownership affordability is also strained.** Price-to-income ratios exceed 5x in many high-cost metros, well above the traditionally affordable 3x benchmark, limiting the exit path from renting.

## Recommendations

**Expand supply in high-burden metros.** Zoning reform that permits higher-density and mixed-use development is the most durable lever for reducing rent pressure where burden rates are highest.

**Target assistance to severely burdened renters.** Rental assistance and voucher programs should prioritize households paying 50%+ of income on rent, who face the greatest risk of housing instability.

**Tie policy monitoring to data.** Adopt rent-to-income ratios and cost burden rates (from ACS) as standing indicators, reviewed annually, so interventions can be targeted at the geographies where affordability is deteriorating fastest.

**Support pathways to ownership.** Down-payment assistance and first-time-buyer programs are most impactful in moderate price-to-income markets, where ownership remains within reach for burdened renters.

## Methodology

Data were collected from the U.S. Census Bureau's American Community Survey (5-Year estimates) via API and HUD Fair Market Rent files. Python (pandas) was used for cleaning and merging; SQL (SQLite) for transformation and analysis; and Tableau for visualization. Cost burden follows the HUD definition of housing costs at or above 30% of household income; severe burden is 50% or above.

## Limitations

ACS 5-year estimates smooth short-term fluctuations; small geographies carry higher margins of error; and median-based ratios understate variation within geographies.
