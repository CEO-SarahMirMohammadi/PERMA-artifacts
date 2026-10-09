from __future__ import annotations

import numpy as np
import pandas as pd


def calculate_returns(
    df: pd.DataFrame,
    method: str = "log",
) -> pd.DataFrame:
    """
    Calculate simple or logarithmic returns from OHLCV close prices.

    Args:
        df: DataFrame containing a 'close' column.
        method: Return calculation method. Supported values:
            'log' or 'simple'.

    Returns:
        A copy of the input DataFrame with a 'returns' column.

    Raises:
        ValueError: If the close column is missing or method is unsupported.
    """

    if "close" not in df.columns:
        raise ValueError("DataFrame must contain a 'close' column.")

    if method not in {"log", "simple"}:
        raise ValueError(
            "method must be either 'log' or 'simple'."
        )

    result = df.copy()

    result["close"] = pd.to_numeric(
        result["close"],
        errors="coerce",
    )

    if method == "log":
        result["returns"] = np.log(
            result["close"] /
            result["close"].shift(1)
        )

    else:
        result["returns"] = result["close"].pct_change()

    return result


if __name__ == "__main__":
    data = pd.DataFrame(
        {
            "close": [100.0, 105.0, 103.0, 110.0],
        }
    )

    result = calculate_returns(data, method="log")

    print(result)

    print(
        "\nMean return:",
        result["returns"].mean(),
    )