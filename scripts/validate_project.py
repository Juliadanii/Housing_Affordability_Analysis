import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def validate_project():
    checks = []
    root = BASE_DIR

    required_files = [
        root / "README.md",
        root / "requirements.txt",
        root / "scripts" / "01_fetch_acs_data.py",
        root / "scripts" / "02_fetch_hud_data.py",
        root / "scripts" / "03_clean_merge.py",
        root / "scripts" / "04_analysis.py",
        root / "sql" / "cost_burden_analysis.sql",
        root / "sql" / "rent_to_income.sql",
        root / "sql" / "demographic_trends.sql",
    ]

    for path in required_files:
        checks.append((path.name, path.exists()))

    processed_dir = root / "data" / "processed"
    expected_outputs = [
        processed_dir / "acs_housing_clean.csv",
        processed_dir / "tableau_cost_burden.csv",
        processed_dir / "tableau_rent_to_income.csv",
        processed_dir / "tableau_demographics.csv",
    ]

    for path in expected_outputs:
        checks.append((path.name, path.exists()))

    summary = {
        "files_present": sum(1 for _, exists in checks if exists),
        "files_checked": len(checks),
        "ready_for_tableau": all(exists for _, exists in checks if _ in {p.name for p in expected_outputs}),
    }

    return {"ok": True, "checks": checks, "summary": summary}


if __name__ == "__main__":
    result = validate_project()
    print("Project validation")
    for name, exists in result["checks"]:
        status = "OK" if exists else "MISSING"
        print(f"- {name}: {status}")
    print(f"Summary: {result['summary']}")
