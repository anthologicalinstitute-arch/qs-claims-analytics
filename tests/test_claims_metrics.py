
import csv
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.claims_metrics import calculate_metrics
ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "synthetic-claims.csv"
EXPOSURE_FILE = ROOT / "data" / "synthetic-exposure.csv"


def read_csv(path):
    with path.open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


class ClaimsMetricsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.claims = read_csv(DATA_FILE)

    def test_claim_count(self):
        self.assertEqual(len(self.claims), 10)

    def test_unique_claim_ids(self):
        ids = [row["claim_id"] for row in self.claims]
        self.assertEqual(len(ids), len(set(ids)))

    def test_incurred_losses(self):
        total = sum(
            float(row["incurred_loss"]) for row in self.claims
        )
        self.assertAlmostEqual(total, 22000.0)

    def test_average_severity(self):
        losses = [
            float(row["incurred_loss"]) for row in self.claims
        ]
        self.assertAlmostEqual(sum(losses) / len(losses), 2200.0)

    def test_paid_losses(self):
        total = sum(
            float(row["paid_loss"]) for row in self.claims
        )
        self.assertAlmostEqual(total, 16200.0)

    def test_average_processing_days(self):
        days = [
            float(row["processing_days"]) for row in self.claims
        ]
        self.assertAlmostEqual(sum(days) / len(days), 19.5)

    def test_reopening_rate(self):
        reopened = sum(
            row["reopened"].lower() == "true"
            for row in self.claims
        )
        self.assertAlmostEqual(reopened / len(self.claims), 0.30)

    def test_claim_frequency(self):
        exposure_rows = read_csv(EXPOSURE_FILE)

        total_exposure = sum(
            float(row["exposure_years"]) for row in exposure_rows
        )
        total_claims = sum(
            int(row["claim_count"]) for row in exposure_rows
        )

        self.assertAlmostEqual(total_exposure, 20.0)
        self.assertEqual(total_claims, 10)
        self.assertAlmostEqual(total_claims / total_exposure, 0.5)


    def test_claims_reference_known_policies(self):
        exposure_rows = read_csv(EXPOSURE_FILE)
        policy_ids = {row["policy_id"] for row in exposure_rows}

        claim_policy_ids = {
            row["policy_id"] for row in self.claims
        }

        self.assertTrue(claim_policy_ids.issubset(policy_ids))

    def test_policy_claim_counts_reconcile(self):
        exposure_rows = read_csv(EXPOSURE_FILE)

        actual_counts = {}
        for row in self.claims:
            policy_id = row["policy_id"]
            actual_counts[policy_id] = (
                actual_counts.get(policy_id, 0) + 1
            )

        for row in exposure_rows:
            policy_id = row["policy_id"]
            expected = int(row["claim_count"])
            actual = actual_counts.get(policy_id, 0)
            self.assertEqual(
                actual, expected,
                f"Claim count mismatch for {policy_id}"
            )

    def test_required_claim_fields_are_present(self):
        required_fields = {
            "claim_id",
            "policy_id",
            "incurred_loss",
            "paid_loss",
            "processing_days",
            "reopened",
        }

        for index, row in enumerate(self.claims, start=1):
            for field in required_fields:
                self.assertTrue(
                    row.get(field, "").strip(),
                    f"Missing {field} in claim row {index}"
                )

    def test_loss_values_are_nonnegative(self):
        for row in self.claims:
            with self.subTest(claim_id=row["claim_id"]):
                incurred = float(row["incurred_loss"])
                paid = float(row["paid_loss"])

                self.assertGreaterEqual(incurred, 0)
                self.assertGreaterEqual(paid, 0)
                self.assertLessEqual(
                    paid, incurred,
                    "Paid loss exceeds incurred loss"
                )

    def test_processing_days_are_nonnegative(self):
        for row in self.claims:
            with self.subTest(claim_id=row["claim_id"]):
                self.assertGreaterEqual(
                    float(row["processing_days"]), 0
                )

    def test_reopened_values_are_valid(self):
        allowed_values = {"true", "false"}

        for row in self.claims:
            with self.subTest(claim_id=row["claim_id"]):
                self.assertIn(
                    row["reopened"].strip().lower(),
                    allowed_values
                )

    def test_exposure_policy_ids_are_unique(self):
        exposure_rows = read_csv(EXPOSURE_FILE)
        policy_ids = [row["policy_id"] for row in exposure_rows]

        self.assertEqual(
            len(policy_ids), len(set(policy_ids)),
            "Duplicate policy IDs in exposure dataset"
        )

    def test_calculated_metrics_report(self):
        metrics = calculate_metrics()

        self.assertEqual(metrics["claim_count"], 10)
        self.assertAlmostEqual(
            metrics["total_exposure_years"], 20.0
        )
        self.assertAlmostEqual(
            metrics["claim_frequency_per_policy_year"], 0.5
        )
        self.assertAlmostEqual(
            metrics["total_incurred_loss"], 22000.0
        )
        self.assertAlmostEqual(
            metrics["total_paid_loss"], 16200.0
        )
        self.assertAlmostEqual(
            metrics["average_severity"], 2200.0
        )
        self.assertAlmostEqual(
            metrics["average_processing_days"], 19.5
        )
        self.assertAlmostEqual(
            metrics["reopening_rate"], 0.30
        )

if __name__ == "__main__":
    unittest.main()
