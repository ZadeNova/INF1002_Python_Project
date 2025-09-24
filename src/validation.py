#Validating results from our functions with the results using functions from pandas
import pandas as pd
import numpy as np
#from analytics import EMA, MACD, RSI, SMA, VWAP
#from SMA import calculate_SMA
from MACD import calculate_MACD
from EMA import calculate_EMA
from RSI import calculate_RSI
from technical_indicators import calculate_SMA
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

    test_case = True
    
    #gets the SMA calcuted from our function
    df = calculate_SMA(df, user_window)

    #gets the SMA calculated from talib function
    df[f"SMA_{user_window}_talib"]= talib.SMA(df['Close'], timeperiod=user_window)

    df = df.fillna(0)

    #Compares each row from both methods for discrepancies
    for i in range(0, len(df[f"SMA_{user_window}"])):
        #compares the values from both methods
        if df[f"SMA_{user_window}"].iloc[i] != df[f"SMA_{user_window}_talib"].iloc[i]:
            print(f"SMA discrepancy at index {i}: calculated {df[f"SMA_{user_window}"].iloc[i]}, pandas {df[f"SMA_{user_window}_talib"].iloc[i]}")
            test_case = False
            return None
        else:
            pass
    if test_case:
        print("All test cases passed!")
        return df

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
            return None
        else:
            if df['Signal_Line'].iloc[i] != df['MACD_signal_talib'].iloc[i]:
                print(f"Signal Line Discrepancy at index {i}: calculated {df['Signal_Line'].iloc[i]}, talib {df['MACD_signal_talib'].iloc[i]}")
                test_case = False
                return None
            else:
                if df['MACD_Histogram'].iloc[i] != df['MACD_hist_talib'].iloc[i]:
                    print(f"Histogram Discrepancy at index {i}: calculated {df['MACD_Histogram'].iloc[i]}, talib {df['MACD_hist_talib'].iloc[i]}")
                    test_case = False
                    return None
        
    if test_case:
        print("All test cases passed!")
        return df

def validate_EMA_results(df, user_window):

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
            print(f"EMA discrepancy at index {i}: calculated {df['EMA12'].iloc[i]}, pandas {df['EMA_talib'].iloc[i]}")
            test_case = False
            return None
        else:
            pass
    if test_case:
        print("All test cases passed!")
        return df
    
def validate_rsi_against_library(historical_stock_data):
    print('Running RSI Validation')
    talab_library_calculated_RSI = talib.RSI(historical_stock_data['Close'],timeperiod=14)
    manually_calculated_RSI = calculate_RSI(historical_stock_data,14)
    
    
    compare_talab_and_manual = np.allclose(talab_library_calculated_RSI, manually_calculated_RSI['RSI'], rtol=1e-3, atol=1e-5,equal_nan=True)
    
    print(talab_library_calculated_RSI)
    print(manually_calculated_RSI)
    if compare_talab_and_manual:
        print("RSI Validation passed!")
        return df
    else:
        print("RSI Validation failed")
        return None
    

#validate_EMA(df, user_window)
validate_SMA_results(df, user_window)
#validate_MACD_results(df)
#df.to_csv("test.csv", index=False)