#Validating results from our functions with the results using functions from pandas
import pandas as pd
import numpy as np
#from analytics import EMA, MACD, RSI, SMA, VWAP
from SMA import calculate_SMA, calculate_SMA_pandas
#from data_loader import 
from data_loader import fetch_stock_data, fetch_latest_price
import config

for tickers in config.TICKERS:
    df = fetch_stock_data(tickers, save=False)

for tickers in config.TICKERS:
    latest_price = fetch_latest_price(tickers)

#tickers = input("Enter ticker symbol: ").upper()    
tickers = "AAPL" #just for testing
df = fetch_stock_data(tickers, save=False)
user_window = int(50) #just for testing


#Data Validation for SMA (Comparing our SMA function with Pandas SMA function)
def validate_results(df, user_window):

    #gets the SMA calcuted from our function
    avg_prices = calculate_SMA(df, user_window)

    #gets the SMA calculated from pandas function
    pandas_avg_prices = calculate_SMA_pandas(df, user_window)['SMA_50'].dropna() #Remove NaN values for comparison
    test_case = "Passed"

    #Compares each row from both methods for discrepancies
    for i in range(0, len(avg_prices)):
        #compares the values from both methods rounded to 5 decimal places
        if round(avg_prices[i],5) != round(pandas_avg_prices.iloc[i],5):
            print(f"Discrepancy at index {i}: calculated {avg_prices[i]}, pandas {pandas_avg_prices.iloc[i]}")
            test_case = "Failed"
            break
        else:
            pass
    if test_case != "Failed":
        print("All test cases passed!")

validate_results(df, user_window)