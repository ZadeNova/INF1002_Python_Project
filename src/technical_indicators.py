"""
technical_indicators.py

Purpose:
    This module implements calculations for various technical indicators
    used in stock market analysis.

Functions:
    - calculate_RSI(df: pd.DataFrame, time_period: int) -> pd.DataFrame
    - calculate_SMA(df: pd.DataFrame, user_window: int) -> pd.DataFrame
    - calculate_EMA(df: pd.DataFrame, period: int, column: str="Close", ema_col: str=None) -> pd.DataFrame
    - calculate_MACD(df: pd.DataFrame, short_period: int=12, long_period: int=26, signal_period: int=9, column: str="Close") -> pd.DataFrame
    - calculate_VWAP(df: pd.DataFrame) -> pd.DataFrame
    - apply_selected_technical_indicators(df: pd.DataFrame, selected_indicators) -> pd.DataFrame    

Notes:
    Each function modifies the input DataFrame in-place by adding new columns
    with the calculated indicator values.
"""





import pandas as pd
import numpy as np
import timeit
import os
import talib
from functools import partial
from src.config import *



def calculate_RSI(df: pd.DataFrame, window: int) -> pd.DataFrame:

    """
    This function calculates the Relative Strength Index (RSI) for the given DataFrame. The DataFrame is modified in-place to include a new column 'RSI'.

    Args:
        df (pd.DataFrame): DataFrame containing stock data with necessary columns.
        time_period (int): The window size for calculating the RSI.

    Returns:
        pd.DataFrame: The modified DataFrame with a new column 'RSI'.
    
    Notes:
        - RSI is a momentum oscillator that measures the speed and change of price movements.
        - The function assumes that the input DataFrame has a 'Close' column.
        - The first (time_period) rows will have NaN values for the RSI since there is insufficient data to calculate the average gains and losses.
        - The function uses a sliding window approach to efficiently compute the RSI for each row.
        - This is O(n) implementation of RSI calculation cause it uses the sliding window approach.
        - The RSI values range from 0 to 100, with values above 70 indicating overbought conditions and values below 30 indicating oversold conditions.
        - The function uses the wilders smoothing method for calculating average gains and losses.
        
    """
    
    closes = list(df["Close"])
    
    price_change = []
    for i in range(1, len(closes)):
        price_change.append(closes[i] - closes[i-1])
    
    gains = []
    losses = []
    
    for change in price_change:
        if change > 0:
            gains.append(change)
            losses.append(0)
        else:
            gains.append(0)
            losses.append(-change)
            
    avg_gains = [None] * len(gains)
    avg_losses = [None] * len(losses)
    
    first_avg_gain = sum(gains[:window]) / window
    first_avg_loss = sum(losses[:window]) / window
    avg_gains[window-1] = first_avg_gain
    avg_losses[window-1] = first_avg_loss  
    
    
    for i in range(window, len(gains)):
        avg_gains[i] = ((avg_gains[i-1] * (window - 1)) + gains[i]) / window
        avg_losses[i] = ((avg_losses[i-1] * (window - 1)) + losses[i]) / window
    
    
    rsi_values = [None] * (len(closes))
    
    for i in range(len(avg_gains)):
        if avg_gains[i] is None or avg_losses[i] is None:
            continue
        if avg_losses[i] == 0:
            rs = float('inf')
        else:
            rs = avg_gains[i] / avg_losses[i]
        rsi_values[i+1] = 100 - (100 / (1 + rs))
    
    df['RSI'] = rsi_values

    
    return df
        



def calculate_EMA(df: pd.DataFrame, window, column: str="Close", ema_col: str=None) -> pd.DataFrame:
    
    """
    This function calculates the Exponential Moving Average (EMA) for the given DataFrame. The DataFrame is modified in-place to include a new column for the EMA values.

    Args:
        df (pd.DataFrame): DataFrame containing stock data with necessary columns.
        period (int): The window size for calculating the EMA.
        column (str, optional): The column name to calculate EMA on. Defaults to "Close

    Returns:
        od: pd.DataFrame: The modified DataFrame with a new column for the EMA values.
    
    Notes:
        - EMA gives more weight to recent prices, making it more responsive to new information.
        - The function assumes that the input DataFrame has the specified column.
        
    """
    
    if ema_col is None:
        ema_col = f"EMA_{window}"
    
    # Ensure numeric values
    df[column] = pd.to_numeric(df[column], errors="coerce")
    
    prices = df[column].tolist()
    ema_values = [None] * len(prices)
    
    # Step 1: first EMA = average of first 'window' prices
    first_ema = sum(prices[:window]) / window
    ema_values[window-1] = first_ema
    
    # Step 2: loop for remaining prices
    k = 2 / (window + 1)
    for i in range(window, len(prices)):
        prev_ema = ema_values[i-1]
        price = prices[i]
        ema_values[i] = (price - prev_ema) * k + prev_ema
    
    # Add raw EMA values to DataFrame
    df[ema_col] = ema_values
    
    # When saving, round to 2 decimals for cleaner CSV
    df[ema_col] = df[ema_col]
    
    return df



