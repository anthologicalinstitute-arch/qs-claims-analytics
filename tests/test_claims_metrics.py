
import csv
import unittest
from pathlib import Path

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

if __name__ == "__main__":
    unittest.main()
