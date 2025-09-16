import pandas as pd
import numpy as np
import timeit
import os
#import talib
from data_loader import fetch_stock_data, fetch_latest_price
import config
import datetime 

for tickers in config.TICKERS:
    df = fetch_stock_data(tickers, save=False)

for tickers in config.TICKERS:
    latest_price = fetch_latest_price(tickers)

tickers = "AAPL" #just for testing
df = fetch_stock_data(tickers, save=False)

#maybe switch to dictionary, dates as keys, prices as values
up_trend_list = [] #stores length of each upward trend
down_trend_list = [] #stores length of each downward trend
up_trend_dates = [] #stores start and end date of each upward trend
down_trend_dates = [] #stores start and end date of each downward trend

def calculate_upward_and_Downward_runs(df: pd.DataFrame):

    #Counter for number of consecutive up and down days
    up_streak_counter = 0
    down_streak_counter = 0

    #Counter for the longest streak in each direction
    highest_up_streak = 0
    highest_down_streak = 0
    highest_up_streak_dates = ""
    highest_down_streak_dates = ""

    start_date = df['Date'].iloc[0]

    #Iterate through each day and compare with previous day
    for i in range(1, len(df)) :

        #if stock price went up compared to previous day, increment up counter
        if df['Close'].iloc[i] >= df['Close'].iloc[i-1]:
            #if there was a down counter before this, means up streak is lesser than 2 days, reset counter
            if down_streak_counter == 1:
                down_streak_counter = 0
                #reset start date to previous day
                start_date = df['Date'].iloc[i-1]
            up_streak_counter += 1

        #if stock price went down compared to previous day, increment down counter    
        elif df['Close'].iloc[i] <= df['Close'].iloc[i-1]:
            #if there was an up counter before this, means down streak is lesser than 2 days, reset counter
            if up_streak_counter == 1:
                up_streak_counter = 0
                #reset start date to previous day
                start_date = df['Date'].iloc[i-1]
            down_streak_counter += 1

        #Check if a up streak lasts for min 2 consecutive days before recording it
        if up_streak_counter >= 2 and down_streak_counter == 1:
            up_trend_list.append(up_streak_counter)
            end_date = df['Date'].iloc[i-1]
            up_trend_dates.append(str(start_date) + " to " + str(end_date))

            #Check if this is the longest up streak so far
            if up_streak_counter > highest_up_streak:
                highest_up_streak = up_streak_counter
                highest_up_streak_dates = str(start_date) + " to " + str(end_date)

            start_date = end_date
            up_streak_counter = 0

        #Check if a down streak lasts for min 2 consecutive days before recording it
        elif down_streak_counter >=2  and up_streak_counter == 1:
            down_trend_list.append(down_streak_counter)
            end_date = df['Date'].iloc[i-1]
            down_trend_dates.append(str(start_date) + " to " + str(end_date))

            #Check if this is the longest up streak so far
            if down_streak_counter > highest_down_streak:
                highest_down_streak = down_streak_counter
                highest_down_streak_dates = str(start_date) + " to " + str(end_date)

            start_date = end_date
            down_streak_counter = 0

        else:
            pass
    print("Longest Upward Trend: " + str(highest_up_streak) + " days from " + str(highest_up_streak_dates))
    print("Longest Downward Trend: " + str(highest_down_streak) + " days from " + str(highest_down_streak_dates))
    pass


def max_profit_calculation():
    pass


def calculate_daily_returns():
    pass

calculate_upward_and_Downward_runs(df)
#print(len(up_trend_list))
#print(len(up_trend_dates))
#print(len(down_trend_list))
#print(len(down_trend_dates))

for i in range(0, len(down_trend_list)):
    print(f"{i+1} Downward Trend of {down_trend_list[i]} days from {down_trend_dates[i]}")
