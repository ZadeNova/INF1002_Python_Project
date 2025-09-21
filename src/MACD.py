from src.EMA import calculate_EMA
import pandas as pd
import numpy as np
import os

#For Calulating MACD, EMA function is needed as MACD uses EMA values
#MACD = EMA(12) - EMA(26), the histogram is MACD - Signal line(9 EMA of MACD), the signal line is used to identify buy/sell signals
#MACD > Signal line indicates bullish trend (prices trending upwards), MACD < Signal line indicates bearish trend(prices trending downwards)

def calculate_MACD(df: pd.DataFrame, short_period: int=12, long_period: int=26, signal_period: int=9, column: str="Close"):
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

def calculate_MACD_new(df, short=12, long=26, signal=9):
    df["EMA12"] = df["Close"].ewm(span=short, adjust=False).mean()
    df["EMA26"] = df["Close"].ewm(span=long, adjust=False).mean()
    df["MACD"] = df["EMA12"] - df["EMA26"]
    df["Signal"] = df["MACD"].ewm(span=signal, adjust=False).mean()
    return df

#Testing MACD functions:
current_dir = os.getcwd()
file_path = os.path.join(current_dir,"src","CSV","AAPL.csv")
stock_df = pd.read_csv(file_path)
stock_df = calculate_MACD(stock_df,12,26,9)
print(stock_df[["Date", "MACD", "Signal_Line", "MACD_Histogram"]].head(50))