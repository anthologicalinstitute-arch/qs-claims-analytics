Data Reconciliation Rules

Status: Draft v0.1
Project: Quantum Sims™ — Claims Analytics
Purpose: Define checks for consistency between synthetic claims records and synthetic policy exposure records.

1. Source Files

- Claims: "data/synthetic-claims.csv"
- Exposure: "data/synthetic-exposure.csv"

Both files are synthetic test data. They must not be represented as actual insurance experience.

2. Required Reconciliation Rules

2.1 Claims integrity

- Every "claim_id" must be present and unique.
- Every claim must have valid incurred loss, paid loss, processing duration, and reopening status.
- Loss amounts must be nonnegative.
- Processing durations must be nonnegative.
- Missing or invalid values must be reported, not silently converted to zero.

2.2 Exposure integrity

- Every "policy_id" must be present and unique.
- "exposure_years" must be numeric and greater than zero for records included in frequency calculations.
- "claim_count" must be a nonnegative integer.
- Every exposure record must use the same defined reporting period and exposure unit.

2.3 Cross-file reconciliation

The current files do not contain a shared policy identifier in the claims dataset. Therefore, claim-level linkage to individual policies cannot yet be verified.

Until a shared key is introduced:

- Compare aggregate claim counts only as a provisional check.
- Do not claim that individual claims have been reconciled to policies.
- Do not use aggregate agreement as proof that the datasets represent the same underlying records.

2.4 Frequency calculation

Calculate frequency only after validating the eligible exposure records and confirming that the claim count is consistent with the defined population and reporting period.

"Claim frequency = Eligible claims / Total eligible exposure in policy-years"

For the current illustrative data:

- Expected claims: 10
- Expected exposure: 20 policy-years
- Expected frequency: 0.5 claims per policy-year

These values are test expectations, not real-world risk estimates.

3. Failure Conditions

The validation process must flag:

- Duplicate or missing identifiers
- Invalid numeric values
- Negative losses or processing durations
- Zero or negative total exposure
- Negative or non-integer claim counts
- Inconsistent reporting periods
- Unresolved claims-to-policy linkage

4. Acceptance Criteria

- [ ] Claims and exposure files pass their respective integrity checks.
- [ ] Invalid records produce clear validation failures.
- [ ] Frequency is not calculated when the denominator is invalid.
- [ ] The missing cross-file linkage is documented.
- [ ] Test results can be reproduced using the committed synthetic files.

5. Next Development Step

Add a shared "policy_id" to the claims dataset and implement automated tests for record integrity, claim-count reconciliation, and valid exposure calculations. Keep the dataset synthetic and document any assumptions used to construct the linkage.