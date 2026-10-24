
import json
import tempfile
import unittest
from pathlib import Path

from scripts.generate_claims_report import generate_report


class ClaimsReportTests(unittest.TestCase):
    def test_report_generator_writes_valid_json(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "claims-metrics-report.json"
            metrics = generate_report(output)

            self.assertTrue(output.exists())
            report = json.loads(
                output.read_text(encoding="utf-8")
            )

            self.assertEqual(report["claim_count"], 10)
            self.assertAlmostEqual(
                report["total_incurred_loss"], 22000.0
            )
            self.assertAlmostEqual(
                report["total_paid_loss"], 16200.0
            )
            self.assertAlmostEqual(
                report["claim_frequency_per_policy_year"], 0.5
            )
            self.assertEqual(report, metrics)


if __name__ == "__main__":
    unittest.main()
