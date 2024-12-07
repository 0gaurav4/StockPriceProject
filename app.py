import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title='stock data analysis')
st.sidebar.header("Stock Data Analysis")
st.sidebar.image("up.png",width=100)

def load_data():
    df = pd.read_csv('stocks.csv', parse_dates=['Date'])
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Calculate VWAP
    df['VWAP'] = (df['Volume'] * (df['High'] + df['Low'] + df['Close']) / 3).cumsum() / df['Volume'].cumsum()
    
    # Calculate Trade (difference between Close and Open prices)
    df['Trades'] = df['Close'] - df['Open']
    
    # Calculate Turnover if 'Trades' column is present
    if 'Trades' in df.columns:
        df['Turnover'] = (df['Volume'] * df['Trades']).astype(int)
    else:
        df['Turnover'] = None  # Set to None or 0 if 'Trades' is not available

    return df



def home(title):
    df = load_data()
    st.title("Stock data Analysis")
    st.image('image.png',width=400)
    st.write(" ")
    st.header("Raw dataset")
    st.write(" ")
    st.write(df.head(10))
    st.markdown("<hr>", unsafe_allow_html= True)
    col1, col2 = st.columns(2)
    col1.subheader("Number of Rows:")
    col1.write(df.shape[0])
    col2.subheader("Number of Columns:")
    col2.write(df.shape[1])
    st.markdown("<hr>", unsafe_allow_html= True)
    st.write(" ")
    st.header("Dataset Summary")
    st.write(" ")
    st.write(df.describe(include='number'))

    st.header("Columns description")
    for i in df.columns:
        st.subheader(i)
        col1, col2 = st.columns(2)
        col1.caption("Unique Values")
        col1.write(len(df[i].unique()))
        col2.caption("Type of Data")
        col2.write("String of Characters" if type(df[i].iloc[0]) is str else "Numerical")
        st.markdown("<hr>",unsafe_allow_html = True)



def page1(title):
    df = load_data()
    st.title(title)

    # Sidebar for selecting a single stock
    stock = st.sidebar.selectbox("Choose a stock for analysis:", list(df.Ticker.unique()))

    # Sidebar for selecting the date range (default: start to end of data)
    start_date = min(df['Date'])
    end_date = max(df['Date'])
    selected_date_range = st.sidebar.date_input("Select Date Range:", 
                                                [start_date, end_date],
                                                min_value=start_date, max_value=end_date)

    # Ensure that the selected_date_range is a list with two dates (start and end)
    if isinstance(selected_date_range, tuple) and len(selected_date_range) == 2:
        start_date_selected, end_date_selected = selected_date_range
    else:
        st.warning("Please select a valid start and end date for the date range.")
        return

    # Check if only one date is selected
    if start_date_selected == end_date_selected:
        st.warning("Please select a date range (start and end date must be different).")
        return

    # Filter data for the selected stock and date range
    selected_stock_data = df[(df['Ticker'] == stock) & 
                             (df['Date'] >= pd.to_datetime(start_date_selected)) & 
                             (df['Date'] <= pd.to_datetime(end_date_selected))]

    # If the user selects a stock
    if len(selected_stock_data) > 0:
        st.success(f"Analyzing stock: **{stock}** from **{start_date_selected}** to **{end_date_selected}**")

        # Description of stock analysis
        st.write("""
        A stock represents ownership in a company. When you purchase a stock, you own a piece of the company, and your investment's value fluctuates with the company's performance.
        - **Close Price**: The closing price of the stock on a given day : :blue[the last price of the day].
        - **VWAP**: The volume-weighted average price of the stock on a given day : :blue[Volume * (High + Low + Close) / 3]. 
        - **Trades**: The number of trades that occurred on a given day : :blue[Close - Open].
        - **Volume**: The volume of trades that occurred on a given day : :blue[Number of shares traded].
        - **Turnover**: The product of Volume and Trades : :blue[Volume * Trades].
        """)

        # Close price line graph
        st.header("Close Price Line Graph")
        st.plotly_chart(px.line(selected_stock_data, 'Date', 'Close', title="Close Price Over Time"))

        # Candlestick plot
        st.header("Candlestick Plot")
        st.plotly_chart(go.Figure(data=[go.Candlestick(x=selected_stock_data['Date'],
                                                      open=selected_stock_data['Open'],
                                                      high=selected_stock_data['High'],
                                                      low=selected_stock_data['Low'],
                                                      close=selected_stock_data['Close'])]))

        # High price histogram
        st.header("High Price Histogram")
        st.plotly_chart(px.histogram(selected_stock_data, x='Date', y='High', title="High Price Distribution"))

        # VWAP over time
        st.header('VWAP Over Time')
        fig = go.Figure([go.Scatter(x=selected_stock_data['Date'], y=selected_stock_data['VWAP'])])
        fig.update_xaxes(title="Date")
        fig.update_yaxes(title="VWAP")
        st.plotly_chart(fig)

        # Trades over time
        st.header("Trades Over Time")
        st.plotly_chart(px.scatter(selected_stock_data, 'Date', 'Trades', title="Trades Over Time"))

        # Volume over time
        st.header("Volume Over Time")
        st.plotly_chart(px.line(selected_stock_data, 'Date', 'Volume', title="Volume Over Time"))

        # Turnover over time
        st.header("Turnover Over Time")
        st.plotly_chart(px.scatter(selected_stock_data, 'Date', 'Turnover', title="Turnover Over Time"))
    
    else:
        st.warning("No data available for the selected stock and date range.")





