"""
run_loader.py

Purpose:
    This module is responsible for running the data loading functions to fetch and update stock data.

Functions:
    Functions are from the data_loader module

Notes:
    It uses functions from the data_loader module to fetch historical stock data and the latest prices.
"""



from data_loader import fetch_stock_data, fetch_latest_price
import config

# Incrementally update historical data for all tickers
for ticker in config.TICKERS:
    df = fetch_stock_data(ticker)
    print(f"{ticker} now has {len(df)} rows")

# Update latest prices
for ticker in config.TICKERS:
    price = fetch_latest_price(ticker)
    print(f"{ticker} latest price: {price}")
