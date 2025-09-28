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
    CSV files are stored under the data folder.
"""


from pathlib import Path
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import os
from src.config import *

# -----------------------------
# Relative path to CSV folder
# -----------------------------
try:
    current_file = Path(__file__).resolve()
    project_root = current_file.parent.parent
    DATA_DIR = project_root / "data" / "CSV"
    os.makedirs(DATA_DIR, exist_ok=True)
    print("Its running!")
    
except Exception as e:
    print(f"Error setting up data directory: {e}")




# -----------------------------
# Fetch historical data
# -----------------------------
def fetch_stock_data(ticker: str, start =START_DATE, end=END_DATE, save: bool=True) -> pd.DataFrame:
    """
    This function fetches historical stock data from Yahoo Finance for a given ticker symbol
    and saves it as a CSV file in the data/CSV directory. If the CSV file already exists,
    it updates the file with the latest data.

    Args:
        ticker (str): The stock ticker symbol (e.g., 'AAPL' for Apple Inc.).
        start (str): The start date for fetching historical data in 'YYYY-MM-DD' format.
        end (str): The end date for fetching historical data in 'YYYY-MM-DD' format.
        save (bool): If True, saves the fetched data to a CSV file. Default is True.
        

    Returns:
        pd.DataFrame: A DataFrame containing the historical stock data fetched from Yahoo Finance for the specified date range.
    
    Notes:
        - The function checks if a CSV file for the ticker already exists. If it does, it loads the existing data and fetches only new data from the last date in the existing file to avoid duplicates.
        - The function uses the yfinance library to fetch stock data.
        - The CSV files are stored in the data/CSV directory with filenames in the format '{ticker}.csv'.
        - If the fetched data contains a MultiIndex (which can happen with some yfinance queries), the function flattens the columns to a single level.
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
def fetch_latest_price(ticker: str, save: bool =True) -> float:
    """
    RThis function fetches the latest stock price for a given ticker symbol
    from Yahoo Finance and optionally saves it to a CSV file in the data/CSV directory.

    Args:
        ticker (str): The stock ticker symbol (e.g., 'AAPL' for Apple Inc.).
        save (bool): If True, saves the latest price to a CSV file. Default is True.
        

    Returns:
        float: The latest stock price fetched from Yahoo Finance.
    
    Notes:
        - The function uses the yfinance library to fetch the latest stock price.
        - The CSV file is stored in the data/CSV directory with the filename format '{ticker}_latest.csv'.
        - If the CSV file already exists, it appends the new price only if the date is not already present to avoid duplicates.
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
