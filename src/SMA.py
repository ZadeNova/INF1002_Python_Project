# Simple Moving Average (SMA) calculation and data fetching 50, 100, 150, 200 days
import pandas as pd
import numpy as np
'''
from data_loader import fetch_stock_data, fetch_latest_price
import config

for tickers in config.TICKERS:
    df = fetch_stock_data(tickers, save=False)

#for tickers in config.TICKERS:
 #   latest_price = fetch_latest_price(tickers)

#tickers = input("Enter ticker symbol: ").upper()    
tickers = "AAPL" #just for testing
df = fetch_stock_data(tickers, save=False)
user_window = int(50) #just for testing

avg_prices = []
'''
# Our own SMA Calculator
def calculate_SMA_old(df: pd.DataFrame, user_window):
    avg_prices = []

    #starts from the first date
    slider = 0
    while slider+user_window <= len(df):
        window_average = df["Close"].iloc[slider:slider+user_window].sum() / user_window
        avg_prices.append(window_average)
        slider += 1
    return avg_prices
    
def calculate_SMA(df: pd.DataFrame, user_window):
    avg_prices = []

    #starts from the last date
    slider = len(df)
    while slider-user_window >= 0:
        window_average = df["Close"].iloc[slider-user_window:slider].sum() / user_window
        avg_prices.insert(0, window_average)
        slider -= 1
    return avg_prices


#SMA Calculator using Pandas
def calculate_SMA_pandas(df, window=50, column="Close"):
    df[f"SMA{window}"] = df[column].rolling(window=window).mean()
    return df
