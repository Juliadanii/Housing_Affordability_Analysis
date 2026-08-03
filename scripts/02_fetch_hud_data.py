
import os
import sys
import time
import requests
import pandas as pd
 
BASE_URL = "https://www.huduser.gov/hudapi/public/fmr"
FMR_YEAR = os.environ.get("HUD_FMR_YEAR", "2024")
TOKEN = os.environ.get("HUD_API_TOKEN")
 
RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
FALLBACK_IN_PATH = os.path.join(RAW_DIR, "hud_fmr.csv")
OUT_PATH = os.path.join(RAW_DIR, "hud_fmr_clean.csv")
 
STD_COLUMNS = ["state_abbr", "county_fips", "county_name", "metro_name",
               "fmr_studio", "fmr_1br", "fmr_2br", "fmr_3br", "fmr_4br"]
 
 
def _headers():
    return {"Authorization": f"Bearer {TOKEN}"}
 
 
def _get(path):
    """GET a HUD API path with basic error handling."""
    url = f"{BASE_URL}/{path}"
    resp = requests.get(url, headers=_headers(), timeout=30)
    if resp.status_code == 401:
        sys.exit("HUD API returned 401 Unauthorized. Check that HUD_API_TOKEN "
                 "is set correctly and that your token is active.")
    resp.raise_for_status()
    return resp.json()
 
 
def list_states():
    """Return list of two-letter state codes (skips territories)."""
    payload = _get("listStates")
    # HUD currently returns a list here, although some API responses wrap
    # records in a ``data`` field. Support both response shapes.
    rows = payload if isinstance(payload, list) else payload.get("data", [])
    skip = {"AS", "GU", "MP", "PR", "VI", "UM"}  # drop territories; ACS side is 50+DC
    return [r["state_code"] for r in rows if r.get("state_code") not in skip]
 
 
def _norm_county(rec):
    """Normalize one county record (case-insensitive keys) to std columns."""
    low = {str(k).lower(): v for k, v in rec.items()}
    fips_raw = str(low.get("fips_code") or low.get("fips") or "")
    # HUD county FIPS is often SSCCC99999; first 5 chars = standard county FIPS
    county_fips = fips_raw[:5] if len(fips_raw) >= 5 else fips_raw
    return {
        "state_abbr":  low.get("state_code") or low.get("state_alpha"),
        "county_fips": county_fips,
        "county_name": low.get("county_name") or low.get("countyname"),
        "metro_name":  low.get("metro_name"),
        "fmr_studio":  low.get("studio") or low.get("efficiency"),
        "fmr_1br":     low.get("one-bedroom"),
        "fmr_2br":     low.get("two-bedroom"),
        "fmr_3br":     low.get("three-bedroom"),
        "fmr_4br":     low.get("four-bedroom"),
    }
 
 
def fetch_from_api():
    states = list_states()
    print(f"Fetching FY{FMR_YEAR} county FMRs for {len(states)} states...")
 
    all_rows = []
    for i, st in enumerate(states, 1):
        try:
            payload = _get(f"statedata/{st}?year={FMR_YEAR}")
        except requests.HTTPError as e:
            print(f"  [{st}] skipped ({e})")
            continue
 
        counties = payload.get("data", {}).get("counties", [])
        for rec in counties:
            all_rows.append(_norm_county(rec))
 
        print(f"  [{i}/{len(states)}] {st}: {len(counties)} counties")
        time.sleep(0.3)  # be polite to the API
 
    df = pd.DataFrame(all_rows, columns=STD_COLUMNS).drop_duplicates()
    return df
 
 
def fetch_from_local_csv():
    print("HUD_API_TOKEN not set; falling back to local CSV.")
    if not os.path.exists(FALLBACK_IN_PATH):
        sys.exit(f"No token and no file at {FALLBACK_IN_PATH}. Either set "
                 "HUD_API_TOKEN or download the county FMR CSV to that path.")
    df = pd.read_csv(FALLBACK_IN_PATH)
    df.columns = [c.strip().lower() for c in df.columns]
    return df
 
 
def main():
    os.makedirs(RAW_DIR, exist_ok=True)
    df = fetch_from_api() if TOKEN else fetch_from_local_csv()
 
    # coerce rent columns to numeric where present
    for c in ["fmr_studio", "fmr_1br", "fmr_2br", "fmr_3br", "fmr_4br"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
 
    df.to_csv(OUT_PATH, index=False)
    print(f"Saved {len(df):,} rows -> {OUT_PATH}")
 
 
if __name__ == "__main__":
    main()
