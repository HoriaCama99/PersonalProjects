import pandas as pd
import numpy as np

def calculate_cumulative_returns(data):
    """
    Calculates cumulative returns from price data.
    """
    if isinstance(data, pd.Series):
        returns = data.pct_change().fillna(0)
    else:
        returns = data['Adj Close'].pct_change().fillna(0)
    cumulative_returns = (1 + returns).cumprod() - 1
    return cumulative_returns


def calculate_annual_volatility(returns):
    """
    Calculates the annualized volatility of returns.
    """
    return returns.std() * np.sqrt(252)  # Assuming 252 trading days in a year

def calculate_sharpe_ratio(returns, risk_free_rate=0.01):
    """
    Calculates the Sharpe Ratio of the portfolio.
    """
    excess_returns = returns.mean() - risk_free_rate / 252
    return excess_returns / returns.std() * np.sqrt(252)

def calculate_maximum_drawdown(cumulative_returns):
    """
    Calculates the maximum drawdown of the portfolio.
    """
    peak = cumulative_returns.expanding(min_periods=1).max()
    drawdown = (cumulative_returns - peak) / peak
    return drawdown.min()
from scipy import stats

def calculate_var(returns, confidence=0.95, period=252):
    """
    Calculate Value at Risk (VaR).
    
    :param returns: pandas Series of returns
    :param confidence: confidence level (default 0.95 for 95% VaR)
    :param period: number of trading days to annualize (default 252 for annual)
    :return: VaR as a positive percentage
    """
    if returns.empty:
        return np.nan
    
    # Calculate the percentile
    var = returns.quantile(1 - confidence)
    
    # Annualize the VaR
    var_annual = var * np.sqrt(period)
    
    # Return as a positive percentage
    return -var_annual

def calculate_tracking_error(portfolio_returns, benchmark_returns):
    """Calculate Tracking Error."""
    return np.std(portfolio_returns - benchmark_returns) * np.sqrt(252)

def calculate_information_ratio(portfolio_returns, benchmark_returns):
    """Calculate Information Ratio."""
    excess_returns = portfolio_returns - benchmark_returns
    return np.mean(excess_returns) / np.std(excess_returns) * np.sqrt(252)

def calculate_sortino_ratio(returns, risk_free_rate=0.01):
    """Calculate Sortino Ratio."""
    excess_returns = returns - risk_free_rate / 252
    downside_returns = np.minimum(excess_returns, 0)
    downside_deviation = np.sqrt(np.mean(downside_returns**2)) * np.sqrt(252)
    return np.mean(excess_returns) * 252 / downside_deviation if downside_deviation != 0 else np.nan

def calculate_alpha_beta(portfolio_returns, benchmark_returns):
    """Calculate Alpha and Beta."""
    # Ensure both series have the same index
    portfolio_returns, benchmark_returns = pd.Series(portfolio_returns).align(pd.Series(benchmark_returns), join='inner')
    
    # Drop any NaN values
    valid_data = pd.concat([portfolio_returns, benchmark_returns], axis=1).dropna()
    
    if len(valid_data) < 2:
        return np.nan, np.nan  # Not enough data to calculate

    portfolio_returns = valid_data.iloc[:, 0]
    benchmark_returns = valid_data.iloc[:, 1]

    covariance = np.cov(portfolio_returns, benchmark_returns)[0][1]
    benchmark_variance = np.var(benchmark_returns)
    
    if benchmark_variance == 0:
        return np.nan, np.nan  # Avoid division by zero

    beta = covariance / benchmark_variance
    alpha = np.mean(portfolio_returns) - beta * np.mean(benchmark_returns)
    return alpha * 252, beta  # Annualized alpha