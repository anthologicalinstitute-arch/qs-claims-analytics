Claims Metrics Validation Report

Status: Initial validation — synthetic data
Version: 0.1

1. Purpose

Document independently calculated expected results for the synthetic claims dataset. These results provide a reference for future automated tests.

2. Dataset

- Source: "data/synthetic-claims.csv"
- Records: 10 synthetic claims
- Currency: Assumed to be USD
- Processing time: Days
- Reopened claims: 3
- Data status: Illustrative only; not real insurance data

3. Expected Results

Metric| Calculation| Expected result
Claim count| Number of claim records| 10
Total incurred losses| Sum of incurred_loss| $22,000
Average claim severity| $22,000 / 10 claims| $2,200
Total paid losses| Sum of paid_loss| $16,200
Average processing time| 195 days / 10 claims| 19.5 days
Reopening rate| 3 reopened / 10 claims| 30%

4. Validation Rules

1. Count each unique claim ID once.
2. Calculate average severity using eligible claims with valid incurred-loss values.
3. Calculate paid-loss totals independently of incurred losses.
4. Calculate processing time using valid processing-day values.
5. Calculate reopening rate using eligible claims with known reopening status.
6. Do not silently replace missing values with zero.
7. Flag duplicate claim IDs, negative amounts, invalid durations, and missing required fields.
8. Protect against division by zero when calculating rates.

5. Claim Frequency Limitation

The dataset contains an "exposure_years" field, but claim-level records alone do not establish total insured exposure, including policies with no claims.

Therefore, do not treat a frequency calculated from these ten rows as a validated actuarial claim frequency. A separate exposure dataset, including exposure with zero claims, is required.

The intended frequency formula is:

"Claim frequency = Eligible claim count / Total eligible exposure"

The exposure unit and reporting period must be defined before the metric is approved.

6. Acceptance Criteria

- [ ] All six reported count, loss, severity, time, and reopening results reproduce from the CSV.
- [ ] Calculations and denominators are documented.
- [ ] Invalid and missing data have explicit handling rules.
- [ ] Claim frequency remains marked provisional until exposure data are available.
- [ ] Automated tests agree with the hand-calculated results.

7. Next Action

Create automated tests that read the synthetic CSV, calculate the expected metrics, and flag discrepancies. Then create a separate synthetic exposure dataset to validate claim frequency properly.