# PERMA Project — Week 3

## AZARS: Trading Feature Engineering, Ethereum Concepts & React TradeCard

**Owner:** Sarah MirMohammadi — CEO
**Role:** AI/Data Engineering with Blockchain and MERN fundamentals
**Phase:** Foundations

## Overview

Week 3 builds on the market-data ingestion work from Week 1 and the mathematical foundations from Week 2. The deliverables introduce a small trading feature pipeline, document Ethereum execution concepts, and implement a reusable React trade card.

## Deliverables

| Artifact                       | Purpose                          |
| ------------------------------ | -------------------------------- |
| `src/features.py`              | OHLCV feature engineering        |
| `src/components/TradeCard.jsx` | React component driven by props  |
| `docs/ethereum_concepts.md`    | EVM, Gas, and Ethereum accounts  |
| `docs/why-scaling-matters.md`  | Feature-scaling explanation      |
| `reports/feature_summary.md`   | Generated feature report         |
| `tests/test_features.py`       | Automated feature-pipeline tests |

## Feature Definitions

* **`sma_7`:** Mean of the latest seven closing prices.
* **`returns_lag_1`:** Previous period's close-to-close percentage return.
* **`volatility_7d`:** Rolling standard deviation of seven close-to-close returns.

The initial rolling-window rows do not have all required features. The pipeline removes these warm-up rows and checks that the final feature columns contain no NaN values.

## Requirements

* Python 3.10+
* Pandas
* Tabulate
* Pytest

## Setup — Windows PowerShell

Run from the repository root:

```powershell
cd Week-03
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Run the Feature Pipeline

```powershell
python src/features.py
```

The pipeline reads `data/mock_ohlcv.csv` and generates:

`reports/feature_summary.md`

## Run Tests

```powershell
python -m pytest -v
```

The tests check required feature columns, missing values, remaining row count, and error handling.

## React Component

`src/components/TradeCard.jsx` receives `symbol`, `price`, `side`, and `timestamp` as props. It is intended to be imported into a React or Next.js application; the Python environment does not run JSX.

## Ethereum Concepts

See `docs/ethereum_concepts.md` for the EVM, Gas, accounts, and a transaction-flow diagram.

## Feature Scaling

See `docs/why-scaling-matters.md` for the role of scaling in machine learning and the importance of preventing data leakage.

## Scope and Limitations

This is a learning artifact using synthetic market data. It does not produce buy/sell recommendations, connect to a live exchange, deploy a smart contract, or implement a complete MERN application.

## References

* [Pandas — Windowing Operations](https://pandas.pydata.org/docs/user_guide/window.html)
* [Ethereum.org — EVM](https://ethereum.org/en/developers/docs/evm/)
* [React — Thinking in React](https://react.dev/learn/thinking-in-react)
* Géron, *Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow*, Chapter 2.