def page2(title):
    data = load_data()
    st.title(title)

    # Sidebar for selecting multiple stocks
    selected_stocks = st.sidebar.multiselect("Choose stocks for comparison:-", list(data.Ticker.unique()))

    # Sidebar for selecting the date range (default: start to end of data)
    start_date = min(data['Date'])
    end_date = max(data['Date'])
    selected_date_range = st.sidebar.date_input("Select Date Range:", 
                                               [start_date, end_date], 
                                               min_value=start_date, max_value=end_date)

    # If the user selects stocks
    if len(selected_stocks) > 0:
        st.success(f"Comparing stocks: **{', '.join(selected_stocks)}** from **{selected_date_range[0]}** to **{selected_date_range[1]}**")

        # Description of stock comparison
        st.write("""
        Stock comparison allows you to analyze and compare the performance of the selected stocks based on key metrics. 
        You can compare factors such as Close Price, VWAP, Trades, Volume, and Turnover across the chosen stocks.
       - **Close Price**: The closing price of the stock on a given day : :blue[the last price of the day].
        - **VWAP**: The volume-weighted average price of the stock on a given day : :blue[Volume * (High + Low + Close) / 3]. 
        - **Trades**: The number of trades that occurred on a given day : :blue[Close - Open].
        - **Volume**: The volume of trades that occurred on a given day : :blue[Number of shares traded].
        - **Turnover**: The product of Volume and Trades : :blue[Volume * Trades].       
        """)

        # Filter data for the selected stocks and date range
        filtered_data = data[(data['Ticker'].isin(selected_stocks)) & 
                              (data['Date'] >= pd.to_datetime(selected_date_range[0])) & 
                              (data['Date'] <= pd.to_datetime(selected_date_range[1]))]

        # Close price comparison for selected stocks
        st.header("Close Price Comparison")
        close_data = filtered_data.groupby(['Ticker', 'Date'])['Close'].last().reset_index()
        st.plotly_chart(px.line(close_data, x='Date', y='Close', color='Ticker', title="Close Price for Selected Stocks"))

        # VWAP comparison for selected stocks
        st.header("VWAP Comparison")
        vwap_data = filtered_data.groupby(['Ticker', 'Date'])['VWAP'].last().reset_index()
        st.plotly_chart(px.line(vwap_data, x='Date', y='VWAP', color='Ticker', title="VWAP for Selected Stocks"))

        # Trades comparison for selected stocks
        st.header("Trades Comparison")
        trades_data = filtered_data.groupby(['Ticker', 'Date'])['Trades'].last().reset_index()
        st.plotly_chart(px.line(trades_data, x='Date', y='Trades', color='Ticker', title="Trades for Selected Stocks"))

        # Volume comparison for selected stocks
        st.header("Volume Comparison")
        volume_data = filtered_data.groupby(['Ticker', 'Date'])['Volume'].sum().reset_index()
        st.plotly_chart(px.line(volume_data, x='Date', y='Volume', color='Ticker', title="Volume for Selected Stocks"))

        # Turnover comparison for selected stocks
        st.header("Turnover Comparison")
        turnover_data = filtered_data.groupby(['Ticker', 'Date'])['Turnover'].sum().reset_index()
        st.plotly_chart(px.line(turnover_data, x='Date', y='Turnover', color='Ticker', title="Turnover for Selected Stocks"))


    else:
        st.warning("Please select at least one stock to compare.")


pages = {'Introduction':home,'Analysing a single stock':page1,'Comparison between Stocks':page2}
page = st.sidebar.selectbox('Choose a page:-',list(pages.keys()))

pages[page](page)