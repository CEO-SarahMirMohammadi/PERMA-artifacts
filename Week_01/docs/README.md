
# AZARS Quant Engine — Week 1

## Objective
Build the first Python-based market data ingestion module.

## Deliverables
- CSV parser with schema validation
- OHLCV statistics report
- Reusable `MarketDataLoader` class
- Markdown report generation

## Requirements
- Python 3.10+
- Pandas

## Setup (Windows PowerShell)

Run these commands from the repository root:

```powershell
python -m venv week1/venv
.\week1\venv\Scripts\Activate.ps1
python -m pip install -r week1/requirements.txt
```

## Run Lab 1

```powershell
python week1/src/lab01_csv_parser.py
```

## Run Lab 2

```powershell
python week1/src/lab02_statistics.py
```

## Run Lab 3

```powershell
python week1/src/lab03_loader.py
```

## Generated Reports
- `week1/reports/week1_statistics.md`
- `week1/reports/week1_loader_summary.md`

The dataset is synthetic and intended for educational use only.