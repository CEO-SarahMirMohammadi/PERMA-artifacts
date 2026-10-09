
"""Feature engineering pipeline for AZARS market data."""

from pathlib import Path
from typing import Any

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA_PATH = PROJECT_ROOT / "data" / "mock_ohlcv.csv"
DEFAULT_REPORT_PATH = PROJECT_ROOT / "reports" / "feature_summary.md"

REQUIRED_COLUMNS = {
    "timestamp",
    "open",
    "high",
    "low",
    "close",
    "volume",
}


class MarketDataLoader:
    """Load OHLCV data and create trading-related features."""

    def __init__(self) -> None:
        """Initialize an empty market-data loader."""
        self.df: pd.DataFrame | None = None

    def load(self, filepath: str | Path) -> pd.DataFrame:
        """Load and validate an OHLCV CSV file."""
        path = Path(filepath)

        if not path.is_file():
            raise FileNotFoundError(f"Market data file not found: {path}")

        df = pd.read_csv(path)

        missing = REQUIRED_COLUMNS - set(df.columns)
        if missing:
            raise ValueError(
                f"Missing required columns: {sorted(missing)}"
            )

        if df.empty:
            raise ValueError("The input dataset is empty.")

        df["timestamp"] = pd.to_datetime(
            df["timestamp"], errors="raise"
        )

        numeric_columns = [
            "open", "high", "low", "close", "volume"
        ]
        for column in numeric_columns:
            df[column] = pd.to_numeric(df[column], errors="raise")

        if df[numeric_columns].isna().any().any():
            raise ValueError("OHLCV numeric columns contain missing values.")

        df = df.sort_values("timestamp").reset_index(drop=True)
        self.df = df
        return df

    def _require_data(self) -> pd.DataFrame:
        """Return loaded data or raise an informative error."""
        if self.df is None:
            raise RuntimeError("Call load() before creating features.")
        return self.df

    def add_sma(self, window: int = 7) -> pd.DataFrame:
        """Add a rolling simple moving average of closing prices."""
        if window < 1:
            raise ValueError("window must be at least 1.")

        df = self._require_data()
        df[f"sma_{window}"] = (
            df["close"].rolling(window=window, min_periods=window).mean()
        )
        return df

    def add_returns_lag(self, n: int = 1) -> pd.DataFrame:
        """Add the close-to-close return from n periods earlier."""
        if n < 1:
            raise ValueError("n must be at least 1.")

        df = self._require_data()
        period_returns = df["close"].pct_change(fill_method=None)
        df[f"returns_lag_{n}"] = period_returns.shift(n)
        return df

    def add_volatility(self, window: int = 7) -> pd.DataFrame:
        """Add rolling standard deviation of close-to-close returns."""
        if window < 2:
            raise ValueError("Volatility window must be at least 2.")

        df = self._require_data()
        period_returns = df["close"].pct_change(fill_method=None)
        df[f"volatility_{window}d"] = (
            period_returns.rolling(
                window=window, min_periods=window
            ).std()
        )
        return df

    def build_feature_matrix(self) -> pd.DataFrame:
        """Create required features and remove rows with missing values."""
        self._require_data()

        self.add_sma(window=7)
        self.add_returns_lag(n=1)
        self.add_volatility(window=7)

        df = self._require_data()
        feature_columns = [
            "sma_7",
            "returns_lag_1",
            "volatility_7d",
        ]

        # Drop warm-up rows caused by rolling windows and lagging.
        df = df.dropna(subset=feature_columns).reset_index(drop=True)

        if df[feature_columns].isna().any().any():
            raise ValueError("Feature matrix still contains NaN values.")

        self.df = df
        return df

    def summary(self) -> dict[str, Any]:
        """Summarize the generated feature matrix."""
        df = self._require_data()
        feature_columns = [
            "sma_7",
            "returns_lag_1",
            "volatility_7d",
        ]

        return {
            "rows": int(len(df)),
            "feature_columns": feature_columns,
            "nan_count": int(df[feature_columns].isna().sum().sum()),
            "average_close": float(df["close"].mean()),
        }

    def export(self, report_path: str | Path) -> Path:
        """Export feature-pipeline results as a Markdown report."""
        df = self._require_data()
        stats = self.summary()
        output_path = Path(report_path)

        feature_columns = stats["feature_columns"]
        preview = df[
            ["timestamp", "close", *feature_columns]
        ].tail(5).copy()

        preview["timestamp"] = preview["timestamp"].dt.strftime(
            "%Y-%m-%d"
        )
        preview_text = preview.to_markdown(index=False, floatfmt=".6f")

        report = f"""# Week 3 — Feature Engineering Report

## Dataset Summary
- Valid rows after feature generation: {stats["rows"]}
- Feature columns: {", ".join(feature_columns)}
- NaN values in features: {stats["nan_count"]}
- Average close price in exported dataset: {stats["average_close"]:.2f}

## Feature Definitions
- `sma_7`: rolling mean of the last seven closing prices.
- `returns_lag_1`: the previous period's close-to-close percentage return.
- `volatility_7d`: rolling sample standard deviation of seven close-to-close returns.

## Last Five Rows

{preview_text}

## Data Quality
Warm-up rows with unavailable rolling or lagged values are removed.
This report uses synthetic sample data and is not a trading recommendation.
"""

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(report, encoding="utf-8")
        return output_path


def main() -> None:
    """Run feature engineering and export the summary report."""
    loader = MarketDataLoader()
    loader.load(DEFAULT_DATA_PATH)
    features = loader.build_feature_matrix()

    report_path = loader.export(DEFAULT_REPORT_PATH)

    print("Feature engineering completed.")
    print(f"Rows in final feature matrix: {len(features)}")
    print(f"NaN values in features: {loader.summary()['nan_count']}")
    print(f"Report saved to: {report_path}")
    print("\nFeature preview:")
    print(
        features[
            ["timestamp", "close", "sma_7",
             "returns_lag_1", "volatility_7d"]
        ].tail().to_string(index=False)
    )


if __name__ == "__main__":
    main()