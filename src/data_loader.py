"""
data_loader.py

Purpose:
    This module handles data fetching from Yahoo Finance and saving it locally as CSV files.

Functions:
    - fetch_stock_data(ticker: str, start: str, end: str, save: bool=True) -> pd.DataFrame
    - fetch_latest_price(ticker: str, save: bool=True) -> float


Notes:
    Each function interacts with the yfinance library to retrieve stock data and
    saves it in a structured format for further analysis.
"""


# data_loader.py
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import os
from src.config import *

# -----------------------------
# Relative path to CSV folder
# -----------------------------
DATA_DIR = os.path.join(os.path.dirname(__file__), "CSV")
os.makedirs(DATA_DIR, exist_ok=True)

# -----------------------------
# Fetch historical data
# -----------------------------
def fetch_stock_data(ticker: str, start =START_DATE, end=END_DATE, save: bool=True):
    """
    Fetch stock data from Yahoo Finance and incrementally update the CSV.
    """
    filename = os.path.join(DATA_DIR, f"{ticker}.csv")
    
    # If CSV exists, load it and update only from the last date
    if os.path.exists(filename):
        existing = pd.read_csv(filename, parse_dates=["Date"])
        last_date = existing["Date"].max()
        new_start = (last_date + timedelta(days=1)).strftime("%Y-%m-%d")
    else:
        existing = pd.DataFrame()
        new_start = start

    # Only fetch if we need new data
    if new_start <= end:
        new_data = yf.download(ticker, start=new_start, end=end, progress=False)
        if isinstance(new_data.columns, pd.MultiIndex):
            ## remove the header from csv file
            new_data.columns = [col[0] for col in new_data.columns] 
        new_data.reset_index(inplace=True)
    else:
        new_data = pd.DataFrame()

    # Merge old + new data
    if not new_data.empty:
        combined = pd.concat([existing, new_data], ignore_index=True)
    else:
        combined = existing

    if save and not combined.empty:
        combined.to_csv(filename, index=False)
        print(f"✅ {ticker} data updated in {filename}")

    return combined

# -----------------------------
# Fetch latest price
# -----------------------------
def fetch_latest_price(ticker: str, save: bool =True):
    """
    Fetch the latest market price and append to a _latest.csv file.
    """
    stock = yf.Ticker(ticker)
    todays_data = stock.history(period="1d")
    latest_price = todays_data["Close"][0]

    if save:
        filename = os.path.join(DATA_DIR, f"{ticker}_latest.csv")
        today = datetime.today().strftime("%Y-%m-%d")
        row = pd.DataFrame([[today, latest_price]], columns=["Date","Close"])
        
        if os.path.exists(filename):
            existing = pd.read_csv(filename)
            if today not in existing["Date"].values:
                row.to_csv(filename, mode="a", header=False, index=False)
        else:
            row.to_csv(filename, index=False)
        
        print(f"✅ Latest {ticker} price saved to {filename}")

    return latest_price
