import streamlit as st
import pandas as pd
import yfinance as yf
from query import get_stock_data
from processing import (
    calculate_cumulative_returns,
    calculate_annual_volatility,
    calculate_sharpe_ratio,
    calculate_maximum_drawdown,
    calculate_var,
    calculate_tracking_error,
    calculate_information_ratio,
    calculate_sortino_ratio,
    calculate_alpha_beta
)
from fig import plot_cumulative_returns

# Define asset classes and their corresponding types
ASSET_CLASSES = {
    "Equity": ["Stock"],
    "Fixed Income": ["Fixed Income"],
    "Commodities": ["Commodity"],
    "Crypto": ["Crypto"]
}

# Define time periods for data retrieval
# These periods align with common financial reporting periods
PERIODS = {
    "1M": "1mo", "3M": "3mo",
    "6M": "6mo", "1Y": "1y", "YTD": "ytd"
}

# Initialize session state
# This allows data persistence between Streamlit reruns
if 'portfolio' not in st.session_state:
    st.session_state.portfolio = {}
if 'total_value' not in st.session_state:
    st.session_state.total_value = 100000.0  # Default to $100,000

@st.cache_data
def get_stock_data(ticker, period):
    """
    Fetches daily prices or OHLCV data for a given ticker.
    """
    data = yf.download(ticker, period=period)
    return data

def add_asset():
    """
    Add a new asset to the portfolio.
    This function is triggered when the user clicks the "Add Asset" button.
    It checks for duplicate assets and ensures a ticker is provided.
    """
    asset_class = st.session_state.new_asset_class
    ticker = st.session_state.new_asset_ticker.upper()
    asset_type = st.session_state.new_asset_type
    if ticker and ticker not in st.session_state.portfolio:
        st.session_state.portfolio[ticker] = {
            "class": asset_class,
            "type": asset_type,
            "weight": 0.0,
            "value": 0.0
        }
        st.success(f"Added {ticker} to the portfolio.")
    elif ticker in st.session_state.portfolio:
        st.warning(f"{ticker} is already in the portfolio.")
    else:
        st.warning("Please enter a ticker symbol.")

def delete_asset(ticker):
    """
    Remove an asset from the portfolio.
    This function is triggered when the user clicks the "Delete" button for an asset.
    It removes the asset and triggers a rerun to update the UI.
    """
    if ticker in st.session_state.portfolio:
        del st.session_state.portfolio[ticker]
        st.success(f"Removed {ticker} from the portfolio.")
        st.rerun()

