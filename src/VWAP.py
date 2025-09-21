import pandas as pd
import numpy as np
import os



def calculate_VWAP(df):

    #Calculate Volume Weighted Average Price (VWAP).
    price = (df['High'] + df['Low'] + df['Close']) / 3
    total_vol = df['Volume'].cumsum()
    total_vol_price = (price * df['Volume']).cumsum()
    df['VWAP'] = total_vol_price / total_vol
    return df

# Testing the function
path = "C:/Users/joelo/OneDrive/Desktop/SIT/Year 1/INF1102 Programming/INF1002_Python_Project/src/CSV/AAPL.csv" 
data = pd.read_csv(path)
data = calculate_VWAP(data)

print(data[['Date', 'Close', 'VWAP']].head(10))

out_path = "C:/Users/joelo/OneDrive/Desktop/SIT/Year 1/INF1102 Programming/INF1002_Python_Project/src/CSV/AAPL_VWAP.csv"
data.to_csv(out_path, index=False)
print(f"\nVWAP results saved to {out_path}")