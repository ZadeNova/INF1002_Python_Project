import pandas as pd
import numpy as np
import timeit
import os
import talib
from functools import partial
from src.config import *

# File to combine the 5 technical indicators here


def calculate_RSI(df: pd.DataFrame, time_period: int) -> pd.DataFrame:
    ## Time Complexity O(n)
    ## Space Complexity O(n)
    #df = df.copy()
    ## Calculate daily gains and losses
    #df['Change'] = df['Close'].diff()
    #df['Gain'] = df['Change'].apply(lambda x: max(x, 0))
    #df['Loss'] = df['Change'].apply(lambda x: max(-x, 0))
    #
    ## Initialize average gain and loss
    #df['Avg_Gain'] = 0
    #df['Avg_Loss'] = 0
    #
    #df.at[time_period, 'Avg_Gain'] = df['Gain'].iloc[1:time_period+1].mean()
    #df.at[time_period, 'Avg_Loss'] = df['Gain'].iloc[1:time_period+1].mean()
    #
    ## 3 Calculate RSI for the first calculation day
    #df['RS'] = 0.0
    #df['RSI'] = 0.0
    #
    #df.at[time_period, 'RS'] = df.at[time_period, 'Avg_Gain'] / df.at[time_period, #'Avg_Loss'] if df.at[time_period, 'Avg_Loss'] != 0 else 0
    #df.at[time_period, 'RSI'] = 100 - 100 / ( 1 + df.at[time_period, 'RS'])
    #
    #
    #print(df)
    #print("whatrs going on here")
    #
    ## 4 Calculate RSI using wilder's smoothing for subsequent days
    #df_idx = df.index
    #for i in range(time_period + 1, len(df)):
    #    prev_avg_gain = df.at[i-1, 'Avg_Gain']
    #    prev_avg_loss = df.at[i-1, 'Avg_Loss']
    #    
    #    #gain = df.at[i, 'Gain']
    #    gain = df.loc[df_idx[i], 'Gain']
    #    loss = df.loc[df_idx[i], 'Loss']
    #    
    #    avg_gain = (prev_avg_gain * (time_period - 1) + gain) / time_period
    #    avg_loss = (prev_avg_loss * (time_period - 1) + loss) / time_period
    #    
    #    df.at[i, 'Avg_Gain'] = avg_gain
    #    df.at[i, 'Avg_Loss'] = avg_loss
    #    
    #    rs = avg_gain / avg_loss if avg_loss != 0 else 0
    #    rsi = 100 - 100 / (1 + rs)
    #    
    #    df.at[i, 'RS'] = rs
    #    df.at[i, 'RSI'] = rsi
    #    
    ## Set rsi for first period to none
    #df.loc[df.index[:time_period], 'RSI'] = None
    #
    #
    ## Clean up dataframe columns
    #df = df.drop(columns=['Change','Gain','Loss','Avg_Gain','Avg_Loss','RS'])
    #
    #return df
    
    # USE library first then settle the RSI function when I have time 
    price_change = df["Close"].diff()
    gain = (price_change.where(price_change > 0, 0)).rolling(window=time_period).mean()
    loss = (-price_change.where(price_change < 0, 0)).rolling(window=time_period).mean()
    rs = gain / loss
    df["RSI"] = 100 - (100 / (1 + rs))
    
    return df
        



def calculate_EMA(df: pd.DataFrame, period: int=12, column: str="Close", ema_col: str=None) -> pd.DataFrame:
    if ema_col is None:
        ema_col = f"EMA{period}"
    
    # Ensure numeric values
    df[column] = pd.to_numeric(df[column], errors="coerce")
    
    prices = df[column].tolist()
    ema_values = [None] * len(prices)
    
    # Step 1: first EMA = average of first 'period' prices
    first_ema = sum(prices[:period]) / period
    ema_values[period-1] = first_ema
    
    # Step 2: loop for remaining prices
    k = 2 / (period + 1)
    for i in range(period, len(prices)):
        prev_ema = ema_values[i-1]
        price = prices[i]
        ema_values[i] = (price - prev_ema) * k + prev_ema
    
    # Add raw EMA values to DataFrame
    df[ema_col] = ema_values
    
    # When saving, round to 2 decimals for cleaner CSV
    df[ema_col] = df[ema_col].round(2)
    
    return df



def calculate_SMA(df: pd.DataFrame, user_window: int):
    avg_prices = []

    #starts from the last date
    slider = len(df)
    #while slider-user_window >= 0:
    #    window_average = df["Close"].iloc[slider-user_window:slider].sum() / user_window
    #    avg_prices.insert(0, window_average)
    #    slider -= 1
    #    
    
    for i in range(len(df)):
        if i + 1 < user_window:
            avg_prices.append(None)
        else:
            window_average = (df['Close'].iloc[i+1-user_window: i+1]).sum() / user_window
            #print(window_average,'testing22334')
            avg_prices.append(window_average)
    
    column_name = f"SMA_{user_window}"
    df[column_name] = avg_prices
    print(df)
    print('testing123')
    return df



def calculate_VWAP(df: pd.DataFrame) -> pd.DataFrame:

    #Calculate Volume Weighted Average Price (VWAP).
    price = (df['High'] + df['Low'] + df['Close']) / 3
    total_vol = df['Volume'].cumsum()
    total_vol_price = (price * df['Volume']).cumsum()
    df['VWAP'] = total_vol_price / total_vol
    return df


def calculate_MACD(df: pd.DataFrame, short_period: int=12, long_period: int=26, signal_period: int=9, column: str="Close") -> pd.DataFrame:
    #Ensure numeric values in close column
    df[column] = pd.to_numeric(df[column], errors="coerce")
    
    #Calculate short-term and long-term EMAs
    df = calculate_EMA(df, period=short_period, column=column, ema_col=f"EMA_{short_period}")
    df = calculate_EMA(df, period=long_period, column=column, ema_col=f"EMA_{long_period}")
    
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


def apply_selected_technical_indicators(df: pd.DataFrame, selected_indicators):
    """
    Applies a specific list of technical indicator functions to the dataframe
    
    
    Returns:
    pd.DataFrame with the new indicator columns added.
    """
    df_with_indicators = df.copy()
    # Loop through the user's selection and apply the corresponding function
    print(selected_indicators)
    
    for indicator_func in selected_indicators:
        print(indicator_func)
        indicator_function = TECHNICAL_INDICATORS[indicator_func]
        
        df_with_indicators = indicator_function(df_with_indicators)
    
    #print(type(df_with_indicators))
    #print(df_with_indicators)
    #print(df_with_indicators[:10:50])
    return df_with_indicators
        

TECHNICAL_INDICATORS = {
    SMA_20_LABEL: partial(calculate_SMA, user_window=20),
    SMA_50_LABEL: partial(calculate_SMA, user_window=50),
    SMA_200_LABEL: partial(calculate_SMA, user_window=200),
    RSI_14_LABEL: partial(calculate_RSI, time_period=14),
    MACD: partial(calculate_MACD, short_period=12, long_period=26, signal_period=9, column="Close"),
    VWAP: partial(calculate_VWAP),
    EMA: partial(calculate_EMA),
}