
"""Generate basic market statistics in Markdown format."""

from pathlib import Path

import pandas as pd

from lab01_csv_parser import load_market_data

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = PROJECT_ROOT / "data" / "mock_ohlcv.csv"
REPORT_PATH = PROJECT_ROOT / "reports" / "week1_statistics.md"


def generate_report(df: pd.DataFrame) -> str:
    """Calculate OHLCV summary statistics and format them as Markdown."""
    if df.empty:
        raise ValueError("Cannot generate a report from an empty dataset.")

    average_close = df["close"].mean()
    highest_volume_index = df["volume"].idxmax()
    highest_volume_row = df.loc[highest_volume_index]
    lowest_low = df["low"].min()
    total_rows = int(df["close"].count())

    timestamp = highest_volume_row["timestamp"]
    timestamp_text = timestamp.strftime("%Y-%m-%d %H:%M")

    return f"""# Week 1 — Market Statistics

## Dataset
- **Source:** `data/mock_ohlcv.csv`
- **Total records:** {total_rows}

## Results

| Metric | Value |
|---|---:|
| Average close price | {average_close:.2f} |
| Highest trading volume | {highest_volume_row["volume"]:,.0f} |
| Highest-volume timestamp | {timestamp_text} |
| Lowest low price | {lowest_low:.2f} |
| Total records | {total_rows} |

## Notes
This report summarizes synthetic OHLCV data for the AZARS Week 1 exercise.
It is not a trading recommendation.
"""


def main() -> None:
    """Load the dataset and write the Markdown report."""
    df = load_market_data(CSV_PATH)
    report = generate_report(df)

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(report, encoding="utf-8")

    print(f"Report saved to: {REPORT_PATH}")
    print(report)


if __name__ == "__main__":
    main()