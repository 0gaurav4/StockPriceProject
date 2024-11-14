import streamlit as st
import pandas as pd

def load_data():
    df = pd.read_csv(r'stocks.csv', parse_dates=['Date'])
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Calculate VWAP
    df['VWAP'] = (df['Volume'] * (df['High'] + df['Low'] + df['Close']) / 3).cumsum() / df['Volume'].cumsum()
    
    # Calculate Trade (difference between Close and Open prices)
    df['Trade'] = df['Close'] - df['Open']
    
    # Calculate Turnover if 'Trades' column is present
    if 'Trades' in df.columns:
        df['Turnover'] = (df['Volume'] * df['Trades']).astype(int)
    else:
        df['Turnover'] = None

    return df

def show_home_page():
    st.title("Welcome to the Stock Market Dashboard")
    st.markdown("""
    This dashboard allows you to explore and analyze stock market data, 
    filter by ticker, date, and volume, and gain insights into the performance 
    of various stocks.
    
    **Features:**
    - 15 Interactive Data Visualizations
    - Filter by Ticker, Date, and Volume
    - Overview of key stock metrics
    """)
    st.image('https://i.pinimg.com/originals/2e/e6/99/2ee6998e34c3e2eff7b894c66cfc5267.jpg', use_column_width=True)


    st.title("📈 Stock Data Overview")

    df = load_data()
    st.header("Interactive Data Exploration")
    st.write("Use the filters below to explore specific data points:")

    # Interactive filters for exploring specific data
    ticker = st.selectbox("Select Ticker", df['Ticker'].unique())
    start_date = st.date_input("Start Date", df['Date'].min())
    end_date = st.date_input("End Date", df['Date'].max())

    filtered_data = df[(df['Ticker'] == ticker) & (df['Date'] >= pd.to_datetime(start_date)) & (df['Date'] <= pd.to_datetime(end_date))]
    st.write(filtered_data)


if __name__ == "__main__":
    show_home_page()
