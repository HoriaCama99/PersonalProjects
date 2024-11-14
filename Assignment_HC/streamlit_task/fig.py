import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

def plot_cumulative_returns(portfolio_returns, benchmark_returns):
    """
    Plots the cumulative returns of the portfolio and benchmark using Plotly.
    """
    fig = make_subplots(rows=1, cols=1)

    # Add traces for portfolio and benchmark
    fig.add_trace(
        go.Scatter(
            x=portfolio_returns.index,
            y=portfolio_returns * 100,
            name="Benchmark",
            line=dict(color="black", width=2)
        )
    )
    fig.add_trace(
        go.Scatter(
            x=benchmark_returns.index,
            y=benchmark_returns * 100,
            name="SPX",
            line=dict(color="orange", width=2)
        )
    )

    # Calculate y-axis range
    y_min = min(portfolio_returns.min(), benchmark_returns.min()) * 100
    y_max = max(portfolio_returns.max(), benchmark_returns.max()) * 100
    y_range = [y_min - 5, y_max + 5]  # Add some padding

    # Update layout
    fig.update_layout(
        title="Performance",
        xaxis_title="Date",
        yaxis_title="Cumulative Returns (%)",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        yaxis=dict(
            tickformat=".0%",
            gridcolor="lightgrey",
            zerolinecolor="grey",
            zerolinewidth=1,
            range=y_range
        ),
        xaxis=dict(
            showgrid=False,
            tickformat="%b",
            dtick="M1"
        ),
        plot_bgcolor="white",
        hovermode="x unified",
        height=500,
        margin=dict(l=0, r=0, t=50, b=0)
    )

    # Add a horizontal line at y=0
    fig.add_shape(
        type="line",
        x0=portfolio_returns.index[0],
        y0=0,
        x1=portfolio_returns.index[-1],
        y1=0,
        line=dict(color="grey", width=1, dash="dash"),
    )

    return fig

def display_metrics_table(metrics):
    """
    Displays risk and performance metrics in a table.
    """
    metrics_df = pd.DataFrame(metrics, index=['Value'])
    return metrics_df
