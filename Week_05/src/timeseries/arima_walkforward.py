"""Evaluate ARIMA walk-forward performance and generate a report."""

from __future__ import annotations

import warnings
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = PROJECT_ROOT / "data" / "mock_ohlcv.csv"
REPORT_PATH = PROJECT_ROOT / "reports" / "walkforward_report.md"
CHART_PATH = PROJECT_ROOT / "reports" / "mae_by_window.png"

TRAIN_WINDOW = 60
TEST_WINDOW = 5
STEP_SIZE = 5
MIN_WINDOWS = 8
CANDIDATE_ORDERS = [
    (0, 0, 0),
    (1, 0, 0),
    (2, 0, 0),
    (0, 1, 1),
    (1, 1, 0),
    (1, 1, 1),
    (2, 1, 0),
    (2, 0, 1),
]


def generate_synthetic_dataset(path: Path) -> pd.DataFrame:
    """Create a synthetic OHLCV dataset when real market data is missing."""
    rng = np.random.default_rng(42)
    dates = pd.date_range("2024-01-01", periods=180, freq="D")
    drift = np.cumsum(rng.normal(0.08, 1.5, len(dates)))
    close = 100 + drift
    open_prices = close - rng.normal(0.6, 0.9, len(dates))
    high = np.maximum(open_prices, close) + rng.uniform(0.5, 2.2, len(dates))
    low = np.minimum(open_prices, close) - rng.uniform(0.5, 2.2, len(dates))
    volume = rng.integers(800, 3400, len(dates))

    df = pd.DataFrame(
        {
            "timestamp": dates.strftime("%Y-%m-%dT%H:%M:%S"),
            "open": open_prices,
            "high": high,
            "low": low,
            "close": close,
            "volume": volume,
        }
    )
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    return df


def load_ohlcv_csv(path: Path) -> pd.DataFrame:
    """Load OHLCV data and generate a synthetic dataset when needed."""
    if not path.exists():
        return generate_synthetic_dataset(path)

    df = pd.read_csv(path)
    required = {"timestamp", "open", "high", "low", "close", "volume"}
    missing = sorted(required - set(df.columns))
    if missing:
        raise ValueError(f"Dataset is missing required columns: {missing}")

    df = df.copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="raise")
    df = df.sort_values("timestamp").reset_index(drop=True)

    numeric_columns = ["open", "high", "low", "close", "volume"]
    df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors="raise")

    if df.empty:
        raise ValueError("The OHLCV dataset is empty.")

    if len(df) < TRAIN_WINDOW + (MIN_WINDOWS - 1) * STEP_SIZE + TEST_WINDOW:
        raise ValueError(
            "The dataset is too short for eight complete walk-forward windows. "
            f"Need at least {TRAIN_WINDOW + (MIN_WINDOWS - 1) * STEP_SIZE + TEST_WINDOW} rows."
        )

    return df


def resample_ohlcv(df: pd.DataFrame, frequency: str = "1D") -> pd.DataFrame:
    """Aggregate OHLCV data to the requested frequency."""
    result = df.copy()
    result = result.set_index("timestamp")

    if result.index.hasnans:
        raise ValueError("The timestamp index contains missing values.")

    if not result.index.is_monotonic_increasing:
        result = result.sort_index()

    aggregated = (
        result.resample(frequency)
        .agg({
            "open": "first",
            "high": "max",
            "low": "min",
            "close": "last",
            "volume": "sum",
        })
        .dropna(subset=["open", "high", "low", "close"])
    )

    if aggregated.empty:
        raise ValueError("The resampled OHLCV dataset is empty.")

    return aggregated


def compute_daily_returns(daily_close: pd.Series) -> pd.Series:
    """Calculate daily close-to-close percentage returns."""
    returns = daily_close.pct_change(fill_method=None).dropna()
    if returns.empty:
        raise ValueError("The returns series is empty after removing the first NaN value.")

    if returns.nunique() < 2:
        raise ValueError("The returns series does not vary enough to evaluate ARIMA models.")

    return returns


def pick_best_arima(train: pd.Series) -> tuple[tuple[int, int, int], float, object]:
    """Select the ARIMA order with the lowest AIC from a small candidate grid."""
    best_order = None
    best_aic = None
    best_fit = None

    for order in CANDIDATE_ORDERS:
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                model = ARIMA(
                    train,
                    order=order,
                    enforce_stationarity=False,
                    enforce_invertibility=False,
                )
                result = model.fit()

            aic = float(result.aic)
            if best_aic is None or aic < best_aic:
                best_order = order
                best_aic = aic
                best_fit = result
        except Exception:
            continue

    if best_order is None or best_fit is None or best_aic is None:
        raise ValueError("No ARIMA model in the candidate grid converged on the training data.")

    return best_order, best_aic, best_fit


