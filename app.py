import streamlit as st
import pandas as pd
import yfinance as yf
from src.visualization import plot_visualization
from src.technical_indicators import *
from src.config import *


# Set up Streamlit app
st.set_page_config( page_title="BullBearAnalysis",page_icon="📈",layout="wide")
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

# # Check if a file or api was provided and load data to data_loader
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file, parse_dates=["Date"])
    data.set_index("Date", inplace=True)
    if verify_data_format(data):
        st.success("CSV uploaded successfully ✅")
    else:
        st.error("CSV format incorrect.")


elif api:
    # Fetch stock data using yfinance API if api is provided
    #data = yf.download(api, period="1y", interval="1d")
    data = yf.Ticker(api).history(period="1y")
    print('wait is this getting activated?')
    print(data)
    if data.empty:
        st.error(f"Could not fetch data for api: {api}")
    else:
        st.write("blah blah")
        #run data visualizations and analytics
        
        
 # Display select field for type of chart       
type_of_chart_selected = st.sidebar.selectbox(
        "Select Chart Type",
        ("LineChart","CandleStick"),
                                         )

# Option to select technical indicators
if data is not None and verify_data_format(data.reset_index()):
    
    
    
    
    
    
    st.sidebar.header("📊 Indicators")
    
    indicators = []
    
    selected_technical_indicators = st.sidebar.multiselect(
        "Select your technical Indicators",
        TECHNICAL_INDICATOR_OPTIONS,
        max_selections=5
        )
    

        
    print(data.head(5))
    print(data.info())
    print("Before Data Processing")

    # We will compute the calculations based on what TA user chose into the dataframe. DO NOT CALCULATE ALL DAtaframe.
    
    # Data processing ( Technical Indicators are applied to dataframe )
    df_processed = apply_selected_technical_indicators(data, selected_technical_indicators)
    
    
    print(df_processed.info())
    print(f"After data processed")
    #print(f"CHART SELECTOR {type_of_chart_selected} {selected_technical_indicators}")
    stock_name = api if api else "Uploaded Data"
    fig = plot_visualization(df=df_processed, stock_name=stock_name, type_of_chart=type_of_chart_selected, indicators=selected_technical_indicators)
    st.plotly_chart(fig, use_container_width=True)


