# AZARS Week 5

## Objectives

This week extends the AZARS time-series and blockchain foundation with rolling walk-forward validation, a simple ownership-aware Solidity trade logger, and a Next.js trade list page built as an App Router server component.

## Deliverables

- `src/timeseries/arima_walkforward.py`
- `reports/walkforward_report.md`
- `reports/mae_by_window.png`
- `contracts/TradeLoggerV2.sol`
- `app/trades/page.jsx`
- `docs/why-walk-forward.md`
- `requirements.txt`
- `screenshots/README.md`

## Folder structure

```text
Week_05/
├── app/
│   └── trades/
│       ├── TradeCard.jsx
│       ├── loading.jsx
│       └── page.jsx
├── contracts/
│   └── TradeLoggerV2.sol
├── data/
│   └── mock_ohlcv.csv  (generated automatically when needed)
├── docs/
│   └── why-walk-forward.md
├── reports/
│   ├── mae_by_window.png
│   └── walkforward_report.md
├── screenshots/
│   └── README.md
├── src/
│   └── timeseries/
│       ├── __init__.py
│       └── arima_walkforward.py
├── README.md
├── requirements.txt
└── .gitignore (optional project-local ignores only)
```

## Setup

From the repository root, create and activate a local virtual environment and install dependencies:

```powershell
cd "C:\Users\Admin\Desktop\PERMA-Project\PERMA-Artifacts\Week_05"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## ARIMA walk-forward evaluation

Run the forecast workflow from the Week 5 folder:

```powershell
cd "C:\Users\Admin\Desktop\PERMA-Project\PERMA-Artifacts\Week_05"
python src/timeseries/arima_walkforward.py
```

The script:

- loads or synthesizes OHLCV market data;
- validates the required columns and time index;
- resamples the dataset to daily candles;
- computes daily close-to-close returns;
- evaluates a fixed candidate ARIMA grid using AIC;
- performs rolling walk-forward validation with a 60-day training window, a 5-day test horizon, and a 5-day step;
- computes MAE for every test window;
- writes `reports/walkforward_report.md` and `reports/mae_by_window.png`.

### Expected outputs

- `reports/walkforward_report.md`
- `reports/mae_by_window.png`

### Rolling window, AIC, and MAE

- Rolling window: repeatedly refit the model on a fixed-length training period and assess the next test segment without peeking into future observations.
- Test horizon: 5 daily observations as the evaluation window size.
- AIC: lower AIC indicates a better trade-off between fit and complexity during model selection.
- MAE: mean absolute error measures average absolute forecast error in the same units as returns.

## Solidity: TradeLoggerV2

The contract lives at `contracts/TradeLoggerV2.sol`. It uses OpenZeppelin's `Ownable` and supports owner-controlled logger authorization:

- `mapping(address => bool) public authorizedLoggers`
- `addLogger(address logger)`
- `removeLogger(address logger)`
- `logTrade(...)` restricted to authorized loggers only
- events for logger grant/removal and trade logging

Compile with Solidity `^0.8.20` and OpenZeppelin Contracts v5.x.

### Remix / Sepolia workflow

1. Open [Remix IDE](https://remix.ethereum.org/).
2. Paste `contracts/TradeLoggerV2.sol` and import `@openzeppelin/contracts/access/Ownable.sol`.
3. Compile with a compatible Solidity 0.8.x version.
4. Connect to a wallet configured for Sepolia.
5. Deploy the contract from the owner wallet.
6. Use `addLogger` to authorize a logger address.
7. Call `logTrade` from the authorized logger address.
8. Verify the contract on [Sepolia Etherscan](https://sepolia.etherscan.io/) if deployment is actually completed.

Genuine deployment evidence requires an actual live deployment and Sonar/Etherscan verification. Do not commit private keys, seed phrases, or secrets.

## Next.js trade list

The App Router trade list is implemented in `app/trades/page.jsx` and is designed as a server component. It fetches data from a configurable endpoint using the `AZARS_TRADES_URL` environment variable, with a public fallback used only when the environment variable is undefined.

The page normalizes remote payloads to the shared schema:

```js
{ id, symbol, price, side, timestamp }
```

It handles:

- HTTP failures;
- invalid payload structures;
- missing or malformed fields;
- stable list keys using the normalized trade id.

The file `app/trades/loading.jsx` provides the loading UI expected by Next.js App Router conventions.

## Security notes and limitations

- Walk-forward MAE reduces look-ahead leakage because each fold uses only information available up to its training window.
- Lower forecast error does not guarantee profitability because transaction costs, market impact, liquidity, and model risk still matter.
- The Solidity contract is intentionally simple and learning-oriented; it is not a production-grade access-control design.
- The public demo endpoint should be replaced with the future AZARS API or a trusted internal service.

## References

- [statsmodels ARIMA documentation](https://www.statsmodels.org/stable/generated/statsmodels.tsa.arima.model.ARIMA.html)
- [Pandas time series overview](https://pandas.pydata.org/docs/user_guide/timeseries.html)
- [OpenZeppelin Ownable](https://docs.openzeppelin.com/contracts/5.x/access-control#ownable)
- [Next.js App Router](https://nextjs.org/docs/app)
- [Solidity docs](https://docs.soliditylang.org/)

## Note

The Week 5 work intentionally keeps all deliverables inside the Week 5 folder and leaves Weeks 1–4 unchanged. The statistical workflow is grounded in a documented candidate grid, repeated backtests, and transparent error reporting rather than a single train/test split.
