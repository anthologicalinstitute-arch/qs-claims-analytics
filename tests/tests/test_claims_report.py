
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "generate_claims_report.py"
OUTPUT = ROOT / "reports" / "claims-metrics-report.json"


class ClaimsReportTests(unittest.TestCase):
    def test_report_generator_writes_valid_json(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(
            result.returncode, 0,
            msg=result.stdout + result.stderr,
        )
        self.assertTrue(OUTPUT.exists())

        report = json.loads(OUTPUT.read_text(encoding="utf-8"))

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


if __name__ == "__main__":
    unittest.main()
