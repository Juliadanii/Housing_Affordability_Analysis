-- schema.sql
-- Core tables for the Housing Affordability and Policy Analysis project.
-- (Tables are created automatically by 03_clean_merge.py; this file
-- documents the schema for reference.)

CREATE TABLE IF NOT EXISTS acs_housing (
    geo_name                    TEXT,       -- e.g. "Maryland" or "Baltimore-Columbia-Towson, MD Metro Area"
    geo_level                   TEXT,       -- 'state' or 'metro'
    year                        INTEGER,    -- ACS 5-year vintage
    total_population            INTEGER,
    median_household_income     REAL,
    median_gross_rent           REAL,
    median_home_value           REAL,
    renters_total               INTEGER,
    rent_burden_30_34           INTEGER,
    rent_burden_35_39           INTEGER,
    rent_burden_40_49           INTEGER,
    rent_burden_50_plus         INTEGER,
    occupied_units_total        INTEGER,
    owner_occupied              INTEGER,
    renter_occupied             INTEGER,
    -- Derived fields
    rent_to_income_ratio        REAL,       -- (median rent * 12) / median income
    cost_burdened_renters       INTEGER,    -- renters paying 30%+ of income
    pct_renters_cost_burdened   REAL,
    pct_severely_burdened       REAL,       -- renters paying 50%+
    renter_share                REAL,
    price_to_income_ratio       REAL        -- home value / income
);

CREATE TABLE IF NOT EXISTS hud_fmr (
    state_abbr      TEXT,
    county_name     TEXT,
    metro_name      TEXT,
    fmr_studio      REAL,
    fmr_1br         REAL,
    fmr_2br         REAL,
    fmr_3br         REAL,
    fmr_4br         REAL
);
