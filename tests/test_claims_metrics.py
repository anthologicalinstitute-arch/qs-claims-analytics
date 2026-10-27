import unittest
from src.claims_metrics import calculate_metrics


class ClaimsMetricsWithAnomaliesTests(unittest.TestCase):
    def test_metrics_include_anomaly_fields(self):
        metrics = calculate_metrics()
        self.assertIn("anomaly_count", metrics)
        self.assertIn("anomaly_rate", metrics)
        self.assertIn("anomaly_total_incurred", metrics)
        self.assertIn("anomaly_share_of_incurred", metrics)

    def test_anomaly_count_is_positive(self):
        metrics = calculate_metrics(severity_threshold=4000.0)
        # CL007 (5000) should be flagged
        self.assertGreaterEqual(metrics["anomaly_count"], 1)

    def test_core_metrics_still_present(self):
        metrics = calculate_metrics()
        self.assertEqual(metrics["claim_count"], 10)
        self.assertAlmostEqual(metrics["total_incurred_loss"], 22000.0)