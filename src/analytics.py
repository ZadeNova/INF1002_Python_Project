"""
analytics.py

Purpose:
    This module contains functions for analyzing stock data, including calculating
    upward and downward trends, maximum profit calculations, and daily returns.

Functions:
    - calculate_upward_and_Downward_runs(df: pd.DataFrame) -> tuple[pd.DataFrame,dict,dict]
    - max_profit_calculation(df: pd.DataFrame) -> tuple[pd.DataFrame, float, int]
    - calculate_daily_returns(stock_dataframe: pd.DataFrame) -> dict

Notes:
    Each function modifies the input DataFrame in-place by adding new columns
    with the analysis results.
"""


import pandas as pd
import numpy as np
import timeit
import os
import talib
import yfinance as yf
from datetime import date , timedelta
from src.config import *
from src.ticker_utils import *



def calculate_upward_and_Downward_runs(df: pd.DataFrame) -> tuple[pd.DataFrame,dict,dict]:
    """
    This function calculates the upward and downward trends in stock prices.
    It identifies consecutive days of price increases (upward trends) and decreases (downward trends),
    and records the length and dates of these trends.

    Args:
        df (pd.DataFrame): DataFrame containing stock data with a 'Close' column.

    Returns:
        tuple: A tuple containing:
            - pd.DataFrame: The original DataFrame with additional columns for upward and downward trends.
            - dict: A dictionary with details of the longest upward trend (length, start date, end date).
            - dict: A dictionary with details of the longest downward trend (length, start date, end date).
    
    Notes:
        - The function adds two new columns to the DataFrame: 'Up_Trend' and 'Down_Trend',
          which indicate the length of the current upward or downward trend at each row.
        
    """

    
    df["Up_Trend"] = 0
    df["Down_Trend"] = 0
    up_streak = 0
    up_start_date = None
    down_streak = 0
    down_start_date = None
    longest_up = {"length": 0, "start": None, "end": None}
    longest_down = {"length": 0, "start": None, "end": None}
    for i in range(1, len(df)):
        if df["Close"].iloc[i] > df["Close"].iloc[i-1]:
            if up_streak == 0:
                up_start_date = df.index[i-1]
                
            up_streak += 1
            df.iloc[i, df.columns.get_loc("Up_Trend")] = up_streak
            
            # Update longest up streak if needed
            if up_streak > longest_up["length"]:
                longest_up["length"] = up_streak
                longest_up["start"] = up_start_date
                longest_up["end"] = df.index[i]
        else:
            up_streak = 0

        if df["Close"].iloc[i] < df["Close"].iloc[i-1]:
            if down_streak == 0:
                down_start_date = df.index[i-1]
                
            down_streak += 1
            df.iloc[i, df.columns.get_loc("Down_Trend")] = down_streak
            
            # Update longest down streak if needed
            if down_streak > longest_down["length"]:
                longest_down["length"] = down_streak
                longest_down["start"] = down_start_date
                longest_down["end"] = df.index[i]
        else:
            down_streak = 0
    
    
    return df, longest_up, longest_down


def max_profit_calculation(df: pd.DataFrame) -> tuple[pd.DataFrame, float, int]:
    """
    This function calculates the maximum theoretical profit that could be achieved
    by buying and selling stocks based on daily price movements. It uses a greedy algorithm. This function also counts the number of buy signals generated. 
    IMPORTANT: This function assumes that there are no transaction fees or taxes involved.

    Args:
        pd.DataFrame: DataFrame containing stock data with a 'Close' column.

    Returns:
        tuple: A tuple containing:
            - pd.DataFrame: The original DataFrame with additional columns for buy and sell signals.
            - float: The maximum theoretical profit that could be achieved.
            - int: The total number of buy signals generated.
    
    Notes:
        - The function adds two new columns to the DataFrame: 'Buy_Signal' and 'Sell_Signal',
          which indicate the days on which a buy or sell action would be taken.
        - The greedy algorithm buys on days when the price increases compared to the previous day
          and sells on the next day, accumulating profit from each transaction.
        - The function returns the total profit and the number of buy signals generated.
        
    """
    
    profit = 0
    
    df["Buy_Signal"] = False
    df["Sell_Signal"] = False
    
    for i in range(1, len(df)):
        if df["Close"].iloc[i] > df["Close"].iloc[i-1]:
            df.iloc[i-1, df.columns.get_loc("Buy_Signal")] = True
            df.iloc[i, df.columns.get_loc("Sell_Signal")] = True
            profit += df["Close"].iloc[i] - df["Close"].iloc[i-1]
    
    
    return df, profit , df["Buy_Signal"].sum()

