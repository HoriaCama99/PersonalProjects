import streamlit as st
import pandas as pd
from data import fetch_ohlcv
from fig import create_figure, create_large_data_chart, create_random_chart
from processing import calculate_indicators
from query import get_connection, create_table, insert_data, fetch_data_paginated, fetch_aggregated_data, delete_old_data

# Caching for performance optimization
@st.cache_data(ttl=60)
def cached_fetch_ohlcv(coin):
    """
    Cache OHLCV data to reduce API calls and improve responsiveness.
    
    Motivation: Reduces the number of API calls, which can be rate-limited or slow,
    improving the overall responsiveness of the dashboard.
    """
    return fetch_ohlcv(coin)

@st.cache_data(ttl=60)
def cached_calculate_indicators(data, ema_12, ema_26, bollinger, window):
    """
    Cache indicator calculations to reduce computational overhead.
    
    Motivation: Indicator calculations can be computationally expensive. Caching these
    calculations significantly improves performance, especially for larger datasets.
    """
    return calculate_indicators(data, ema_12, ema_26, bollinger, window)

# Database setup
conn = get_connection()
if conn is not None:
    create_table(conn)
else:
    st.error("Error! Cannot create the database connection.")

# UI Setup
st.title("21.co Streamlit Test - Optimization Exercise")

# Sidebar configuration
st.sidebar.title("Filters")
coin = st.sidebar.selectbox("Select Coin", ["BTC/USDT", "ETH/USDT", "LTC/USDT"])
frequency = st.sidebar.selectbox("Select Update Frequency", ["1 second", "5 seconds", "10 seconds"])
frequency_map = {"1 second": 1, "5 seconds": 5, "10 seconds": 10}

st.sidebar.title("Indicators")
show_ema_12 = st.sidebar.checkbox("Show EMA 12", value=True)
show_ema_26 = st.sidebar.checkbox("Show EMA 26", value=True)
show_bollinger = st.sidebar.checkbox("Show Bollinger Bands", value=True)
bollinger_window = st.sidebar.slider("Bollinger Bands Window", 10, 50, 10)

# Placeholders for dynamic content
message_placeholder = st.empty()
message_placeholder.warning("Please wait, the initial calculations may take some time...")

tabs = st.tabs(["Large Data Chart", "Random Chart 1", "Random Chart 2", "OHLCV Chart"])
large_data_placeholder, random_chart_1_placeholder, random_chart_2_placeholder, ohlcv_chart_placeholder = [tab.empty() for tab in tabs]
latest_data_placeholder = st.empty()
aggregated_data_placeholder = st.empty()

# Chart update functions
@st.fragment(run_every="10s")
def display_large_data_chart():
    """
    Display large dataset chart, refreshing every 10 seconds.
    
    Motivation: Demonstrates the dashboard's capability to handle and visualize large datasets.
    The 10-second refresh interval provides regular updates without overwhelming the system.
    
    Use of st.fragment:
    - Purpose: Enables automatic, periodic updates of the chart without full page reloads.
    - Implementation: The @st.fragment decorator with run_every="10s" ensures this function
      is re-executed every 10 seconds, providing real-time updates to the large data chart.
    - Benefit: Improves user experience by providing live data updates without manual refreshing,
      while being more efficient than updating the entire page.
    """
    large_data_fig = create_large_data_chart()
    large_data_placeholder.plotly_chart(large_data_fig, use_container_width=True)

@st.fragment(run_every="10s")
def display_random_chart(placeholder, title):
    """
    Display random chart, refreshing every 10 seconds.
    
    Motivation: Simulates real-time data updates and demonstrates the dashboard's
    ability to handle multiple updating charts simultaneously.
    
    Use of st.fragment:
    - Purpose: Allows for independent, periodic updates of each random chart.
    - Implementation: Similar to the large data chart, this function uses @st.fragment
      to update every 10 seconds, creating a dynamic, constantly changing visualization.
    - Benefit: Showcases the ability to have multiple, independently updating components
      on the same dashboard, enhancing the real-time feel of the application.
    """
    random_chart = create_random_chart(title)
    placeholder.plotly_chart(random_chart, use_container_width=True)

@st.fragment(run_every=frequency_map[frequency])
def update_ohlcv_chart():
    """
    Update OHLCV chart and related data displays.
    
    Motivation: This function is the core of the dashboard, providing real-time updates
    of cryptocurrency data. It combines data fetching, processing, storage, and visualization.
    The use of progress indicators improves user experience during data loading.
    
    Use of st.fragment:
    - Purpose: Enables user-configurable, real-time updates of the OHLCV chart and related data.
    - Implementation: 
      1. The @st.fragment decorator is used with a dynamic run_every parameter.
      2. frequency_map[frequency] allows users to select the update frequency (1, 5, or 10 seconds).
      3. This implementation provides flexibility in update rates while maintaining real-time functionality.
    - Benefit: 
      1. Allows for more frequent updates of critical data compared to other charts.
      2. Provides users control over update frequency, balancing between data freshness and system load.
      3. Ensures that the most important data (OHLCV) is updated at a rate suitable for trading decisions.
    """
    with st.spinner('Loading data...'):
        data = cached_fetch_ohlcv(coin)
        data = cached_calculate_indicators(data, show_ema_12, show_ema_26, show_bollinger, bollinger_window)
        
        if len(data) > 0:
            latest_data = data.iloc[-1]
            insert_data(coin.split('/')[0], latest_data['close'])
    
        db_data = fetch_data_paginated(coin.split('/')[0], page=1, page_size=5)
        fig = create_figure(data, ema_12=show_ema_12, ema_26=show_ema_26, bollinger=show_bollinger)
    
    ohlcv_chart_placeholder.plotly_chart(fig, use_container_width=True)
    
    with latest_data_placeholder.container():
        st.write("Latest data from database:")
        st.dataframe(pd.DataFrame(db_data, columns=["ID", "Coin", "Price", "Timestamp"]), use_container_width=True)

    with aggregated_data_placeholder.container():
        st.write("Aggregated Data:")
        agg_data = fetch_aggregated_data(coin.split('/')[0])
        st.dataframe(pd.DataFrame(agg_data, columns=["Coin", "Avg Price", "Min Price", "Max Price", "Data Points"]), use_container_width=True)

# Initialize charts
display_large_data_chart()
display_random_chart(random_chart_1_placeholder, "Random Chart 1")
display_random_chart(random_chart_2_placeholder, "Random Chart 2")
update_ohlcv_chart()

message_placeholder.success("Finished heavy processing charts. Now displaying real-time OHLCV chart.")

# Data management
if st.button("Clean up old data"):
    """
    Motivation: Provides a way to manage database size and maintain performance.
    Regular cleanup of old data is crucial for long-term maintenance of the dashboard.
    """
    delete_old_data()
    st.success("Old data cleaned up successfully!")

# Pagination for historical data
st.write("Display more items")
page = st.number_input("Page", min_value=1, value=1)
page_size = st.selectbox("Items per page", [10, 20, 50, 100])

if st.button("Load More Data"):
    """
    Motivation: Pagination allows users to browse through large amounts of historical data
    efficiently. This improves performance by loading data in smaller chunks and provides
    a better user experience for exploring extensive datasets.
    """
    more_data = fetch_data_paginated(coin.split('/')[0], page=page, page_size=page_size)
    st.dataframe(more_data, use_container_width=True)
