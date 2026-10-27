"""
Claims metrics calculation with validated loading and anomaly detection.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Any

from src.claims_loader import load_claims, flag_anomalies

ROOT = Path(__file__).resolve().parents[1]
CLAIMS_FILE = ROOT / "data" / "synthetic-claims.csv"
EXPOSURE_FILE = ROOT / "data" / "synthetic-exposure.csv"


def _read_exposure() -> float:
    """Simple exposure total (kept separate for now)."""
    import csv
    with EXPOSURE_FILE.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    return sum(float(row["exposure_years"]) for row in rows)


def calculate_metrics(
    severity_threshold: float = 4000.0,
    processing_days_threshold: float = 30.0,
) -> Dict[str, Any]:
    """
    Calculate core claims metrics + anomaly summary.
    Uses the validated loader and rule-based anomaly flagging.
    """
    claims = load_claims(CLAIMS_FILE)
    claims = flag_anomalies(
        claims,
        severity_threshold=severity_threshold,
        processing_days_threshold=processing_days_threshold,
    )

    total_claims = len(claims)
    total_incurred = sum(c.incurred_loss for c in claims)
    total_paid = sum(c.paid_loss for c in claims)
    total_processing_days = sum(c.processing_days for c in claims)
    reopened_claims = sum(1 for c in claims if c.reopened)
    total_exposure = _read_exposure()

    # Anomaly metrics
    anomalous = [c for c in claims if c.is_anomaly]
    anomaly_count = len(anomalous)
    anomaly_incurred = sum(c.incurred_loss for c in anomalous)

    return {
        "claim_count": total_claims,
        "total_exposure_years": total_exposure,
        "claim_frequency_per_policy_year": (
            round(total_claims / total_exposure, 4) if total_exposure > 0 else None
        ),
        "total_incurred_loss": round(total_incurred, 2),
        "total_paid_loss": round(total_paid, 2),
        "average_severity": (
            round(total_incurred / total_claims, 2) if total_claims > 0 else None
        ),
        "average_processing_days": (
            round(total_processing_days / total_claims, 2) if total_claims > 0 else None
        ),
        "reopening_rate": (
            round(reopened_claims / total_claims, 4) if total_claims > 0 else None
        ),
        # New anomaly section
        "anomaly_count": anomaly_count,
        "anomaly_rate": (
            round(anomaly_count / total_claims, 4) if total_claims > 0 else None
        ),
        "anomaly_total_incurred": round(anomaly_incurred, 2),
        "anomaly_share_of_incurred": (
            round(anomaly_incurred / total_incurred, 4) if total_incurred > 0 else None
        ),
    }


if __name__ == "__main__":
    print(json.dumps(calculate_metrics(), indent=2))