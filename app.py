"""
app.py

Purpose:
    This module is the main Streamlit application for visualizing stock data
    and technical indicators. It allows users to upload CSV files or enter stock and the stock data will be fetched using yfinance API.
    It also provides options to select date ranges, technical indicators, and display trade signals and trend highlights.
    The app uses plotly for interactive visualizations and a chart will be displayed based on user selections.

Functions:
    - None (main application script)
Notes:
    Each function modifies the input DataFrame in-place by adding new columns
    with the calculated indicator values.
"""



import streamlit as st
import pandas as pd
import yfinance as yf
from src.visualization import plot_visualization
from src.technical_indicators import *
from src.analytics import *
from src.config import *
from src.helper import *


# Set up Streamlit app
st.set_page_config( page_title="BullBearAnalysis",page_icon="📈",layout="wide")
st.title("BullBearAnalysis📈")
st.write("Welcome! To analyze stock data for bullish and bearish trends. You can upload a CSV file with stock data or enter a stock API to fetch data using the yfinance API")

# Option to upload CSV file
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

# Option to enter stock api
period_option_for_data = st.selectbox(
    "Period timeframe for Historical Data",
    PERIOD_SELECT_OPTIONS,
    index=5,
    placeholder="Select a period from the select box",

)
api = st.text_input('Enter Stock Ticker (for yfinance API)', '')



# Initialising data to hold csv file/api data
data = None

# # Check if a file or api was provided and load data to data_loader
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file, parse_dates=["Date"])
    data.set_index("Date", inplace=True)
    
    # Set date_range for the new stock.
    st.session_state["date_range"] = (data.index.min().date(), data.index.max().date())
    
    if verify_data_format(data):
        st.success("CSV uploaded successfully ✅")
    else:
        st.error("CSV format incorrect.")


elif api:
    # Fetch stock data using yfinance API if api is provided
    #data = yf.download(api, period="1y", interval="1d")
    data = yf.Ticker(api).history(period=period_option_for_data)
    # Clear session state date_range
    st.session_state["date_range"] = ""

    st.session_state["date_range"] = (data.index.min().date(), data.index.max().date())
    print('wait is this getting activated?')
    print(data)
    if data.empty:
        st.error(f"Could not fetch data for api: {api}")
    else: 
        pass
        
 # Display select field for type of chart       
type_of_chart_selected = st.sidebar.selectbox(
        "Select Chart Type",
        ("LineChart","CandleStick"),
                                         )








if data is not None and verify_data_format(data.reset_index()):
    
    if "date_range" not in st.session_state:
        st.session_state["date_range"] = (data.index.min().date(), data.index.max().date())
    
    
  
    

    
    st.sidebar.header("📅 Date Range Selection")
    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=st.session_state["date_range"],
        min_value=data.index.min().date(),
        max_value=data.index.max().date()
    )
    
    if len(date_range) == 2:
        st.session_state["date_range"] = date_range
    
    start_date , end_date = st.session_state["date_range"]
    data_filtered = filter_dataframe_by_date_range(data, start_date, end_date)
    
    
    # Default date will always be 1Y or 3Y
    # Filter the date here in the dataframe
    
    
    st.sidebar.header("📊 Indicators")
    
    indicators = []
    
    selected_technical_indicators = st.sidebar.multiselect(
        "Select your technical Indicators",
        TECHNICAL_INDICATOR_OPTIONS,
        max_selections=10
        )
    
    st.sidebar.subheader("Price Trend Highlights")
    show_upward_and_downward_trends = st.sidebar.checkbox("Show Upward and Downward Trends 📈", value=False)

    
    st.sidebar.subheader("Trade Signals")
    show_buy_signals = st.sidebar.checkbox("Show Buy Signals 🟢", value=False)
    show_sell_signals = st.sidebar.checkbox("Show Sell Signals 🔴", value=False)

        
    print(data.head(5))
    print(data.info())
    print("Before Data Processing")

    # Data processing ( Technical Indicators are applied to dataframe )
    df_processed = apply_selected_technical_indicators(data_filtered, selected_technical_indicators)
    
    
    # Implement trade signals and trend highlights here
    if show_upward_and_downward_trends:
        df_processed, longest_up_streak, longest_down_streak = calculate_upward_and_Downward_runs(df_processed)  
        column_to_display_upward_streak , column_to_display_downward_streak = st.columns(2)


        column_to_display_upward_streak.metric("📈 Longest Upward Streak", f"{longest_up_streak['length']}      days", f"From {longest_up_streak['start'].date()} to {longest_up_streak['end'].date()}", border=True)
        
        column_to_display_downward_streak.metric("📉 Longest Downward Streak", f"{longest_down_streak       ['length']} days", f"From {longest_down_streak['start'].date()} to {longest_down_streak['end'].date()}  ", border=True,delta_color='inverse')


    
    if show_buy_signals or show_sell_signals:
        df_processed, max_profit, num_buys = max_profit_calculation(df_processed)

        
        column_to_display_buy_and_sell, column_to_display_max_profit = st.columns(2)
        column_to_display_buy_and_sell.metric("Total Buy and Sell Signals", f"{num_buys}      buys", "", border=True)
        column_to_display_max_profit.metric("Maximum Theoretical Profit (No transaction fees)", f"${max_profit:.2f}", border=True)
        
        
    print(df_processed.head(5))
    print(df_processed.info())
    print(f"After data processed")
    
    
    stock_name = api if api else "Uploaded Data"
    fig = plot_visualization(df=df_processed, stock_name=stock_name, type_of_chart=type_of_chart_selected, indicators=selected_technical_indicators, show_buy_signals=show_buy_signals, show_sell_signals=show_sell_signals, show_upward_and_downward_trends=show_upward_and_downward_trends)
    st.plotly_chart(fig, use_container_width=True)

    
    
    
    
    
    # More UI elements to display analytics about the stock?
    

