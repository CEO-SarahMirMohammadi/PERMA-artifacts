
"""Tests for the Week 3 feature engineering pipeline."""

import pandas as pd
import pytest

from src.features import MarketDataLoader


def make_sample_data(rows: int = 20) -> pd.DataFrame:
    """Create deterministic OHLCV data for testing."""
    return pd.DataFrame(
        {
            "timestamp": pd.date_range(
                "2026-07-01", periods=rows, freq="D"
            ),
            "open": [100 + i for i in range(rows)],
            "high": [102 + i for i in range(rows)],
            "low": [99 + i for i in range(rows)],
            "close": [101 + i for i in range(rows)],
            "volume": [1000 + 10 * i for i in range(rows)],
        }
    )


def test_feature_matrix_has_required_columns() -> None:
    """Ensure all three required features are created."""
    loader = MarketDataLoader()
    loader.df = make_sample_data()
    result = loader.build_feature_matrix()

    assert {
        "sma_7",
        "returns_lag_1",
        "volatility_7d",
    }.issubset(result.columns)


def test_feature_matrix_has_no_nan_values() -> None:
    """Ensure generated feature columns contain no NaN values."""
    loader = MarketDataLoader()
    loader.df = make_sample_data()
    result = loader.build_feature_matrix()

    feature_columns = ["sma_7", "returns_lag_1", "volatility_7d"]
    assert not result[feature_columns].isna().any().any()


def test_at_least_eight_rows_remain() -> None:
    """Ensure enough records remain after rolling-window warm-up."""
    loader = MarketDataLoader()
    loader.df = make_sample_data()
    result = loader.build_feature_matrix()

    assert len(result) >= 8


def test_features_require_loaded_data() -> None:
    """Ensure feature generation fails before data is loaded."""
    loader = MarketDataLoader()

    with pytest.raises(RuntimeError):
        loader.add_sma()


def test_missing_file_raises_error(tmp_path) -> None:
    """Ensure a nonexistent input path raises FileNotFoundError."""
    loader = MarketDataLoader()

    with pytest.raises(FileNotFoundError):
        loader.load(tmp_path / "missing.csv")