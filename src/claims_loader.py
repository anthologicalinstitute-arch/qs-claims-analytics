
"""Validated loading and rule-based anomaly detection for synthetic claims data."""

from __future__ import annotations

import csv
import math
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Iterable


REQUIRED_COLUMNS = {
    "claim_id",
    "policy_id",
    "exposure_years",
    "incurred_loss",
    "paid_loss",
    "processing_days",
    "reopened",
}


@dataclass(frozen=True)
class Claim:
    claim_id: str
    policy_id: str
    exposure_years: float
    incurred_loss: float
    paid_loss: float
    processing_days: float
    reopened: bool
    is_anomaly: bool = False
    anomaly_reasons: tuple[str, ...] = ()


def _number(value: str, field: str, row_number: int) -> float:
    """Parse a finite numeric value or raise a descriptive validation error."""
    if value is None or not value.strip():
        raise ValueError(
            f"Row {row_number}: missing required value for '{field}'."
        )

    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(
            f"Row {row_number}: '{field}' must be numeric; got {value!r}."
        ) from exc

    if not math.isfinite(number):
        raise ValueError(
            f"Row {row_number}: '{field}' must be finite."
        )

    return number


def _boolean(value: str, field: str, row_number: int) -> bool:
    """Accept explicit true/false values only."""
    normalized = (value or "").strip().lower()

    if normalized == "true":
        return True
    if normalized == "false":
        return False

    raise ValueError(
        f"Row {row_number}: '{field}' must be true or false; got {value!r}."
    )


def load_claims(file_path: str | Path) -> list[Claim]:
    """Load claims from CSV and reject missing, duplicate, or invalid records."""
    path = Path(file_path)

    if not path.is_file():
        raise FileNotFoundError(f"Claims file not found: {path}")

    claims: list[Claim] = []
    seen_ids: set[str] = set()

    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)

        if not reader.fieldnames:
            raise ValueError("Claims CSV is empty or has no header.")

        headers = {
            header.strip() for header in reader.fieldnames if header
        }
        missing_columns = REQUIRED_COLUMNS - headers

        if missing_columns:
            raise ValueError(
                "Claims CSV is missing required columns: "
                + ", ".join(sorted(missing_columns))
            )

        for row_number, row in enumerate(reader, start=2):
            # Normalize header whitespace without silently filling missing data.
            row = {
                key.strip(): value
                for key, value in row.items()
                if key is not None
            }

            claim_id = (row.get("claim_id") or "").strip()
            policy_id = (row.get("policy_id") or "").strip()

            if not claim_id:
                raise ValueError(
                    f"Row {row_number}: missing required 'claim_id'."
                )
            if claim_id in seen_ids:
                raise ValueError(
                    f"Row {row_number}: duplicate claim_id {claim_id!r}."
                )
            if not policy_id:
                raise ValueError(
                    f"Row {row_number}: missing required 'policy_id'."
                )

            exposure_years = _number(
                row.get("exposure_years"), "exposure_years", row_number
            )
            incurred_loss = _number(
                row.get("incurred_loss"), "incurred_loss", row_number
            )
            paid_loss = _number(
                row.get("paid_loss"), "paid_loss", row_number
            )
            processing_days = _number(
                row.get("processing_days"), "processing_days", row_number
            )
            reopened = _boolean(
                row.get("reopened"), "reopened", row_number
            )

            if exposure_years <= 0:
                raise ValueError(
                    f"Row {row_number}: exposure_years must be greater than zero."
                )
            if incurred_loss < 0 or paid_loss < 0:
                raise ValueError(
                    f"Row {row_number}: loss amounts must be nonnegative."
                )
            if processing_days < 0:
                raise ValueError(
                    f"Row {row_number}: processing_days must be nonnegative."
                )

            claims.append(
                Claim(
                    claim_id=claim_id,
                    policy_id=policy_id,
                    exposure_years=exposure_years,
                    incurred_loss=incurred_loss,
                    paid_loss=paid_loss,
                    processing_days=processing_days,
                    reopened=reopened,
                )
            )
            seen_ids.add(claim_id)

    if not claims:
        raise ValueError("Claims CSV contains no data records.")

    return claims


def flag_anomalies(
    claims: Iterable[Claim],
    severity_threshold: float = 4000.0,
    processing_days_threshold: float = 30.0,
) -> list[Claim]:
    """Return claims with transparent, rule-based anomaly flags.

    A claim is flagged for high incurred severity, long processing duration,
    or a reopened status. These are screening rules, not proof of an error.
    """
    for name, threshold in (
        ("severity_threshold", severity_threshold),
        ("processing_days_threshold", processing_days_threshold),
    ):
        if not math.isfinite(threshold) or threshold < 0:
            raise ValueError(f"{name} must be finite and nonnegative.")

    flagged: list[Claim] = []

    for claim in claims:
        reasons: list[str] = []

        if claim.incurred_loss >= severity_threshold:
            reasons.append("high_incurred_severity")

        if claim.processing_days >= processing_days_threshold:
            reasons.append("long_processing_duration")

        if claim.reopened:
            reasons.append("reopened_claim")

        flagged.append(
            replace(
                claim,
                is_anomaly=bool(reasons),
                anomaly_reasons=tuple(reasons),
            )
        )

    return flagged
