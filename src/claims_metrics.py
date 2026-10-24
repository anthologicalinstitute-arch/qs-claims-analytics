
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLAIMS_FILE = ROOT / "data" / "synthetic-claims.csv"
EXPOSURE_FILE = ROOT / "data" / "synthetic-exposure.csv"


def read_csv(path):
    with path.open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def calculate_metrics():
    claims = read_csv(CLAIMS_FILE)
    exposures = read_csv(EXPOSURE_FILE)

    total_claims = len(claims)
    total_incurred = sum(
        float(row["incurred_loss"]) for row in claims
    )
    total_paid = sum(
        float(row["paid_loss"]) for row in claims
    )
    total_processing_days = sum(
        float(row["processing_days"]) for row in claims
    )
    reopened_claims = sum(
        row["reopened"].strip().lower() == "true"
        for row in claims
    )
    total_exposure = sum(
        float(row["exposure_years"]) for row in exposures
    )

    return {
        "claim_count": total_claims,
        "total_exposure_years": total_exposure,
        "claim_frequency_per_policy_year": (
            total_claims / total_exposure
            if total_exposure > 0 else None
        ),
        "total_incurred_loss": round(total_incurred, 2),
        "total_paid_loss": round(total_paid, 2),
        "average_severity": (
            round(total_incurred / total_claims, 2)
            if total_claims > 0 else None
        ),
        "average_processing_days": (
            round(total_processing_days / total_claims, 2)
            if total_claims > 0 else None
        ),
        "reopening_rate": (
            round(reopened_claims / total_claims, 4)
            if total_claims > 0 else None
        ),
    }


if __name__ == "__main__":
    print(json.dumps(calculate_metrics(), indent=2))