def run_walk_forward_validation(returns: pd.Series) -> list[dict[str, object]]:
    """Run rolling-window evaluation and compute MAE per test window."""
    results: list[dict[str, object]] = []

    for start in range(0, len(returns) - TRAIN_WINDOW - TEST_WINDOW + 1, STEP_SIZE):
        train_end = start + TRAIN_WINDOW
        test_end = train_end + TEST_WINDOW

        if test_end > len(returns):
            break

        train = returns.iloc[start:train_end]
        test = returns.iloc[train_end:test_end]

        order, aic, fit = pick_best_arima(train)
        forecast = fit.forecast(steps=len(test))
        forecast_values = np.asarray(forecast)
        actual_values = np.asarray(test)
        mae = float(np.mean(np.abs(actual_values - forecast_values)))

        results.append(
            {
                "window_number": len(results) + 1,
                "train_start": train.index[0].strftime("%Y-%m-%d"),
                "train_end": train.index[-1].strftime("%Y-%m-%d"),
                "test_start": test.index[0].strftime("%Y-%m-%d"),
                "test_end": test.index[-1].strftime("%Y-%m-%d"),
                "order": order,
                "aic": float(aic),
                "mae": mae,
            }
        )

        if len(results) >= MIN_WINDOWS:
            break

    if len(results) < MIN_WINDOWS:
        raise ValueError(
            f"Unable to produce eight complete test windows. Observed {len(results)}. "
            "Increase the dataset length or adjust the rolling validation configuration."
        )

    return results


def generate_mae_chart(results: list[dict[str, object]], output_path: Path) -> None:
    """Plot the MAE for each test window."""
    labels = [item["window_number"] for item in results]
    maes = [float(item["mae"]) for item in results]

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(labels, maes, marker="o", color="#2563eb", linewidth=2)
    ax.set_title("MAE by Walk-Forward Test Window")
    ax.set_xlabel("Test window")
    ax.set_ylabel("MAE")
    ax.grid(True, linestyle="--", alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)


def build_report(results: list[dict[str, object]], dataset_path: Path) -> str:
    """Build a Markdown summary of the walk-forward validation results."""
    maes = [float(item["mae"]) for item in results]
    mean_mae = float(np.mean(maes))
    std_mae = float(np.std(maes, ddof=1)) if len(maes) > 1 else 0.0

    rows = "\n".join(
        [
            "| {window} | {train_start} | {train_end} | {test_start} | {test_end} | {order} | {aic:.4f} | {mae:.6f} |".format(
                window=item["window_number"],
                train_start=item["train_start"],
                train_end=item["train_end"],
                test_start=item["test_start"],
                test_end=item["test_end"],
                order=item["order"],
                aic=float(item["aic"]),
                mae=float(item["mae"]),
            )
            for item in results
        ]
    )

    return f"""# Week 5 — ARIMA Walk-Forward Evaluation

## Dataset and evaluation setup

- Input dataset: `{dataset_path}`
- Training window: {TRAIN_WINDOW} daily observations
- Test horizon: {TEST_WINDOW} daily observations
- Step size: {STEP_SIZE} observations
- Candidate ARIMA orders: {CANDIDATE_ORDERS}
- Evaluated windows: {len(results)}

## Detailed results

| Window | Train start | Train end | Test start | Test end | ARIMA order | AIC | MAE |
|---|---|---|---|---|---|---:|---:|
{rows}

## Summary metrics

- Mean MAE: {mean_mae:.6f}
- Standard deviation of MAE: {std_mae:.6f}

## Interpretation

The rolling walk-forward test refits an ARIMA model on each training window and compares the forecast against the next unseen five-day horizon. The selected order is the one with the lowest AIC in the small candidate grid for that training window. The average MAE and the spread in MAE across windows summarize how stable the model is across different market states.

Forecast error is useful for model assessment, but it does not prove profitability. Actual trading performance also depends on execution costs, market conditions, risk controls, and the decision rules used after the forecast is produced.

## Limitations

- The synthetic or provided dataset may not reflect live market regimes.
- AIC helps compare candidate models for each training window, but it is not a guarantee of superior trading performance.
- MAE provides a straightforward average error measure, yet it does not show directionality or whether the forecast captures volatility clustering.
- This study is for learning and exploration, not a production trading system.
"""


def main() -> None:
    """Generate the walk-forward report and MAE chart."""
    raw_df = load_ohlcv_csv(DATA_PATH)
    daily = resample_ohlcv(raw_df, frequency="1D")
    close_prices = daily["close"].dropna()
    returns = compute_daily_returns(close_prices)

    results = run_walk_forward_validation(returns)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(build_report(results, DATA_PATH), encoding="utf-8")
    generate_mae_chart(results, CHART_PATH)

    print(f"Available rows in price series: {len(close_prices)}")
    print(f"Evaluated walk-forward windows: {len(results)}")
    print(f"Mean MAE: {float(np.mean([float(item['mae']) for item in results])):.6f}")
    print(f"Report saved to: {REPORT_PATH}")
    print(f"Chart saved to: {CHART_PATH}")


if __name__ == "__main__":
    main()
