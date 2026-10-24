
import json
from pathlib import Path

from src.claims_metrics import calculate_metrics

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "reports" / "claims-metrics-report.json"


def generate_report(output_file=DEFAULT_OUTPUT):
    output_file = Path(output_file)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    metrics = calculate_metrics()
    output_file.write_text(
        json.dumps(metrics, indent=2) + "\n",
        encoding="utf-8",
    )
    return metrics


if __name__ == "__main__":
    generate_report()
    print(f"Report written to {DEFAULT_OUTPUT.relative_to(ROOT)}")
