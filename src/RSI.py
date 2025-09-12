import pandas as pd
import numpy as np
import timeit
import os

# Technical Indicator Functions


# Dont touch any RSI function pls
def calculate_RSI_1(df: pd.DataFrame):
    # Time Complexity O(n)
    # Space Complexity O(n)

    # Loop method
    for i in range(2,len(df)):
        current_close = float(df.iloc[i]['Close'])
        previous_close = float(df.iloc[i-1]['Close'])
        
        if current_close > previous_close:
            df.at[i, 'gain'] = current_close - previous_close
            df.at[i, 'loss'] = 0
        elif current_close < previous_close:
            df.at[i,'loss'] = previous_close - current_close
            df.at[i,'gain'] = 0
        else:
            df.at[i,'gain'] = 0
            df.at[i,'loss'] = 0

    # df['Close'][2:len(df)] = pd.to_numeric(df['Close'][2:len(df)], errors='coerce')
    # df['Change'] = df['Close'][2:len(df)].diff()
    # df['Gain'] = df['Change'][2:len(df)].clip(lower=0)
    # df['Loss'] = (-df['Change'][2:len(df)]).clip(lower=0)

    #print(df) 
    pass

def calculate_RSI2(df):
    df.loc[2:len(df),"Close"] = pd.to_numeric(df.loc[2:len(df),"Close"], errors='coerce')
    df['Change'] = df.loc[2:len(df),"Close"].diff()
    df['Gain'] = df.loc[2:len(df),"Close"].clip(lower=0)
    df['Loss'] = (-df.loc[2:len(df),"Close"]).clip(lower=0)

    #print(df) 

def calculate_EMA():
    pass

def calculate_MACD():
    pass

def calculate_VWAP():
    pass

# Other Functions

def Calculate_upward_and_Downward_runs():
    # Count of Total Occurrences.
    # How many individual upward movements happen
    # How many individual downward movements happen
    # Streaks/Runs analysis
    # Upward streak 2+ consecutive days. Same for downward streak
    # Longest streaks. Maximum number of consecutive days the price increased and decreased.
    # Utilize two pointers to calculate the longest streaks in each direction
    pass



# Testing my functions:
current_dir = os.getcwd()
file_path = os.path.join(current_dir,"src","CSV","AAPL.csv")
print(current_dir)

stock_df = pd.read_csv(file_path)
time1 = timeit.timeit(lambda: calculate_RSI_1(stock_df),number=10)
time2 = timeit.timeit(lambda: calculate_RSI2(stock_df),number=10)

print(f"Method 1 avg time: {time1/10:.6f} seconds")
print(f"Method 2 avg time: {time2/10:.6f} seconds")