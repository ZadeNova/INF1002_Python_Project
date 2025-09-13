# Simple Moving Average (SMA) calculation and data fetching 50, 100, 150, 200 days
import pandas as pd
import numpy as np
from data_loader import fetch_stock_data, fetch_latest_price
import config

# Our own SMA Calculator
def calculate_SMA(df: pd.DataFrame, user_window):
    avg_prices = []

    #starts from the first date
    slider = 0
    while slider+user_window <= len(df):
        window_average = df["Close"].iloc[slider:slider+user_window].sum() / user_window
        avg_prices.append(window_average)
        slider += 1
    return avg_prices
    


#SMA Calculator using Pandas
def calculate_SMA_pandas(df: pd.DataFrame, user_window):
    df['SMA_50'] = df['Close'].rolling(window=user_window).mean()
    return df

