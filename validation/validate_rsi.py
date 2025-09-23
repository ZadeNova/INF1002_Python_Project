import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"..")))

try:
    import yfinance as yf
    import pandas as pd
    import numpy as np
    import talib
    from ta import momentum
    from src.technical_indicators import *

except ImportError as e:
    print(f"Error: {e}")
    print("Please installed required packages")
    sys.exit(1)


def validate_rsi_against_library(historical_stock_data):
    print('Running RSI Validation')
    talab_library_calculated_RSI = talib.RSI(historical_stock_data['Close'],timeperiod=14)
    manually_calculated_RSI = calculate_RSI(historical_stock_data,14)
    
    
    compare_talab_and_manual = np.allclose(talab_library_calculated_RSI, manually_calculated_RSI['RSI'], rtol=1e-3, atol=1e-5,equal_nan=True)
    
    print(talab_library_calculated_RSI)
    print(manually_calculated_RSI)
    if compare_talab_and_manual:
        print("RSI Validation passed!")
    else:
        print("RSI Validation failed")


if __name__ == "__main__":
    current_dir = os.getcwd()
    file_path = os.path.join(current_dir,"src","CSV","META.csv")
    AAPL_data = pd.read_csv(file_path)
    validate_rsi_against_library(AAPL_data)