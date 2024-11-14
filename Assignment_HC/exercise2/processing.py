import pandas as pd


def calculate_indicators(data, ema_12=False, ema_26=False, bollinger=False, window=20):
    if ema_12:
        data["ema_12"] = data["close"].ewm(span=12, adjust=False).mean()
    if ema_26:
        data["ema_26"] = data["close"].ewm(span=26, adjust=False).mean()
    if bollinger:
        data["sma"] = data["close"].rolling(window=window).mean()
        data["stddev"] = data["close"].rolling(window=window).std()
        data["upper_band"] = data["sma"] + (data["stddev"] * 2)
        data["lower_band"] = data["sma"] - (data["stddev"] * 2)
    return data
