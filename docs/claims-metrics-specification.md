Claims Analytics Metrics Specification

Status: Draft v0.1

Purpose

Define reproducible metrics for analyzing a synthetic insurance claims dataset.

Initial metrics

1. Claim frequency: claims divided by the defined exposure measure.
2. Average claim severity: total incurred losses divided by the number of eligible claims.
3. Average processing time: mean elapsed time between defined claim lifecycle events.
4. Reopening rate: reopened claims divided by the defined eligible claim population.
5. Paid-loss total: sum of eligible payments during the specified reporting period.

Required definitions

For each metric, document the numerator, denominator, unit, reporting window, exclusions, missing-data rules, and source fields.

Distinguish paid amounts from incurred losses and distinguish claim counts from exposure-adjusted rates.

Validation

Use synthetic records with hand-calculated expected results. Test empty datasets, missing values, duplicate records, zero denominators, and date boundaries.

Acceptance criteria

- [ ] Every metric has an operational definition.
- [ ] Synthetic test data and expected results are documented.
- [ ] Missing-data and exclusion rules are explicit.
- [ ] Each calculation can be independently reproduced.

Next action

Create the synthetic sample dataset and verify every metric against hand-calculated results.