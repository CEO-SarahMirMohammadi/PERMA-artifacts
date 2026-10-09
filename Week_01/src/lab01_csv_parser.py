
"""Load and inspect mock OHLCV market data."""

from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = PROJECT_ROOT / "data" / "mock_ohlcv.csv"

REQUIRED_COLUMNS = [
    "timestamp",
    "open",
    "high",
    "low",
    "close",
    "volume",
]


def load_market_data(filepath: str | Path) -> pd.DataFrame:
    """Load a CSV file, validate its schema, and parse timestamps."""
    path = Path(filepath)

    if not path.is_file():
        raise FileNotFoundError(f"CSV file not found: {path}")

    df = pd.read_csv(path)
    missing = set(REQUIRED_COLUMNS) - set(df.columns)

    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="raise")

    for column in ["open", "high", "low", "close", "volume"]:
        df[column] = pd.to_numeric(df[column], errors="raise")

    return df


def main() -> None:
    """Print the first five records and dataset size."""
    df = load_market_data(CSV_PATH)

    print("First five OHLCV records:")
    print(df.head().to_string(index=False))
    print(f"\nTotal rows: {len(df)}")


if __name__ == "__main__":
    main()