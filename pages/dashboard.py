import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_data():
    # Load the dataset (replace with your actual dataset path)
    data = pd.read_csv("stocks.csv")  # Replace with actual dataset
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

    # st.write(f"Showing data for {selected_ticker} from {date_range[0]} to {date_range[1]} with volume above {volume_filter}")

    # Generate 15 different graphs
    st.header("Stock Price and Volume Analysis")

    col1, col2 = st.columns(2)
    with col1:
        st.pyplot(plot_graph(filtered_data, "Close Price Over Time", 'Date', 'Close', kind='line', color='green'))
        st.pyplot(plot_graph(filtered_data, "Open Price Over Time", 'Date', 'Open', kind='line', color='blue'))
        st.pyplot(plot_graph(filtered_data, "High Price Over Time", 'Date', 'High', kind='line', color='orange'))
        st.pyplot(plot_graph(filtered_data, "Low Price Over Time", 'Date', 'Low', kind='line', color='red'))
        st.pyplot(plot_graph(filtered_data, "Adj Close Price Over Time", 'Date', 'Adj Close', kind='line', color='purple'))

    with col2:
        st.pyplot(plot_graph(filtered_data, "Volume Over Time", 'Date', 'Volume', kind='bar', color='gray'))
        st.pyplot(plot_graph(filtered_data, "Price vs Volume (Scatter)", 'Volume', 'Close', kind='scatter', color='red'))
        st.pyplot(plot_graph(filtered_data, "High vs Low Price", 'High', 'Low', kind='scatter', color='blue'))
        st.pyplot(plot_graph(filtered_data, "Open vs Close Price", 'Open', 'Close', kind='scatter', color='green'))
        st.pyplot(plot_graph(filtered_data, "High Price Distribution", 'High', 'Volume', kind='scatter', color='orange'))

    # Additional graphs to complete 15
    st.header("Additional Metrics")

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
