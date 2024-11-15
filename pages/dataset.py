import streamlit as st
import pandas as pd

def load_data():
    df = pd.read_csv(r'stocks.csv', parse_dates=['Date'])
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Calculate VWAP
    df['VWAP'] = (df['Volume'] * (df['High'] + df['Low'] + df['Close']) / 3).cumsum() / df['Volume'].cumsum()
    
    # Calculate Trade (difference between Close and Open prices)
    df['Trade'] = df['Close'] - df['Open']  # Renamed to 'Trade' to avoid overwriting 'Trades'
    
    # Calculate Turnover if 'Trades' column is present
    if 'Trade' in df.columns:
        df['Turnover'] = (df['Volume'] * df['Trade']).astype(int)
    else:
        df['Turnover'] = None  # Set to None or 0 if 'Trades' is not available

    return df

def show_dataset_page():
    st.title("Dataset Overview")
    
    df = load_data()

    st.subheader(":green[Here is a quick overview of the dataset:]")
    st.write(df.head())

    st.subheader(":green[**Basic Statistics**]")
    st.write(df.describe())
    
    st.subheader(":green[**Column Information**]")
    st.write("""
    - `Ticker`: Stock symbol
    - `Date`: Date of the stock data
    - `Open`: Opening price
    - `High`: Highest price during the day
    - `Low`: Lowest price during the day
    - `Close`: Closing price
    - `Adj Close`: Adjusted closing price
    - `Volume`: Number of shares traded
    - `VWAP`: Volume-weighted average price
    - `Trade`: Difference between Close and Open prices
    - `Turnover`: Product of Volume and Trades (if Trades data is available)
    """)

    st.subheader(":green[**Full Dataset**]")
    st.write(df)

# Call show_dataset_page to display the page in Streamlit
if __name__ == "__main__":
    show_dataset_page()
