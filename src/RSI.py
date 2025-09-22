import pandas as pd
import numpy as np
import timeit
import os
import talib


# Technical Indicator Functions


# Dont touch any RSI function pls
def calculate_RSI(df: pd.DataFrame, time_period: int) -> pd.DataFrame:
    # Time Complexity O(n)
    # Space Complexity O(n)

    for i in range(1,len(df)):
        change = df.loc[i,'Close'] - df.loc[i-1,'Close']
        df.loc[i,'gain'] = max(change,0)
        df.loc[i,'loss'] = max(-change,0)
    
    # Calculate initial average gain and loss
    df.loc[time_period, 'avg_gain'] = df['gain'].iloc[1:time_period+1].sum() / time_period
    df.loc[time_period, 'avg_loss'] = df['loss'].iloc[1:time_period+1].sum() / time_period

    # Compute initial RS and RSI
    if df.loc[time_period, 'avg_loss'] != 0:
        df.loc[time_period, 'RS'] = df.loc[time_period, 'avg_gain'] / df.loc[time_period, 'avg_loss']
    else:
        df.loc[time_period, 'RS'] = 0
    df.loc[time_period, 'RSI'] = (100 - (100 / (1 + df.loc[time_period, 'RS'])))

    # Apply Wilder's smoothing for the rest of the days.
    for i in range(time_period+1, len(df)):
        prev_avg_gain = df.loc[i-1, 'avg_gain']
        prev_avg_loss = df.loc[i-1, 'avg_loss']

        gain = df.loc[i, 'gain']
        loss = df.loc[i, 'loss']

        avg_gain = ((prev_avg_gain * (time_period-1)) + gain ) / time_period
        avg_loss = ((prev_avg_loss * (time_period-1)) + loss ) / time_period

        df.loc[i, 'avg_gain'] = avg_gain
        df.loc[i, 'avg_loss'] = avg_loss

        rs = avg_gain / avg_loss if avg_loss != 0 else 0
        rsi = 100 - 100 / ( 1 + rs)

        df.loc[i, 'RS'] = rs
        df.loc[i, 'RSI'] = rsi
    
    return df

def calculate_RSI_new(df, window=14):
    price_change = df["Close"].diff()
    gain = (price_change.where(price_change > 0, 0)).rolling(window=window).mean()
    loss = (-price_change.where(price_change < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    df["RSI"] = 100 - (100 / (1 + rs))
    return df

# Other Functions

def sayHello_test():
    print(f"Hello there!")

# Testing my functions:
current_dir = os.getcwd()
file_path = os.path.join(current_dir,"src","CSV","AAPL.csv")
print(current_dir)

stock_df = pd.read_csv(file_path)
df = calculate_RSI(stock_df,14)
print(df)

