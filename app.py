import streamlit as st
import pandas as pd
import yfinance as yf

# Set up Streamlit app
st.set_page_config(
    page_title="BullBearAnalysis",
    page_icon="📈",
    layout="wide"
)
st.title("BullBearAnalysis📈")
st.write("Welcome! To analyze stock data for bullish and bearish trends. You can upload a CSV file with stock data or enter a stock API to fetch data using the yfinance API")

# Option to upload CSV file
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

# Option to enter stock api
api = st.text_input('Enter Stock API (for yfinance API)', '')

# Function to verify if data is in correct format
def verify_data_format(data):
    required_columns = ['Date', 'Close', 'High', 'Low', 'Open', 'Volume']
    for col in required_columns:
        if col in data.columns:
            return True
    return False

# Initialising data to hold csv file/api data
data = None

# Check if a file or api was provided and load data to data_loader
if uploaded_file is not None:
    # Read CSV data if uploaded
    data = pd.read_csv(uploaded_file)
    if not verify_data_format(data): # check if csv file is in correct format
        st.error("CSV file is not in the correct format. Please ensure it contains the required columns: Date, Close, High, Low, Open, Volume")
    else:
        st.write("blah blah")
        #run data visualizations and analytics

elif api:
    # Fetch stock data using yfinance API if api is provided
    data = yf.download(api, period="1y", interval="1d")
    if data.empty:
        st.error(f"Could not fetch data for api: {api}")
    else:
        st.write("blah blah")
        #run data visualizations and analytics


# Option to select technical indicators
if data is not None and verify_data_format(data):
    indicators = []

    if st.checkbox('Moving Average (50 & 200)', value=True):
        indicators.append('SMA')

    if st.checkbox('Relative Strength Index (RSI)', value=True):
        indicators.append('RSI')

    if st.checkbox('MACD', value=True):
        indicators.append('MACD')

    if st.checkbox('Exponential Moving Average (EMA)', value=True):
        indicators.append('EMA')

    if st.checkbox('VWAP', value=True):
        indicators.append('VWAP')