def calculate_SMA(df: pd.DataFrame, window: int) -> pd.DataFrame:
    
    """
    This function calculates the Simple Moving Average (SMA) for the given DataFrame. The DataFrame is modified in-place to include a new column 'SMA_{user_window}'.

    Args:
        df (pd.DataFrame): DataFrame containing stock data with necessary columns.
        user_window (int): The window size for calculating the SMA.

    Returns:
        pd.DataFrame: The modified DataFrame with a new column 'SMA_{user_window}'.
    
    Notes:
        - SMA is calculated as the average of the closing prices over the specified window.
        - The function assumes that the input DataFrame has a 'Close' column.
        - The first (user_window - 1) rows will have NaN values for the SMA since there is insufficient data to calculate the average.
        - The function uses a sliding window approach to efficiently compute the SMA for each row.
        
    """
    
    avg_prices = []

    #starts from the last date
    slider = len(df)
    #while slider-user_window >= 0:
    #    window_average = df["Close"].iloc[slider-user_window:slider].sum() / user_window
    #    avg_prices.insert(0, window_average)
    #    slider -= 1
    #    
    
    for i in range(len(df)):
        if i + 1 < window:
            avg_prices.append(None)
        else:
            window_average = (df['Close'].iloc[i+1-window: i+1]).sum() / window
            #print(window_average,'testing22334')
            avg_prices.append(window_average)
    
    column_name = f"SMA_{window}"
    df[column_name] = avg_prices
    print(df)
    print('testing123')
    return df



def calculate_VWAP(df: pd.DataFrame) -> pd.DataFrame:
    """
    This function calculates the Volume Weighted Average Price (VWAP) for the given DataFrame. The DataFrame is modified in-place to include a new column 'VWAP'.

    Args:
        df (pd.DataFrame): DataFrame containing stock data with necessary columns.

    Returns:
        pd.DataFrame: The modified DataFrame with a new column 'VWAP'.
    
    Notes:
        - VWAP is calculated using the formula: VWAP = (Cumulative Price * Volume) / Cumulative Volume
        - The function assumes that the input DataFrame has the necessary columns: 'High', 'Low', 'Close', and 'Volume'.
        - The function uses cumulative sums to efficiently compute VWAP for each row.
        
    """
    #Calculate Volume Weighted Average Price (VWAP).
    price = (df['High'] + df['Low'] + df['Close']) / 3
    total_vol = df['Volume'].cumsum()
    total_vol_price = (price * df['Volume']).cumsum()
    df['VWAP'] = total_vol_price / total_vol
    return df


def calculate_MACD(df: pd.DataFrame, short_period: int=12, long_period: int=26, signal_period: int=9, column: str="Close") -> pd.DataFrame:
    """
    This function calculates the Moving Average Convergence Divergence (MACD) for the given DataFrame. The DataFrame is modified in-place to include new columns 'MACD', 'Signal_Line', and 'MACD_Histogram'.

    Args:
        df (pd.DataFrame): DataFrame containing stock data with necessary columns.
        short_period (int, optional): The short-term EMA period. Defaults to 12.
        long_period (int, optional): The long-term EMA period. Defaults to 26.
        signal_period (int, optional): The signal line EMA period. Defaults to 9.
        column (str, optional): The column name to calculate MACD on. Defaults to "Close".

    Returns:
        pd.DataFrame: The modified DataFrame with new columns 'MACD', 'Signal_Line', and 'MACD_Histogram'.
    
    Notes:
        - MACD is a trend-following momentum indicator that shows the relationship between two moving averages of a security's price.
        - The function assumes that the input DataFrame has the specified column.
        - The MACD line is calculated as the difference between the short-term and long-term EMAs.
        - The signal line is the EMA of the MACD line.
        
    """
    #Ensure numeric values in close column
    df[column] = pd.to_numeric(df[column], errors="coerce")
    
    #Calculate short-term and long-term EMAs
    df = calculate_EMA(df, window=short_period, column=column, ema_col=f"EMA_{short_period}")
    df = calculate_EMA(df, window=long_period, column=column, ema_col=f"EMA_{long_period}")
    
    #Calculate MACD line
    df["MACD"] = df[f"EMA_{short_period}"] - df[f"EMA_{long_period}"]
    
    #Calculate Signal line
    #df= calculate_EMA(df, period=signal_period, column="MACD", ema_col="Signal_Line")
    df["Signal_Line"] = (pd.Series(df["MACD"].to_numpy(), index=df.index).ewm(span=signal_period, adjust=False, min_periods=signal_period).mean())
    
    #Calculate MACD Histogram
    df["MACD_Histogram"] = df["MACD"] - df["Signal_Line"]
    
    #Round values to 2 decimal places for cleaner display
    df["MACD"] = df["MACD"]
    df["Signal_Line"] = df["Signal_Line"]
    df["MACD_Histogram"] = df["MACD_Histogram"]

    return df