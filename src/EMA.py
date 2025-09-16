import pandas as pd
import numpy as np
import timeit
import os

# Technical Indicator Functions
def calculate_EMA(df: pd.DataFrame, period: int=12, column: str="Close", ema_col: str=None):
    # Time Complexity O(n)
    # Space Complexity O(n)
    
    if ema_col is None:
        ema_col = f"EMA_{period}"
    
    df[column] = pd.to_numeric(df[column], errors="coerce")
    
    # Smoothing factor
    k = 2 / (period + 1)
    
    # Initialize EMA column with NaN
    df[ema_col] = np.nan
    
    # First EMA = SMA of first `period` values
    df.loc[period-1, ema_col] = df.loc[:period-1, column].mean()
    
    # Loop calculation
    for i in range(period, len(df)):
        price = df.loc[i, column]
        prev_ema = df.loc[i-1, ema_col]
        df.loc[i, ema_col] = (price - prev_ema) * k + prev_ema
    
    return df


# Testing EMA functions:
current_dir = os.getcwd()
file_path = os.path.join(current_dir,"src","CSV","AAPL.csv")
print(current_dir)

stock_df = pd.read_csv(file_path)
time1 = timeit.timeit(lambda: calculate_EMA(stock_df),number=10)

print(f"Method 1 avg time: {time1/10:.6f} seconds")
