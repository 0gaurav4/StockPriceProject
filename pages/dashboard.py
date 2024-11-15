import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_data():
    # Load the dataset (replace with your actual dataset path)
    data = pd.read_csv("stocks.csv")  # Replace with the path to your dataset
    data['Date'] = pd.to_datetime(data['Date'])
    return data

def plot_graph(df, title, x_col, y_col, kind='line', color='blue'):
    fig, ax = plt.subplots()
    if kind == 'line':
        ax.plot(df[x_col], df[y_col], color=color)
    elif kind == 'scatter':
        ax.scatter(df[x_col], df[y_col], color=color)
    elif kind == 'bar':
        ax.bar(df[x_col], df[y_col], color=color)
    ax.set_title(title)
    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
    return fig

def show_dashboard_page():
    st.title("Stock Market Dashboard")

    # Load dataset
    data = load_data()

    # Filters
    tickers = data['Ticker'].unique()
    selected_ticker = st.sidebar.selectbox("Select Ticker", tickers)
    
    date_range = st.sidebar.date_input("Select Date Range", [data['Date'].min(), data['Date'].max()], key='date_range')
    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_date, end_date = date_range
    else:
        st.warning("Please select a start and end date.")
        return
    filtered_data = data[(data['Date'] >= pd.to_datetime(start_date)) & (data['Date'] <= pd.to_datetime(end_date))]

    # Filtered data based on selected ticker
    filtered_data = filtered_data[filtered_data['Ticker'] == selected_ticker]

    st.write("""
### :green[What is a ***Ticker***?]
A **Ticker** is a unique symbol or abbreviation used to represent a publicly traded company or asset on a stock exchange. 
These symbols are typically made up of a few letters and help investors and traders identify and track the performance of specific stocks.
For example:
- **AAPL** represents Apple Inc.
- **TSLA** represents Tesla, Inc.
- **GOOGL** represents Alphabet Inc. (Google’s parent company).""")

    # Display Ticker and Date Range Info
    st.success(f"Showing data for  **{selected_ticker}**  from  **{date_range[0]}**  to  **{date_range[1]}**")


    # Stock Price Graphs
    st.header(":blue[Stock Price and Volume Analysis]")
    st.subheader(":green[Overview of Key Metrics]")
    st.write("""
    - Close: The closing price of the stock on a given day.
    - Open: The opening price of the stock on a given day.
    - High: The highest price of the stock on a given day.
    - Low: The lowest price of the stock on a given day.
    - Adj Close: The adjusted closing price of the stock on a given day.
    - Volume: The number of shares traded on a given day.
    """)

    col1, col2 = st.columns(2)
    
    with col1:
        st.pyplot(plot_graph(filtered_data, "Close Price Over Time", 'Date', 'Close', kind='line', color='green'))
        st.pyplot(plot_graph(filtered_data, "Open Price Over Time", 'Date', 'Open', kind='line', color='blue'))
        st.pyplot(plot_graph(filtered_data, "High Price Over Time", 'Date', 'High', kind='line', color='orange'))
        st.pyplot(plot_graph(filtered_data, "Low Price Over Time", 'Date', 'Low', kind='line', color='red'))
        st.pyplot(plot_graph(filtered_data, "Adj Close Price Over Time", 'Date', 'Adj Close', kind='line', color='purple'))

    st.write("""
    - :green[**Chart Descriptions :**]
    - Volume Over Time: The volume of shares traded over time.
    - Price vs Volume (Scatter): The relationship between the closing price and the volume of shares traded.
    - High vs Low Price: The relationship between the high and low prices over time.
    - Open vs Close Price: The relationship between the opening and closing prices over time.
    - High Price Distribution: The distribution of high prices over time.
    """)

    with col2:
        st.pyplot(plot_graph(filtered_data, "Volume Over Time", 'Date', 'Volume', kind='bar', color='gray'))
        st.pyplot(plot_graph(filtered_data, "Price vs Volume (Scatter)", 'Volume', 'Close', kind='scatter', color='red'))
        st.pyplot(plot_graph(filtered_data, "High vs Low Price", 'High', 'Low', kind='scatter', color='blue'))
        st.pyplot(plot_graph(filtered_data, "Open vs Close Price", 'Open', 'Close', kind='scatter', color='green'))
        st.pyplot(plot_graph(filtered_data, "High Price Distribution", 'High', 'Volume', kind='scatter', color='orange'))

    # Additional Metrics to Complete 15 Graphs
    st.header(" :blue[Additional Metrics] :sunglasses:" )
    st.subheader(":green[Additional Stock Metrics and Visualizations]")
    st.write("""
    - Low Price Distribution: The distribution of low prices over time.
    - Close Price Moving Average: The moving average of the closing price over time.
    - Opening Price Histogram: The histogram of the opening price over time.
    - Closing Price Histogram: The histogram of the closing price over time.
    - Adj Close Price Histogram: The histogram of the adjusted closing price over time.
    - Volume Over Time (Bar Chart): The volume of shares traded over time.
    """)
    col3, col4, col5 = st.columns(3)
    
    with col3:
        st.pyplot(plot_graph(filtered_data, "Low Price Distribution", 'Low', 'Volume', kind='scatter', color='pink'))
        st.pyplot(plot_graph(filtered_data, "Close Price Moving Average", 'Date', 'Close', kind='line', color='blue'))

    with col4:
        st.pyplot(plot_graph(filtered_data, "Opening Price Histogram", 'Open', 'Volume', kind='bar', color='red'))
        st.pyplot(plot_graph(filtered_data, "Closing Price Histogram", 'Close', 'Volume', kind='bar', color='purple'))

    with col5:
        st.pyplot(plot_graph(filtered_data, "Adj Close Price Histogram", 'Adj Close', 'Volume', kind='bar', color='brown'))
        st.pyplot(plot_graph(filtered_data, "Volume Over Time (Bar Chart)", 'Date', 'Volume', kind='bar', color='cyan'))

if __name__ == "__main__":
    show_dashboard_page()
