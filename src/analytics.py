import pandas as pd
import numpy as np
import timeit
import os
import talib
import yfinance as yf
from datetime import date

#for tickers in config.TICKERS:
    #df = fetch_stock_data(tickers, save=False)

#for tickers in config.TICKERS:
    #latest_price = fetch_latest_price(tickers)

#tickers = "AAPL" #just for testing
#df = fetch_stock_data(tickers, save=False)

#maybe switch to dictionary, dates as keys, prices as values
up_trend_list = [] #stores length of each upward trend
down_trend_list = [] #stores length of each downward trend
up_trend_dates = [] #stores start and end date of each upward trend
down_trend_dates = [] #stores start and end date of each downward trend

def calculate_upward_and_Downward_runs(df: pd.DataFrame) -> tuple[pd.DataFrame,dict,dict]:

    #Counter for number of consecutive up and down days
    #up_streak_counter = 0
    #down_streak_counter = 0
#
    ##Counter for the longest streak in each direction
    #highest_up_streak = 0
    #highest_down_streak = 0
    #highest_up_streak_dates = ""
    #highest_down_streak_dates = ""
#
    #start_date = df['Date'].iloc[0]
#
    ##Iterate through each day and compare with previous day
    #for i in range(1, len(df)) :
#
    #    #if stock price went up compared to previous day, increment up counter
    #    if df['Close'].iloc[i] >= df['Close'].iloc[i-1]:
    #        #if there was a down counter before this, means up streak is lesser than 2 days, reset counter
    #        if down_streak_counter == 1:
    #            down_streak_counter = 0
    #            #reset start date to previous day
    #            start_date = df['Date'].iloc[i-1]
    #        up_streak_counter += 1
#
    #    #if stock price went down compared to previous day, increment down counter    
    #    elif df['Close'].iloc[i] <= df['Close'].iloc[i-1]:
    #        #if there was an up counter before this, means down streak is lesser than 2 days, reset counter
    #        if up_streak_counter == 1:
    #            up_streak_counter = 0
    #            #reset start date to previous day
    #            start_date = df['Date'].iloc[i-1]
    #        down_streak_counter += 1
#
    #    #Check if a up streak lasts for min 2 consecutive days before recording it
    #    if up_streak_counter >= 2 and down_streak_counter == 1:
    #        up_trend_list.append(up_streak_counter)
    #        end_date = df['Date'].iloc[i-1]
    #        up_trend_dates.append(str(start_date) + " to " + str(end_date))
#
    #        #Check if this is the longest up streak so far
    #        if up_streak_counter > highest_up_streak:
    #            highest_up_streak = up_streak_counter
    #            highest_up_streak_dates = str(start_date) + " to " + str(end_date)
#
    #        start_date = end_date
    #        up_streak_counter = 0
#
    #    #Check if a down streak lasts for min 2 consecutive days before recording it
    #    elif down_streak_counter >=2  and up_streak_counter == 1:
    #        down_trend_list.append(down_streak_counter)
    #        end_date = df['Date'].iloc[i-1]
    #        down_trend_dates.append(str(start_date) + " to " + str(end_date))
#
    #        #Check if this is the longest up streak so far
    #        if down_streak_counter > highest_down_streak:
    #            highest_down_streak = down_streak_counter
    #            highest_down_streak_dates = str(start_date) + " to " + str(end_date)
#
    #        start_date = end_date
    #        down_streak_counter = 0
#
    #    else:
    #        pass
    #print("Longest Upward Trend: " + str(highest_up_streak) + " days from " + str(highest_up_streak_dates))
    #print("Longest Downward Trend: " + str(highest_down_streak) + " days from " + str(highest_down_streak_dates))
    
    df["Up_Trend"] = 0
    df["Down_Trend"] = 0
    up_streak = 0
    up_start_date = None
    down_streak = 0
    down_start_date = None
    longest_up = {"length": 0, "start": None, "end": None}
    longest_down = {"length": 0, "start": None, "end": None}
    for i in range(1, len(df)):
        if df["Close"].iloc[i] > df["Close"].iloc[i-1]:
            if up_streak == 0:
                up_start_date = df.index[i-1]
                
            up_streak += 1
            df.iloc[i, df.columns.get_loc("Up_Trend")] = up_streak
            
            # Update longest up streak if needed
            if up_streak > longest_up["length"]:
                longest_up["length"] = up_streak
                longest_up["start"] = up_start_date
                longest_up["end"] = df.index[i]
        else:
            up_streak = 0

        if df["Close"].iloc[i] < df["Close"].iloc[i-1]:
            if down_streak == 0:
                down_start_date = df.index[i-1]
                
            down_streak += 1
            df.iloc[i, df.columns.get_loc("Down_Trend")] = down_streak
            
            # Update longest down streak if needed
            if down_streak > longest_down["length"]:
                longest_down["length"] = down_streak
                longest_down["start"] = down_start_date
                longest_down["end"] = df.index[i]
        else:
            down_streak = 0
    
    
    return df, longest_up, longest_down


def max_profit_calculation(df: pd.DataFrame) -> tuple[pd.DataFrame, float]:
    
    profit = 0
    
    df["Buy_Signal"] = False
    df["Sell_Signal"] = False
    
    for i in range(1, len(df)):
        if df["Close"].iloc[i] > df["Close"].iloc[i-1]:
            df.iloc[i-1, df.columns.get_loc("Buy_Signal")] = True
            df.iloc[i, df.columns.get_loc("Sell_Signal")] = True
            profit += df["Close"].iloc[i] - df["Close"].iloc[i-1]
    
    #print(df["Buy_Signal"].head(15))
    #print(df["Sell_Signal"].tail(15))
    
    return df, profit

    


def calculate_daily_returns(stock_dataframe: pd.DataFrame):
    if not stock_dataframe.empty:
        tickers = stock_dataframe['ticker'].tolist()
        import yfinance as yf
        d = date(2025, 9, 22) 
        #api_data = yf.download(tickers, start = "2025-09-22", end = "2025-09-22" ,interval="1d", group_by='ticker', threads=True)
        api_data = yf.download(tickers, start=d, interval="1d", group_by='ticker', threads=True)
        print(api_data)
        daily_returns = {}
        for ticker in tickers:
            try:
                if len(tickers) == 1:
                    close_prices = api_data['Close']
                else:
                    close_prices = api_data[ticker]['Close']
                if len(close_prices) >= 2:
                    latest_close = close_prices[-1]
                    previous_close = close_prices[-2]
                    value = latest_close
                    print(value)
                    print(previous_close)
                    daily_return = (latest_close - previous_close) / previous_close *100
                    daily_returns[ticker] = {'daily_return': daily_return, 'value': value}
                else:
                    daily_returns[ticker] = {'daily_return': None, 'value': None}
            except Exception as e:
                daily_returns[ticker] = {'daily_return': None, 'value': None}
                print(f"Error fetching data for {ticker}: {e}")
        return daily_returns
    pass

#calculate_upward_and_Downward_runs(df)
#print(len(up_trend_list))
#print(len(up_trend_dates))
#print(len(down_trend_list))
#print(len(down_trend_dates))

for i in range(0, len(down_trend_list)):
    print(f"{i+1} Downward Trend of {down_trend_list[i]} days from {down_trend_dates[i]}")


#testing max profit calculation
#current_dir = os.getcwd()
#file_path = os.path.join(current_dir,"src","CSV","AAPL.csv")
#df2 = pd.read_csv(file_path)
#max_profit= max_profit_calculation(df2)