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
from src.technical_indicators import *
from src.data_loader import fetch_stock_data, fetch_latest_price
from src.config import *
#import ta-lib for accurate calculation
import talib
from functools import partial
#import tabulate for table format in terminal
from tabulate import tabulate


        
'''
    Validation Functions
'''
validation_results = []
#Data Validation for SMA (Comparing our SMA function with talib SMA function)
def validate_SMA_results(df: pd.DataFrame, window: int) -> pd.DataFrame:    
    """
    This function validates the Simple Moving Average (SMA) calculation
    by comparing the results from a custom implementation with those from the TA-Lib library.

    Args:
        df (pd.DataFrame): DataFrame containing stock data with necessary columns.
        period (int): The window size for calculating the SMA.

    Returns:
        pd.DataFrame: DataFrame with both custom and TA-Lib SMA columns for comparison.
        It also prints discrepancies to the console if any are found.
    
    Notes:
        - The function assumes that the input DataFrame contains a 'Close' column.
        - It fills NaN values with 0 for comparison purposes.
        - It uses a for loop to compare each row in the dataframe from both methods (TA-Lib and custom implementation).
        - Discrepancies between the two methods are printed to the console.
        
    """
    print("Running SMA Validation")
    
    #gets the SMA calcuted from our function
    df = calculate_SMA(df, window)

    #gets the SMA calculated from talib function
    df[f"SMA_{window}_talib"]= talib.SMA(df['Close'], timeperiod=window)

    df = df.fillna(0)
    #Compares each row from both methods for discrepancies
    for i in range(0, len(df[f"SMA_{window}"])):
        #compares the values from both methods
        if df[f"SMA_{window}"].iloc[i] != df[f"SMA_{window}_talib"].iloc[i]: 
        #if not np.isclose(df[f"SMA_{window}"].iloc[i],df[f"SMA_{window}_talib"].iloc[i]): #compared to the above, isclose() allows for tolerance (default up to 9dp)
            validation_results.append(["SMA","❌ Failed",f"SMA discrepancy at index {i}: calculated {df[f'SMA_{window}'].iloc[i]}, talib {df[f'SMA_{window}_talib'].iloc[i]}"])
            return None
        else:
            pass
    validation_results.append(["SMA", "✅ Passed", "Calculated values tally with Talib Values"])
    return df.replace(0, np.nan)

def validate_MACD_results(df: pd.DataFrame) -> pd.DataFrame:
    """
    This function validates the Moving Average Convergence Divergence (MACD) calculation
    by comparing the results from a custom implementation with those from the TA-Lib library.

    Args:
        df (pd.DataFrame): DataFrame containing stock data with necessary columns.
        

    Returns:
        pd.DataFrame: DataFrame with both custom and TA-Lib MACD columns for comparison.
        It also prints discrepancies to the console if any are found.
    
    Notes:
        - The function assumes that the input DataFrame contains a 'Close' column.
        - It fills NaN values with 0 for comparison purposes.
        - Discrepancies between the two methods are printed to the console.
        
    """
    print("Running MACD Validation")

    #gets MACD calculated from own function
    df = calculate_MACD(df)

    #calculate MACD using ta-lib
    df['MACD_talib'], df['MACD_signal_talib'], df['MACD_hist_talib'] = talib.MACD(df['Close'], 
                                                         fastperiod=12, 
                                                         slowperiod=26, 
                                                         signalperiod=9)
    df = df.fillna(0) #replace all NaN values with 0
    
    for i in range (0, len(df['MACD'])):
        if not np.isclose(df['MACD'].iloc[i],df['MACD_talib'].iloc[i]) and df['MACD'].iloc[i] == 0:
            validation_results.append(["MACD","❌ Failed",f"MACD Discrepancy at index {i}: calculated {df['MACD'].iloc[i]}, talib {df['MACD_talib'].iloc[i]}"])
            return None
        else:
            if not np.isclose(df['Signal_Line'].iloc[i],df['MACD_signal_talib'].iloc[i]):
                validation_results.append(["MACD","❌ Failed",f"MACD Signal Line Discrepancy at index {i}: calculated {df['Signal_Line'].iloc[i]}, talib {df['MACD_signal_talib'].iloc[i]}"])
                return None
            else:
                if not np.isclose(df['MACD_Histogram'].iloc[i],df['MACD_hist_talib'].iloc[i]):
                    validation_results.append(["MACD","❌ Failed",f"MACD Histogram Discrepancy at index {i}: calculated {df['MACD_Histogram'].iloc[i]}, talib {df['MACD_hist_talib'].iloc[i]}"])
                    return None
        
    validation_results.append(["MACD", "✅ Passed", "Calculated values tally with Talib Values"])
    return df.replace(0, np.nan)

