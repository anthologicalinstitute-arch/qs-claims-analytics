
import csv
import unittest
from pathlib import Path

DATA_FILE = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "synthetic-claims.csv"
)


def load_claims():
    with DATA_FILE.open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


class ClaimsMetricsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.claims = load_claims()

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
            float(row["incurred_loss"])
            for row in self.claims
        ]
        self.assertAlmostEqual(sum(losses) / len(losses), 2200.0)

    def test_paid_losses(self):
        total = sum(
            float(row["paid_loss"]) for row in self.claims
        )
        self.assertAlmostEqual(total, 16200.0)

    def test_average_processing_days(self):
        days = [
            float(row["processing_days"])
            for row in self.claims
        ]
        self.assertAlmostEqual(sum(days) / len(days), 19.5)

    def test_reopening_rate(self):
        reopened = sum(
            row["reopened"].lower() == "true"
            for row in self.claims
        )
        self.assertAlmostEqual(reopened / len(self.claims), 0.30)


if __name__ == "__main__":
    unittest.main()
