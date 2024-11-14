import plotly.graph_objects as go
import numpy as np
import pandas as pd
import time


def create_figure(data, ema_12=False, ema_26=False, bollinger=False):
    fig = go.Figure(
        data=[
            go.Candlestick(
                x=data["timestamp"],
                open=data["open"],
                high=data["high"],
                low=data["low"],
                close=data["close"],
            )
        ]
    )

    if ema_12:
        fig.add_trace(
            go.Scatter(
                x=data["timestamp"], y=data["ema_12"], mode="lines", name="EMA 12"
            )
        )
    if ema_26:
        fig.add_trace(
            go.Scatter(
                x=data["timestamp"], y=data["ema_26"], mode="lines", name="EMA 26"
            )
        )
    if bollinger:
        fig.add_trace(
            go.Scatter(
                x=data["timestamp"],
                y=data["upper_band"],
                mode="lines",
                line=dict(color="lightgray"),
                name="Upper Band",
            )
        )
        fig.add_trace(
            go.Scatter(
                x=data["timestamp"],
                y=data["lower_band"],
                fill="tonexty",
                mode="lines",
                line=dict(color="lightgray"),
                name="Lower Band",
            )
        )

    fig.update_layout(
        title="OHLCV Data with Indicators", xaxis_title="Time", yaxis_title="Price"
    )
    return fig


def create_large_data_chart():
    # Simulate a complex calculation
    start_time = time.time()
    size = 10000
    x = np.arange(size)
    y = np.random.random(size) * 100

    # Perform some intensive computations to simulate complexity
    z = np.sin(x) ** 2 + np.cos(y) ** 2
    result = np.fft.fft(z)

    elapsed_time = time.time() - start_time
    print(f"Complex calculation took {elapsed_time:.2f} seconds")

    # Create a scatter plot
    fig = go.Figure(data=[go.Scatter(x=x, y=np.abs(result), mode="lines")])
    fig.update_layout(
        title="Complex Calculation Result (FFT)",
        xaxis_title="Index",
        yaxis_title="Value",
    )
    return fig


def create_random_chart(title):
    size = 10000
    x = np.arange(size)
    y = np.random.random(size) * 100

    # Create a bar chart
    fig = go.Figure(data=[go.Bar(x=x, y=y)])
    fig.update_layout(title=title, xaxis_title="Index", yaxis_title="Value")
    return fig
