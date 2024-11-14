import yfinance as yf
import streamlit as st

@st.cache_data
def get_stock_data(ticker, period):
    """
    Fetches daily prices or OHLCV data for a given ticker.
    """
    data = yf.download(ticker, period=period)  