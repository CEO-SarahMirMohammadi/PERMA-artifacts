
"""Reusable loader for OHLCV market data."""

from pathlib import Path
from typing import Any

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = PROJECT_ROOT / "data" / "mock_ohlcv.csv"
REPORT_PATH = PROJECT_ROOT / "reports" / "week1_loader_summary.md"

REQUIRED_COLUMNS = [
    "timestamp",
    "open",
    "high",
    "low",
    "close",
    "volume",
]


class MarketDataLoader:
    """Load, summarize, and export OHLCV market data."""

    def __init__(self) -> None:
        """Initialize the loader with no dataset."""
        self.df: pd.DataFrame | None = None

    def load(self, filepath: str | Path) -> pd.DataFrame:
        """Read and validate a CSV dataset."""
        path = Path(filepath)

        if not path.is_file():
            raise FileNotFoundError(f"CSV file not found: {path}")

        df = pd.read_csv(path)
        missing = set(REQUIRED_COLUMNS) - set(df.columns)

        if missing:
            raise ValueError(f"Missing required columns: {sorted(missing)}")

        if df.empty:
            raise ValueError("The CSV contains no data rows.")

        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="raise")

        for column in ["open", "high", "low", "close", "volume"]:
            df[column] = pd.to_numeric(df[column], errors="raise")

        self.df = df
        return df

    def summary(self) -> dict[str, Any]:
        """Return basic statistics for the loaded dataset."""
        if self.df is None:
            raise RuntimeError("Call load() before summary().")

        df = self.df
        highest_volume_index = df["volume"].idxmax()
        highest_volume_row = df.loc[highest_volume_index]

        return {
            "total_rows": int(len(df)),
            "average_close": float(df["close"].mean()),
            "highest_volume": float(highest_volume_row["volume"]),
            "highest_volume_timestamp": str(
                highest_volume_row["timestamp"]
            ),
            "lowest_low": float(df["low"].min()),
        }

    def export(self, report_path: str | Path) -> Path:
        """Export the dataset summary to a Markdown file."""
        stats = self.summary()
        output_path = Path(report_path)

        report = f"""# Week 1 — Loader Summary

| Metric | Value |
|---|---:|
| Total rows | {stats["total_rows"]} |
| Average close | {stats["average_close"]:.2f} |
| Highest volume | {stats["highest_volume"]:,.0f} |
| Highest-volume timestamp | {stats["highest_volume_timestamp"]} |
| Lowest low | {stats["lowest_low"]:.2f} |
"""

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(report, encoding="utf-8")
        return output_path


def main() -> None:
    """Run the loader and print its summary."""
    loader = MarketDataLoader()

    try:
        loader.load(CSV_PATH)

        for metric, value in loader.summary().items():
            print(f"{metric}: {value}")

        saved_path = loader.export(REPORT_PATH)
        print(f"\nReport saved to: {saved_path}")

    except (FileNotFoundError, ValueError, RuntimeError) as error:
        print(f"Data loading failed: {error}")
        raise SystemExit(1) from error


if __name__ == "__main__":
    main()