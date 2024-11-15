import streamlit as st

def show_about_page():
    st.title(":blue[About This Project]")
    st.markdown("""
    This dashboard is designed to help users interactively explore stock market data.
    You can filter data by ticker, date, and volume to understand stock performance.
    
    **Technologies Used:**
    - Python
    - Streamlit
    - Pandas for data manipulation
    - Matplotlib & Seaborn for visualizations
    
    **Author**: Anu Tiwari
    """)

    st.header(":blue[How to Use This App]")
    st.write("""
    - **Main Page**: Navigate to different sections like stock analysis, comparisons, and visualizations.
- **Home Page**: View and analyze the raw dataset, along with key statistics and column details.
- **Dashboard Page**: A comprehensive dashboard displaying various interactive visualizations for stock performance.
- **Dataset Page**: View detailed information about the dataset, including basic statistics, columns, and raw data.
- **About Page**: Learn about the app's features, its purpose, and how the stock data is processed and analyzed.
    """)

    st.header(":green[Setup Instructions]")

    st.subheader("1. Install Requirements")
    st.write("""
    In your terminal, navigate to the project directory where your `requirements.txt` file is located, then run:
    ```
    pip install -r requirements.txt
    ```
    This will install all the necessary packages.
    """)

    st.subheader("2. Run the App")
    st.write("""
    After installing the requirements, start the app with this command:
    ```
    streamlit run app.py
    ```
    Open the URL displayed in the terminal (usually `http://localhost:8501`) to access the app in your browser.
    """)

# Display about page content
if __name__ == "__main__":
    show_about_page()

