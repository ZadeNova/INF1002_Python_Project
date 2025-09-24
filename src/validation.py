"""
validation.py

Purpose:
    This module implements validation functions to ensure the correctness
    of technical indicator calculations by comparing them against established libraries such as TA-Lib.

Functions:
    - validate_SMA_results(df: pd.DataFrame, user_window: int) -> pd.DataFrame
    - validate_MACD_results(df: pd.DataFrame) -> pd.DataFrame
    - validate_EMA_results(df: pd.DataFrame, user_window: int) -> pd.DataFrame
    - validate_rsi_against_library(historical_stock_data: pd.DataFrame) -> pd.DataFrame

Notes:
    Each function compares the results of custom implemented technical indicators functions with those from TA-Lib for validation purposes.
"""




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
def validate_SMA_results(df: pd.DataFrame, user_window: int) -> pd.DataFrame:    
    """
    This function validates the Simple Moving Average (SMA) calculation
    by comparing the results from a custom implementation with those from the TA-Lib library.

    Args:
        df (pd.DataFrame): DataFrame containing stock data with necessary columns.
        user_window (int): The window size for calculating the SMA.

    Returns:
        pd.DataFrame: DataFrame with both custom and TA-Lib SMA columns for comparison.
    
    Notes:
        - The function assumes that the input DataFrame contains a 'Close' column.
        - It fills NaN values with 0 for comparison purposes.
        - Discrepancies between the two methods are printed to the console.
        
    """

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

def validate_MACD_results(df: pd.DataFrame) -> pd.DataFrame:
    """
    This function validates the Moving Average Convergence Divergence (MACD) calculation
    by comparing the results from a custom implementation with those from the TA-Lib library.

    Args:
        df (pd.DataFrame): DataFrame containing stock data with necessary columns.
        

    Returns:
        pd.DataFrame: DataFrame with both custom and TA-Lib MACD columns for comparison.
    
    Notes:
        - The function assumes that the input DataFrame contains a 'Close' column.
        - It fills NaN values with 0 for comparison purposes.
        - Discrepancies between the two methods are printed to the console.
        
    """

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

def validate_EMA_results(df: pd.DataFrame, user_window: int) -> pd.DataFrame:  
    """
    This function validates the Exponential Moving Average (EMA) calculation
    by comparing the results from a custom implementation with those from the TA-Lib library.

    Args:
        df (pd.DataFrame): DataFrame containing stock data with necessary columns.
        user_window (int): The window size for calculating the EMA.

    Returns:
        pd.DataFrame: DataFrame with both custom and TA-Lib EMA columns for comparison.
    
    Notes:
        - The function assumes that the input DataFrame contains a 'Close' column.
        - It fills NaN values with 0 for comparison purposes.
        - Discrepancies between the two methods are printed to the console.
        
    """

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
    
def validate_rsi_against_library(historical_stock_data: pd.DataFrame, window: int) -> pd.DataFrame:
    """
    This function validates the Relative Strength Index (RSI) calculation
    by comparing the results from a custom implementation with those from the TA-Lib library.

    Args:
        historical_stock_data (pd.DataFrame): DataFrame containing stock data with necessary columns.
        window (int): The window size for calculating the RSI.
    
    Returns:
        pd.DataFrame: DataFrame with both custom and TA-Lib RSI columns for comparison.
    
    Notes:
        - The function assumes that the input DataFrame contains a 'Close' column.
        - It fills NaN values with 0 for comparison purposes.
        - Discrepancies between the two methods are printed to the console.
        
    """
    print('Running RSI Validation')
    talab_library_calculated_RSI = talib.RSI(historical_stock_data['Close'],timeperiod=window)
    manually_calculated_RSI = calculate_RSI(historical_stock_data,window)
    
    
    compare_talab_and_manual = np.allclose(talab_library_calculated_RSI, manually_calculated_RSI['RSI'], rtol=1e-3, atol=1e-5,equal_nan=True)
    
    print(talab_library_calculated_RSI)
    print(manually_calculated_RSI)
    if compare_talab_and_manual:
        print("RSI Validation passed!")
        return df
    else:
        print("RSI Validation failed")
        return None
    

#validate_rsi_against_library(df, 14)
#validate_EMA(df, user_window)
validate_SMA_results(df, user_window)
#validate_MACD_results(df)
#df.to_csv("test.csv", index=False)