def main():
    """
    Main function to run the Streamlit app.
    This function handles the overall flow of the application, including:
    - UI layout
    - Portfolio management
    - Data retrieval and processing
    - Performance calculation and visualization
    """
    st.set_page_config(layout="wide", page_title="Portfolio Simulator")
    
    # Apply custom CSS styles for better UI
    st.markdown("""
    <style>
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }
    .asset-box {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    .asset-title {
        font-weight: bold;
        font-size: 1.1em;
        margin-bottom: 0.5rem;
    }
    .sub-asset {
        margin-left: 1rem;
        margin-bottom: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)

    st.title("Portfolio Simulator")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.subheader("Portfolio Composition")
        
        # Input for total portfolio value
        st.session_state.total_value = st.number_input("Total Portfolio Value ($)", 
                                                       min_value=0.0, 
                                                       value=st.session_state.total_value, 
                                                       step=1000.0, 
                                                       format="%.2f")
        
        # Asset addition interface
        with st.expander("Add Asset"):
            new_asset_class = st.selectbox("Asset Class", list(ASSET_CLASSES.keys()), key="new_asset_class")
            new_asset_type = st.selectbox("Asset Type", ASSET_CLASSES[new_asset_class], key="new_asset_type")
            new_asset_ticker = st.text_input("Ticker", key="new_asset_ticker")
            if st.button("Add Asset"):
                add_asset()
        
        # Choose between percentage or absolute allocation
        allocation_type = st.radio("", ("% Weighted", "$ Absolute"), horizontal=True)
        
        total_weight = 0.0
        total_value = 0.0
        
        # Display and manage assets by class
        for asset_class in ASSET_CLASSES:
            class_weight = sum(asset['weight'] for asset in st.session_state.portfolio.values() if asset['class'] == asset_class)
            class_value = sum(asset['value'] for asset in st.session_state.portfolio.values() if asset['class'] == asset_class)
            
            st.markdown(f"""
            <div class='asset-class-header'>
                <span class='asset-class-title'>{asset_class}</span>
                <span class='asset-class-total'>{class_weight*100:.1f}% | ${class_value:,.2f}</span>
            </div>
            """, unsafe_allow_html=True)
            
            for ticker, asset in list(st.session_state.portfolio.items()):
                if asset['class'] == asset_class:
                    # Display asset info
                    st.markdown(f"""
                    <div class='asset-info'>
                        <span class='asset-label'><strong>{ticker}</strong></span>
                        <span class='asset-type'>{asset['type']}</span>
                        </span>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Handle asset allocation input
                    if allocation_type == "% Weighted":
                        value = st.slider(f"Weight (%)", 0.0, 100.0, float(asset['weight'] * 100), 0.1, key=f"{asset_class}_{ticker}")
                        asset['weight'] = value / 100
                        asset['value'] = asset['weight'] * st.session_state.total_value
                    else:  # $ Absolute
                        value = st.number_input(f"Value ($)", 0.0, float(st.session_state.total_value), float(asset['value']), key=f"{asset_class}_{ticker}")
                        asset['value'] = value
                        asset['weight'] = asset['value'] / st.session_state.total_value if st.session_state.total_value != 0 else 0.0
                    
                    # Delete asset button
                    if st.button(f"Delete {ticker}", key=f"delete_{ticker}"):
                        delete_asset(ticker)
                        st.rerun()
                    
                    st.markdown("<hr>", unsafe_allow_html=True)

                    total_weight += asset['weight']
                    total_value += asset['value']
                    
                    # Display current allocation
                    display_value = f"{asset['weight']*100:.2f}%" if allocation_type == "% Weighted" else f"${asset['value']:,.2f}"
                    st.markdown(f"<div class='asset-allocation'>Current allocation: {display_value}</div>", unsafe_allow_html=True)
                    
                    st.markdown("<hr>", unsafe_allow_html=True)
            
            # Display total for asset class
            st.markdown(f"<div class='asset-total-weight'>Total {asset_class}: {class_weight*100:.1f}%" if allocation_type == "% Weighted" else f"${class_value:,.2f}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Display total portfolio allocation
        total_display = f"{total_weight*100:.1f}%" if allocation_type == "% Weighted" else f"${total_value:,.2f}"
        st.metric("Total Portfolio", total_display)
        
        # Normalize portfolio if total weight exceeds 100%
        if total_weight > 1.0:
            st.warning("Total weight exceeds 100%. Portfolio will be normalized.")
            for asset in st.session_state.portfolio.values():
                asset['weight'] /= total_weight
                asset['value'] = asset['weight'] * st.session_state.total_value
        
        st.button("Save as benchmark portfolio", key="save_benchmark")
    
    with col2:
        # Period selector for data retrieval
        selected_period = st.radio("Select Period", list(PERIODS.keys()), horizontal=True)
        period = PERIODS[selected_period]
        
        # Fetch data and calculate returns
        data = {}
        valid_tickers = []
        for ticker, asset in st.session_state.portfolio.items():
            if asset['weight'] > 0:
                stock_data = get_stock_data(ticker, period)
                if not stock_data.empty and 'Adj Close' in stock_data.columns:
                    data[ticker] = stock_data
                    valid_tickers.append(ticker)
                else:
                    st.warning(f"No valid data available for {ticker}. It will be excluded from the portfolio calculations.")
        
        if not data:
            st.warning("No valid data available for any assets in the portfolio.")
            return
        
        # Calculate portfolio returns
        portfolio_returns = pd.Series(0, index=data[valid_tickers[0]].index)
        for ticker in valid_tickers:
            portfolio_returns += data[ticker]['Adj Close'].pct_change() * st.session_state.portfolio[ticker]['weight']
        
        # Fetch benchmark data (S&P 500)
        benchmark_data = get_stock_data("^GSPC", period)
        if benchmark_data.empty or 'Adj Close' not in benchmark_data.columns:
            st.warning("Unable to fetch benchmark data. Proceeding without benchmark comparison.")
            benchmark_returns = None
        else:
            benchmark_returns = benchmark_data['Adj Close'].pct_change().dropna()

        # Calculate cumulative returns
        cumulative_returns = calculate_cumulative_returns(portfolio_returns)
        
        if benchmark_returns is not None:
            benchmark_cumulative_returns = calculate_cumulative_returns(benchmark_returns)
            # Align the data to ensure comparison over the same time period
            cumulative_returns, benchmark_cumulative_returns = cumulative_returns.align(benchmark_cumulative_returns, join='inner')
        else:
            benchmark_cumulative_returns = None

        # Display results
        st.subheader("Performance")
        chart_col, results_col = st.columns([2, 1])
        
        with chart_col:
            if not cumulative_returns.empty:
                fig = plot_cumulative_returns(cumulative_returns, benchmark_cumulative_returns)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Not enough data to display the chart for the selected period.")
        
        with results_col:
            st.markdown('<div class="results-table">', unsafe_allow_html=True)
            st.subheader("Results")
            
            try:
                # Calculate and display various portfolio metrics
                start_date = portfolio_returns.index[0].strftime('%m/%d/%Y')
                end_date = portfolio_returns.index[-1].strftime('%m/%d/%Y')
                cumulative_ret = cumulative_returns.iloc[-1]
                annual_ret = (1 + portfolio_returns.mean()) ** 252 - 1  # Annualize daily returns
                annual_vol = calculate_annual_volatility(portfolio_returns)
                var_95 = calculate_var(portfolio_returns, confidence=0.95)  # 95% VaR is a common risk measure
                max_drawdown = calculate_maximum_drawdown(cumulative_returns)
                tracking_error = calculate_tracking_error(portfolio_returns, benchmark_returns)
                information_ratio = calculate_information_ratio(portfolio_returns, benchmark_returns)
                sharpe_ratio = calculate_sharpe_ratio(portfolio_returns)
                sortino_ratio = calculate_sortino_ratio(portfolio_returns)
                
                # Ensure portfolio_returns and benchmark_returns are pandas Series
                portfolio_returns = pd.Series(portfolio_returns)
                benchmark_returns = pd.Series(benchmark_returns)

                # Calculate alpha and beta
                alpha, beta = calculate_alpha_beta(portfolio_returns, benchmark_returns)
                
                metrics = {
                    "startDate": start_date,
                    "endDate": end_date,
                    "cumulativeRet": f"{cumulative_ret:.2%}",
                    "annRet": f"{annual_ret:.2%}",
                    "annVol": f"{annual_vol:.2%}",
                    "VaR95 (annually)": f"{var_95:.2%}",
                    "maxDrawdown": f"{max_drawdown:.2%}",
                    "trackingError": f"{tracking_error:.2%}",
                    "infoRatio": f"{information_ratio:.2f}",
                    "sharpeRatio": f"{sharpe_ratio:.2f}",
                    "sortinoRatio": f"{sortino_ratio:.2f}",
                    "alpha (vs SP500)": f"{alpha:.2%}",
                    "beta (vs SP500)": f"{beta:.2f}"
                }
                
                for key, value in metrics.items():
                    st.text(f"{key:<20} {value:>10}")
            except IndexError:
                st.warning("Not enough data to calculate metrics. Please ensure your portfolio contains assets and data is available for the selected period.")
            
            st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