def validate_EMA_results(df: pd.DataFrame, window: int) -> pd.DataFrame:  
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
    print("Running EMA Validation")

    #gets EMA calculated from our function
    calculate_EMA(df, window)

    #gets EMA calculated using talib
    df[f'EMA_{window}_talib'] = talib.EMA(df['Close'], timeperiod=window)

    #replace NaN values with 0
    df = df.fillna(0)
    #Compares each row from both methods for discrepancies
    for i in range(0, len(df[f'EMA_{window}'])):
        #compares the values from both methods
        if not np.isclose(df[f'EMA_{window}'].iloc[i],df[f'EMA_{window}_talib'].iloc[i]):
            validation_results.append(["EMA","❌ Failed",f"EMA discrepancy at index {i}: calculated {df[f'EMA_{window}'].iloc[i]}, talib {df[f'EMA_{window}_talib'].iloc[i]}"])
            return None
        else:
            pass
    validation_results.append(["EMA", "✅ Passed", "Calculated values tally with Talib Values"])
    return df.replace(0, np.nan)
    
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
    df = calculate_RSI(historical_stock_data,window)
    df["RSI_talib"] = talib.RSI(historical_stock_data['Close'],timeperiod=window)
    df.fillna(0)
    #compare_talab_and_manual = np.allclose(talab_library_calculated_RSI, df['RSI'], rtol=1e-3, atol=1e-5,equal_nan=True)
    
    df = df.fillna(0)
    #Compares each row from both methods for discrepancies
    for i in range(0, len(df[f"SMA_{window}"])):
        #compares the values from both methods
        if not np.isclose(df[f"RSI"].iloc[i],df[f"RSI_talib"].iloc[i]): 
            validation_results.append(["RSI","❌ Failed",f"SMA discrepancy at index {i}: calculated {df[f"RSI"].iloc[i]}, talib {df[f"RSI_talib"].iloc[i]}"])
            return None
        else:
            pass
    validation_results.append(["RSI", "✅ Passed", "Calculated values tally with Talib Values"])
    return df.replace(0, np.nan)
    #print(talab_library_calculated_RSI)
    ##print(df)
    '''
    if compare_talab_and_manual:
        validation_results.append(["RSI", "✅ Passed", "Calculated values tally with Talib Values"])
        return df.replace(0, np.nan)
    else:
        validation_results.append(["RSI", "❌ Failed", "Calculated values tally with Talib Values"])
        return None
    '''


# Example usage
"""
Run this validation.py file to validate the technical indicators calculations.
The custom technical indicators will be compared against TA-Lib's calculations.
The results will be printed to the console.
Make sure to adjust the stock symbol , date range, and window size as needed.

Additional Notes for next change:
- Give professor the command to run this validation file
- Display the data in a nicer way to the professor  ( might consider log file )
- Command is python -m validation.validation.py

"""
user_window = 14
# Please ensure you have an active internet connection to fetch the stock data, also ensure that the ticker is valid.
# Some examples of stock tickers: AAPL, MSFT, GOOGL, AMZN, TSLA, GME
stock_ticker = "AAPL"
# Date format is in YYYY-MM-DD
start_date = "2024-01-01"
end_date = "2025-09-01"
df = fetch_stock_data(stock_ticker, start_date, end_date)

validate_SMA_results(df, user_window)
validate_EMA_results(df, user_window)
validate_rsi_against_library(df, user_window)
validate_MACD_results(df)
print(tabulate(validation_results, headers=["Function", "Status", "Remarks"],tablefmt="double_grid"))
#df.to_csv("test.csv", index=False)