
    def test_claim_frequency(self):
        exposure_file = (
            Path(__file__).resolve().parents[1]
            / "data"
            / "synthetic-exposure.csv"
        )

        with exposure_file.open(
            newline="", encoding="utf-8"
        ) as file:
            exposure_rows = list(csv.DictReader(file))

        total_exposure = sum(
            float(row["exposure_years"])
            for row in exposure_rows
        )
        total_claims = sum(
            int(row["claim_count"])
            for row in exposure_rows
        )

        self.assertAlmostEqual(total_exposure, 20.0)
        self.assertEqual(total_claims, 10)
        self.assertAlmostEqual(
            total_claims / total_exposure, 0.5
        )
