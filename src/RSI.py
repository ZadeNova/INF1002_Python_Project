import pandas as pd
import numpy as np
import timeit
import os
import talib

# Technical Indicator Functions


# Dont touch any RSI function pls
def calculate_RSI(df: pd.DataFrame,N) -> pd.DataFrame:
    # Time Complexity O(n)
    # Space Complexity O(n)

    for i in range(1,len(df)):
        change = df.loc[i,'Close'] - df.loc[i-1,'Close']
        df.loc[i,'gain'] = max(change,0)
        df.loc[i,'loss'] = max(-change,0)
    
    # Calculate initial average gain and loss
    df.loc[N, 'avg_gain'] = df['gain'].iloc[1:N+1].sum() / N
    df.loc[N, 'avg_loss'] = df['loss'].iloc[1:N+1].sum() / N

    # Compute initial RS and RSI
    if df.loc[N, 'avg_loss'] != 0:
        df.loc[N, 'RS'] = df.loc[N, 'avg_gain'] / df.loc[N, 'avg_loss']
    else:
        df.loc[N, 'RS'] = 0
    df.loc[N, 'RSI'] = (100 - (100 / (1 + df.loc[N, 'RS'])))

    # Apply Wilder's smoothing for the rest of the days.
    for i in range(N+1, len(df)):
        prev_avg_gain = df.loc[i-1, 'avg_gain']
        prev_avg_loss = df.loc[i-1, 'avg_loss']

        gain = df.loc[i, 'gain']
        loss = df.loc[i, 'loss']

        avg_gain = ((prev_avg_gain * (N-1)) + gain ) / N
        avg_loss = ((prev_avg_loss * (N-1)) + loss ) / N

        df.loc[i, 'avg_gain'] = avg_gain
        df.loc[i, 'avg_loss'] = avg_loss

        rs = avg_gain / avg_loss if avg_loss != 0 else 0
        rsi = 100 - 100 / ( 1 + rs)

        df.loc[i, 'RS'] = rs
        df.loc[i, 'RSI'] = rsi
    
    return df

    #print(df)
    

    # This is the way to validate RSI
    # closing_prices = df['Close'].values
    # rsi = talib.RSI(closing_prices, timeperiod=14)
    # df['RSI2'] = rsi



# Other Functions



# Testing my functions:
current_dir = os.getcwd()
file_path = os.path.join(current_dir,"src","CSV","AAPL.csv")
print(current_dir)

stock_df = pd.read_csv(file_path)
calculate_RSI(stock_df,14)
