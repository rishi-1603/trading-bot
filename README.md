# Binance Futures Testnet Trading Bot

A small Python CLI app that places MARKET and LIMIT orders on Binance Futures Testnet (USDT-M).

## Features
- BUY and SELL support
- MARKET and LIMIT orders
- CLI validation
- Request/response/error logging
- Separate client, order, validator, and CLI layers

## Project Structure
```text
trading_bot/
├── bot/
│   ├── __init__.py
│   ├── client.py
│   ├── orders.py
│   ├── validators.py
│   ├── logging_config.py
│   └── cli.py
├── logs/
├── .env.example
├── requirements.txt
└── README.md
```

## Setup
1. Create a virtual environment.
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Create a `.env` file:
```bash
BINANCE_API_KEY=your_testnet_key
BINANCE_API_SECRET=your_testnet_secret
```

## Run Examples
### Market order
```bash
python -m bot.cli --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

### Limit order
```bash
python -m bot.cli --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 70000
```

## Logs
Logs are written to:
```text
logs/trading_bot.log
```

## Assumptions
- This project uses Binance Futures Testnet only.
- Quantity and price are passed as decimal values.
- `avgPrice` may not always be returned by the API, so `N/A` is shown when missing.