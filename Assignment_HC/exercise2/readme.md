
# Exercise 2 - Dashboard Performance Optimization

This repository contains the code for a data visualization exercise for the Data Visualization position at 21.co. The project demonstrates the use of Streamlit for real-time data visualization, including complex initial data processing and real-time OHLCV (Open, High, Low, Close, Volume) chart updates for cryptocurrency data. It also includes `query.py` for potential SQL queries, even though database integration is not currently implemented.

## Exercise Instructions

The purpose of this exercise is to optimize the dashboard that loads many charts with different sizes and try to optimize loading times & code structure for the user.

### Tasks

1. **Make the dashboard run in Docker**:
   - Complete the Dockerfile to enable running the project in a Docker container instead of using the `streamlit run` command.

2. **Add cache support for data loading**:
   - Use Streamlit's `st.cache` modules to cache data loading and improve performance.

3. **Make the charts load independently**:
   - Use Streamlit's latest feature (fragments) to ensure the dashboard does not reload from the start of the script when filter values change. Update the full dashboard code to have independent parts that reload separately. [Streamlit Fragments Documentation](https://docs.streamlit.io/develop/api-reference/execution-flow/st.fragment)

4. **Open Question**:
   - Suggest and implement any enhancements to handle bigger data sizes or heavier SQL queries that may be added in the future to the dashboard. Explain the approach in some small text if not implemented.
   - Suggest improvements in user experience, including tricks to make users feel that the dashboard is faster to use without optimizing the data loading part.

## Project Structure

```
/project-directory
    /data.py
    /fig.py
    /processing.py
    /query.py
    /main.py
    requirements.txt
    Dockerfile
```

### Files and Their Purpose

- **main.py**: The main Streamlit app file. It sets up the Streamlit interface, handles user input, and updates the real-time chart.
- **data.py**: Contains functions to fetch OHLCV data from the Binance exchange using the `ccxt` library.
- **fig.py**: Contains functions to create and update various charts, including the initial complex data chart and random charts for display before the real-time chart.
- **processing.py**: Contains functions to calculate indicators (like EMA) on the fetched data.
- **query.py**: Contains SQL queries for creating tables, inserting data, fetching data, and deleting data from an SQLite database. Note that database integration is not currently implemented, but this file provides a starting point for working with SQL queries.
- **requirements.txt**: Lists the Python dependencies needed to run the project.
- **Dockerfile**: Currently empty. The Docker instructions are provided as guidelines, but the candidate is expected to write the Dockerfile to make the project work in a Docker container.

## Setup Instructions

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Streamlit app**:
   ```bash
   streamlit run main.py
   ```

## Docker Instructions

The Docker instructions provided below are just guidelines. The Dockerfile is currently empty, and the candidate is expected to code the Dockerfile to make the project work through Docker.

1. **Build the Docker Image**:
   ```bash
   docker build -t streamlit-app .
   ```

2. **Run the Docker Container**:
   ```bash
   docker run -p 8501:8501 streamlit-app
   ```

3. **Access the Streamlit App**:
   Open your web browser and go to `http://localhost:8501` to access the Streamlit app.

## How It Works

### Initial Setup
- The app initializes by displaying a warning message indicating that initial calculations may take some time.
- It then displays a series of charts: a complex data chart and two random charts with simulated loading times between each.

### Real-time Data Visualization
- The main loop fetches OHLCV data for the selected cryptocurrency in real-time.
- It calculates the selected indicators (EMA 12 and EMA 26) and updates the OHLCV chart.
- The chart updates at the specified frequency, displaying the latest market data.

### Database Integration
- Database integration is not currently implemented, but the app includes `query.py` with functions to create tables, insert data, fetch data, and delete old data using SQL queries. Data is intended to be stored in an SQLite database (`crypto.db`).

## Contributing

Feel free to submit issues or pull requests if you find any bugs or have suggestions for improvements.

## License

This project is licensed under the MIT License.
