# Week 5 — ARIMA Walk-Forward Evaluation

## Dataset and evaluation setup

- Input dataset: `C:\Users\Admin\Desktop\PERMA-Project\PERMA-Artifacts\Week_05\data\mock_ohlcv.csv`
- Training window: 60 daily observations
- Test horizon: 5 daily observations
- Step size: 5 observations
- Candidate ARIMA orders: [(0, 0, 0), (1, 0, 0), (2, 0, 0), (0, 1, 1), (1, 1, 0), (1, 1, 1), (2, 1, 0), (2, 0, 1)]
- Evaluated windows: 8

## Detailed results

| Window | Train start | Train end | Test start | Test end | ARIMA order | AIC | MAE |
|---|---|---|---|---|---|---:|---:|
| 1 | 2024-01-02 | 2024-03-01 | 2024-03-02 | 2024-03-06 | (0, 0, 0) | -354.2889 | 0.006624 |
| 2 | 2024-01-07 | 2024-03-06 | 2024-03-07 | 2024-03-11 | (0, 0, 0) | -365.3179 | 0.009448 |
| 3 | 2024-01-12 | 2024-03-11 | 2024-03-12 | 2024-03-16 | (0, 0, 0) | -364.9586 | 0.009129 |
| 4 | 2024-01-17 | 2024-03-16 | 2024-03-17 | 2024-03-21 | (0, 0, 0) | -364.4290 | 0.005295 |
| 5 | 2024-01-22 | 2024-03-21 | 2024-03-22 | 2024-03-26 | (0, 0, 0) | -367.6674 | 0.009168 |
| 6 | 2024-01-27 | 2024-03-26 | 2024-03-27 | 2024-03-31 | (0, 0, 0) | -367.3372 | 0.005636 |
| 7 | 2024-02-01 | 2024-03-31 | 2024-04-01 | 2024-04-05 | (0, 0, 0) | -376.2450 | 0.010255 |
| 8 | 2024-02-06 | 2024-04-05 | 2024-04-06 | 2024-04-10 | (0, 0, 0) | -372.1325 | 0.011036 |

## Summary metrics

- Mean MAE: 0.008324
- Standard deviation of MAE: 0.002171

## Interpretation

The rolling walk-forward test refits an ARIMA model on each training window and compares the forecast against the next unseen five-day horizon. The selected order is the one with the lowest AIC in the small candidate grid for that training window. The average MAE and the spread in MAE across windows summarize how stable the model is across different market states.

Forecast error is useful for model assessment, but it does not prove profitability. Actual trading performance also depends on execution costs, market conditions, risk controls, and the decision rules used after the forecast is produced.

## Limitations

- The synthetic or provided dataset may not reflect live market regimes.
- AIC helps compare candidate models for each training window, but it is not a guarantee of superior trading performance.
- MAE provides a straightforward average error measure, yet it does not show directionality or whether the forecast captures volatility clustering.
- This study is for learning and exploration, not a production trading system.
