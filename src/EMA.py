import pandas as pd
import numpy as np
import os

# Technical Indicator Functions
def calculate_EMA(df: pd.DataFrame, period: int=12, column: str="Close", ema_col: str=None):
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


# Testing EMA functions:
current_dir = os.getcwd()
file_path = os.path.join(current_dir,"src","CSV","AAPL.csv")
print(current_dir)

stock_df = pd.read_csv(file_path)

# Add EMA columns
#stock_df = calculate_EMA(stock_df, period=12)
#stock_df = calculate_EMA(stock_df, period=26)

# Save back to CSV with 2 dp EMA
#stock_df.to_csv(file_path, index=False)

#print(stock_df.head(20))

