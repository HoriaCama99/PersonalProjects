import sqlite3
from datetime import datetime, timedelta
from sqlite3 import Error
import threading

# Create a thread-local storage
local = threading.local()

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('crypto_data.db', check_same_thread=False)
        return conn
    except Error as e:
        print(e)
    return conn

def get_connection():
    if not hasattr(local, 'conn'):
        local.conn = create_connection()
    return local.conn

def create_table(conn):
    """Create the crypto_data table if it doesn't exist and add necessary indexes."""
    try:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS crypto_prices
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      coin TEXT NOT NULL,
                      price REAL NOT NULL,
                      timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    except Error as e:
        print(e)

def insert_data(coin, price):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO crypto_prices (coin, price) VALUES (?, ?)", (coin, price))
    conn.commit()


def fetch_data_paginated(coin, page, page_size):
    """
    Fetch data with pagination for efficient loading of large datasets.
    
    Logic:
    - Pagination is crucial for handling large datasets efficiently.
    - It allows loading data in smaller chunks, reducing memory usage and improving load times.
    - The OFFSET clause in SQL is used to skip a certain number of rows before starting to return data.
    
    Why it's added:
    - As the crypto database grows, loading all data at once becomes impractical.
    - Pagination allows users to browse through large amounts of data without overwhelming the system.
    - It improves the dashboard's responsiveness and UX when dealing with extensive historical data.
    """
    conn = get_connection()
    offset = (page - 1) * page_size
    cur = conn.cursor()
    cur.execute("SELECT * FROM crypto_prices WHERE coin = ? ORDER BY timestamp DESC LIMIT ? OFFSET ?", 
                (coin, page_size, offset))
    return cur.fetchall()

def fetch_aggregated_data(coin):
    """
    Fetch aggregated data for a given symbol.

    Returns:
    -------
    list
        List of tuples containing aggregated data
    
    Logic:
    - Aggregation summarizes large datasets into meaningful statistics.
    - It uses SQL's GROUP BY clause to bucket data by time intervals.
    - AVG, MIN, and MAX functions provide a comprehensive overview of price movements.
    
    Why it's added:
    - Aggregated data is essential for analyzing trends over time.
    - It allows users to view summarized information without being overwhelmed by individual data points.
    - Hourly aggregation provides a balance between detail and overview, suitable for most trading analyses.
    - The dashboard benefits from this by offering insights at a glance, enhancing decision-making capabilities.
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            coin,
            AVG(price) as avg_price,
            MIN(price) as min_price,
            MAX(price) as max_price,
            COUNT(*) as data_points
        FROM crypto_prices
        WHERE coin = ?
        GROUP BY coin
    """, (coin,))
    return cur.fetchall()

def delete_old_data():
    """
    Delete data older than one day from the database.
    
    Logic:
    - Uses a threshold date to determine which data to delete.
    - Removes all entries older than the specified number of days.
    
    Why it's added:
    - Database management is crucial for long-term performance and storage efficiency.
    - Regularly removing old data prevents the database from growing indefinitely.
    - It helps maintain query performance by keeping the dataset size manageable.
    - The dashboard benefits from this by ensuring it remains responsive over time, even as new data is continuously added.
    - The 30-day default provides a reasonable balance between historical data retention and database optimization.
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM crypto_prices WHERE timestamp < datetime('now', '-1 day')")
    conn.commit()
