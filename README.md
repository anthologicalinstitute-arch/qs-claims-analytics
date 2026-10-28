# qs-claims-analytics

Python supports statistical claims analysis, cost modeling and anomaly detection; SQL supports structured claims datasets.

## Current Capabilities

- Validated claims data loader with schema and business-rule checks
- Rule-based anomaly detection (high severity, long processing time, high-value reopenings)
- Core claims metrics: frequency, severity, processing time, reopening rate
- Anomaly impact metrics: count, rate, total incurred, share of total loss 
- JSON report generation

## Quick Start

```bash
# Calculate metrics (including anomalies)
python -m src.claims_metrics

# Generate report
python scripts/generate_claims_report.pyValidation Status
Status
Partially Validated

Validation Scope
The following components have been reviewed:

Claims data schema validation
Business-rule validation
Core metric calculations
JSON report generation workflow
Not Yet Validated
The following areas have not yet been fully validated:

Real-world production deployment performance
Cross-industry datasets
Large-scale production workloads
External independent review
Review Information
Last Review: 2026-10-28

Research Reviewer: Kurt Celvin, AAMMR™
