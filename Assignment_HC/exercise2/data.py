import ccxt
import pandas as pd

# Initialize the exchange
exchange = ccxt.binance()


def fetch_ohlcv(coin):
    # Fetch OHLCV data
    ohlcv = exchange.fetch_ohlcv(coin, timeframe="1m", limit=100)
    # Create a DataFrame
    data = pd.DataFrame(
        ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"]
    )
    data["timestamp"] = pd.to_datetime(data["timestamp"], unit="ms")
    return data
