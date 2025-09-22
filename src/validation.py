#Validating results from our functions with the results using functions from pandas
import pandas as pd
import numpy as np
#from analytics import EMA, MACD, RSI, SMA, VWAP
from SMA import calculate_SMA, calculate_SMA_talib
from MACD import calculate_MACD
from EMA import calculate_EMA
#from data_loader import 
from data_loader import fetch_stock_data, fetch_latest_price
import config
#import ta-lib for accurate calculation
import talib 

for tickers in config.TICKERS:
    df = fetch_stock_data(tickers, save=False)

#for tickers in config.TICKERS:
#    latest_price = fetch_latest_price(tickers)

#tickers = input("Enter ticker symbol: ").upper()    
tickers = "AMZN" #just for testing
df = fetch_stock_data(tickers, save=False)
user_window = int(50) #just for testing


#Data Validation for SMA (Comparing our SMA function with talib SMA function)
def validate_SMA_results(df, user_window):

    #gets the SMA calcuted from our function
    avg_prices = calculate_SMA(df, user_window)

    #gets the SMA calculated from talib function
    pandas_avg_prices = calculate_SMA_talib(df, user_window)[f'SMA_{user_window}'].dropna() #Remove NaN values for comparison
    test_case = True

    #Compares each row from both methods for discrepancies
    for i in range(0, len(avg_prices)):
        #compares the values from both methods
        if avg_prices [i] != pandas_avg_prices.iloc[i]:
            print(f"Discrepancy at index {i}: calculated {avg_prices[i]}, pandas {pandas_avg_prices.iloc[i]}")
            test_case = False
            break
        else:
            pass
    if test_case:
        print("All test cases passed!")

def validate_MACD_results(df):

    test_case = True

    #gets MACD calculated from own function
    df = calculate_MACD(df)

    #calculate MACD using ta-lib
    df['MACD_talib'], df['MACD_signal_talib'], df['MACD_hist_talib'] = talib.MACD(df['Close'], 
                                                         fastperiod=12, 
                                                         slowperiod=26, 
                                                         signalperiod=9)
    df = df.fillna(0) #replace all NaN values with 0
    print(df.iloc[33])
    
    for i in range (0, len(df['MACD'])):
        if df['MACD'].iloc[i] != df['MACD_talib'].iloc[i] and df['MACD'].iloc[i] == 0:
            print(f"MACD Discrepancy at index {i}: calculated {df['MACD'].iloc[i]}, talib {df['MACD_talib'].iloc[i]}")
            test_case = False
            break
        else:
            if df['Signal_Line'].iloc[i] != df['MACD_signal_talib'].iloc[i]:
                print(f"Signal Line Discrepancy at index {i}: calculated {df['Signal_Line'].iloc[i]}, talib {df['MACD_signal_talib'].iloc[i]}")
                test_case = False
                break
            else:
                if df['MACD_Histogram'].iloc[i] != df['MACD_hist_talib'].iloc[i]:
                    print(f"Histogram Discrepancy at index {i}: calculated {df['MACD_Histogram'].iloc[i]}, talib {df['MACD_hist_talib'].iloc[i]}")
                    test_case = False
                    break
        
    if test_case:
        print("All test cases passed!")

def validate_EMA(df, user_window):

    test_case = True

    #gets EMA calculated from our function
    calculate_EMA(df)

    #gets EMA calculated using talib
    df['EMA_talib'] = talib.EMA(df['Close'], timeperiod=12)

    #replace NaN values with 0
    df = df.fillna(0)

    #Compares each row from both methods for discrepancies
    for i in range(0, len(df['EMA12'])):
        #compares the values from both methods
        if df['EMA12'].iloc[i] != df['EMA_talib'].iloc[i]:
            print(f"Discrepancy at index {i}: calculated {df['EMA12'].iloc[i]}, pandas {df['EMA_talib'].iloc[i]}")
            test_case = False
            break
        else:
            pass
    if test_case:
        print("All test cases passed!")

    

#validate_EMA(df, user_window)
#validate_SMA_results(df, user_window)
#validate_MACD_results(df)
#df.to_csv("test.csv", index=False)