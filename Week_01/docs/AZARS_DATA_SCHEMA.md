
# AZARS Market Data Schema

## Week 1 OHLCV Schema

| Field | Type | Description |
|---|---|---|
| `timestamp` | ISO 8601 datetime | Observation timestamp |
| `open` | float | Opening price |
| `high` | float | Highest price |
| `low` | float | Lowest price |
| `close` | float | Closing price |
| `volume` | numeric | Trading volume |

## Extended Shared Schema

The wider AZARS platform may also use:

- `symbol`: instrument identifier
- `bid`: best bid price
- `ask`: best ask price

These fields are not required in the Week 1 sample CSV.

## Validation Rules

- All required columns must exist.
- Timestamps must be parseable.
- OHLCV values must be numeric.
- Empty datasets must be rejected.
- Missing files must raise a clear error.