import streamlit as st

def show_about_page():
    st.title("About This Project")
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

    st.header("How to Use This App")
    st.write("""
    - **Home Page**: Explore recent entries in the dataset, key statistics, and filter data by ticker and date range.
    - **About Page**: Learn about the dataset and key metrics calculated within this app.
    """)

    st.header("Setup Instructions")

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