#Calculate and display net worth for every stock holding and comparing to close stock price
def calculate_networth(stock_dataframe: pd.DataFrame):
    if stock_dataframe.empty:
        return {
            "table": stock_dataframe.copy(),
            "total_invested": 0.0,
            "total_current_value": 0.0,
            "profit_loss": 0.0,
            "profit_loss_pct": 0.0,
        }
    
    net_worth = stock_dataframe.copy()
    required = {"ticker", "price_per_share", "quantity"}
    missing = required - set(net_worth.columns)
    if missing:
        raise ValueError(f"Missing columns in stock_dataframe: {missing}")
    
    #Ensure types
    net_worth["ticker"] = net_worth["ticker"].astype(str).str.upper()
    net_worth["price_per_share"] = pd.to_numeric(net_worth["price_per_share"], errors="coerce")
    net_worth["quantity"] = pd.to_numeric(net_worth["quantity"], errors="coerce").fillna(0)

    #Total invested (what the user paid)
    net_worth["invested_value"] = net_worth["price_per_share"] * net_worth["quantity"]
    total_invested = float(net_worth["invested_value"].sum())

    #Pull latest close for each ticker
    ticker_list = net_worth["ticker"].tolist()
    d = date.today() - timedelta(days=5)
    


    # TEST THE UNKNOWN TICKERS . If user puts in unknown ticker
    ticker_currency  = categorize_tickers(tickers_list=ticker_list, exchange_map=EXCHANGE_MAP)
    
    prices_data = get_prices(tickers_list=ticker_list)
    print(ticker_currency)
    print('analytics.py')
    ticker_currency = resolve_unknown_currency(tickers_list=ticker_list, ticker_currency=ticker_currency)

    current_prices = get_prices_and_currency(tickers_list=ticker_list, ticker_prices=prices_data, ticker_currency=ticker_currency)
 
    
    
    
    current_prices = convert_current_prices_to_sgd(current_prices)

    net_worth["ticker"].map(lambda x: print(current_prices[x]['price_sgd']))
    net_worth["current_price_in_sgd"] = net_worth["ticker"].map(lambda x: current_prices[x]['price_sgd'])
    net_worth["current_invested_value_sgd"] = net_worth["current_price_in_sgd"] * net_worth["quantity"]
    
    
    
    net_worth["currency"] = net_worth["ticker"].map(lambda x: current_prices[x]["currency"])
    unique_currencies = net_worth["currency"].unique().tolist()
    
    fx_rates = get_fx_rates(unique_currencies, target_currency="SGD")
    
    net_worth = convert_invested_values(net_worth, fx_rates)
    

    total_current_value_in_SGD = float(net_worth["current_invested_value_sgd"].sum(skipna=True))
    total_invested_value_in_SGD = float(net_worth["invested_value_sgd"].sum(skipna=True))
    profit_loss_total_in_SGD = total_current_value_in_SGD - total_invested_value_in_SGD
    profit_loss_percentage = (profit_loss_total_in_SGD / total_invested_value_in_SGD) * 100.0

    

    return {
        "table": net_worth,
        "total_invested_value_in_sgd": total_invested_value_in_SGD,  # This is total invested has not been converted to currency sgd yet
        "total_current_value_in_sgd": total_current_value_in_SGD,
        "profit_loss": profit_loss_total_in_SGD,
        "profit_loss_percentage": profit_loss_percentage,
    }

def calculate_daily_returns(stock_dataframe: pd.DataFrame) -> dict:
    from src.ticker_utils import categorize_tickers, get_prices, resolve_unknown_currency, get_prices_and_currency, convert_current_prices_to_sgd
    import yfinance as yf
    from src.config import EXCHANGE_MAP
    try:
        if not stock_dataframe.empty:
            tickers = stock_dataframe['ticker'].tolist()
            #d = date(2025, 9, 22) 
            d = date.today() - timedelta(days=5)
            api_data = yf.download(tickers, start=d,interval="1d", group_by='ticker', threads=True)
            daily_returns = {}
            for ticker in tickers:
                try:
                    #Handle single vs multi-ticker frame
                    if isinstance(api_data.columns, pd.MultiIndex):
                        close = api_data[ticker]["Close"]
                    else:
                        close = api_data["Close"]

                    close = close.dropna()
                    if len(close) < 2:
                        daily_returns[ticker] = {"daily_return": None, "value": None}
                        continue

                    latest_close   = close.iloc[-1]
                    previous_close = close.iloc[-2]
                    daily_return = (latest_close - previous_close) / previous_close * 100
                    daily_returns[ticker] = {"daily_return": float(daily_return), "value": float(latest_close)}
                except Exception as e:
                    print(f"[calculate_daily_returns] {ticker}: {e!r}")
                    daily_returns[ticker] = {"daily_return": None, "value": None}
            # Step 2: Attach currency and convert to SGD
            ticker_currency = categorize_tickers(tickers_list=tickers, exchange_map=EXCHANGE_MAP)
            ticker_currency = resolve_unknown_currency(tickers_list=tickers, ticker_currency=ticker_currency)
            
            # Build price+currency dict to convert
            combined_data = {t: {"price": daily_returns[t]["value"], "currency": ticker_currency.get(t)} for t in tickers if t in daily_returns}
            sgd_converted = convert_current_prices_to_sgd(combined_data)

            # Step 3: Update with SGD values
            for ticker in tickers:
                if ticker in daily_returns and ticker in sgd_converted:
                    sgd_value = sgd_converted[ticker]["price_sgd"]
                    daily_returns[ticker]["value_sgd"] = sgd_value
                    daily_returns[ticker]["currency"] = "SGD"

    except Exception as e:
        print(f"Error occurred at calculate_daily_returns: {e}")

    return daily_returns
