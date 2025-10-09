"""
ticker_utils.py

Purpose:
    This module contains utility functions for handling stock tickers, including
    categorizing tickers by exchange, fetching current prices, and converting prices to SGD.

Functions:
    - categorize_tickers(tickers_list: list, exchange_map: dict) -> dict
    - get_prices(tickers_list: list, period="5d", interval="1d") -> dict
    - resolve_unknown_currency(tickers_list: list, ticker_currency: dict) -> dict
    - get_prices_and_currency(tickers_list: list, ticker_prices:dict, ticker_currency:dict ) -> dict
    - convert_current_prices_to_sgd(price_data:dict) -> dict
    - get_fx_rates(currencies: list, target_currency: str = "SGD") -> dict
    - convert_invested_values(df: pd.DataFrame, fx_rates: dict, target_col="invested_value_sgd") -> pd.DataFrame
    
Notes:
    - Each function is designed to be modular and reusable.
    - Designed to work for the scope of this project.
    - Uses yfinance to fetch stock and forex data.
    - Handles unknown ticker currencies by attempting to fetch from yfinance info.
    - Converts prices to SGD using fetched forex rates.
    - Improvements can be made by adding caching for forex rates.

"""

from src.config import *
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import date, timedelta


def categorize_tickers(tickers_list: list, exchange_map: dict) -> dict:
    """
    Categorizes tickers based on their exchange suffix and assigns the corresponding currency.

    Args:
        tickers_list (list): A list of stock tickers to categorize.
        exchange_map (dict): A mapping of ticker suffixes to their exchange and currency information.

    Returns:
        dict: A dictionary mapping of each ticker to its corresponding currency.

    Notes:
        - If a ticker does not match any known suffix and does not contain a '.', it is assumed to be in USD.
        - This is because many US stocks do not have a suffix.
        - Tickers with unknown suffixes or formats will not be included in the returned dictionary. - Tickers with unknown suffixes will be settled by another function.
    """
    ticker_currency = {}


    for ticker in tickers_list:
        try:
            found = False
            for suffix, data in exchange_map.items():
                if ticker.endswith(suffix):
                    ticker_currency[ticker] = data["currency"]
                    found = True
                    break
                
            if not found:
                if "." not in ticker:
                    ticker_currency[ticker] = "USD"
        except Exception as e:
            print(f"Error categorizing ticker: {e}")
            continue
    print(ticker_currency)
    print('bola caregorize ticker')
    return ticker_currency



def get_prices(tickers_list: list, period="5d", interval="1d") -> dict:
    """
    Fetches the latest closing prices for a list of tickers using yfinance.

    Args:
        tickers_list (list): A list of stock tickers to fetch prices for.
        period (str): The period over which to fetch historical data. Default is "5d".
        interval (str): The data interval. Default is "1d".

    Returns:
        dict: A dictionary mapping each ticker to its latest closing price.

    Notes:
        - If a ticker has no available price data, its price will be set to NaN.
        - Uses yfinance to download historical data.
        - The function handles both single and multiple tickers.
        - Errors during data fetching or processing are caught and logged, with NaN assigned to problematic tickers.
    """
    prices_data = {}

    if not tickers_list:
        return {}

    try:
        data = yf.download(tickers_list, period=period, interval=interval, group_by="ticker", progress=False)
    except Exception as e:
        print(f"Error fetching prices: {e}")
        return {ticker: float("nan") for ticker in tickers_list}

    # --- Single ticker path ---
    if len(tickers_list) == 1:
        ticker = tickers_list[0]
        try:
            # Try bulk-download data first
            if "Close" in data.columns:
                price_series = data["Close"].dropna()
                if not price_series.empty and price_series.iloc[-1] != 0:
                    prices_data[ticker] = float(price_series.iloc[-1])
                    return prices_data

            # If bulk failed or 0, fallback to ticker.history()
            print(f"Retrying {ticker} with direct fetch...")
            t = yf.Ticker(ticker)
            hist = t.history(period=period, interval=interval)
            if not hist.empty and "Close" in hist.columns:
                last_close = hist["Close"].dropna().iloc[-1]
                prices_data[ticker] = float(last_close)
            else:
                prices_data[ticker] = float("nan")

        except Exception as e:
            print(f"Error processing single ticker {ticker}: {e}")
            prices_data[ticker] = float("nan")

        return prices_data

    # --- Multi-ticker path ---
    for ticker in tickers_list:
        try:
            if ticker not in data.columns.levels[0]:
                print(f"Ticker {ticker} not found in fetched data")
                prices_data[ticker] = float("nan")
                continue

            price_series = data[ticker]["Close"].dropna()
            if price_series.empty or price_series.iloc[-1] == 0:
                print(f"Empty/zero data for {ticker}, setting NaN")
                prices_data[ticker] = float("nan")
            else:
                prices_data[ticker] = float(price_series.iloc[-1])

        except Exception as e:
            print(f"Unexpected error for ticker {ticker}: {e}")
            prices_data[ticker] = float("nan")

    return prices_data


def resolve_unknown_currency(tickers_list: list, ticker_currency: dict):
    """
    Resolves unknown currencies for tickers by fetching their info from yfinance.

    Args:
        tickers_list (list): A list of stock tickers to resolve currencies for.
        ticker_currency (dict): A dictionary mapping tickers to their known currencies. Tickers with unknown currencies should not be in this dictionary.

    Returns:
        dict: An updated dictionary mapping each ticker to its resolved currency.

    Notes:
        - If a ticker's currency cannot be determined, it will be set to "UNKNOWN".
        - Uses yfinance to fetch ticker information.
        - This function modifies the input dictionary in place and also returns it for convenience.
        - Errors during data fetching or processing are caught and logged, with "UNKNOWN" assigned to problematic tickers.
    """
    print('hgi')
    print(ticker_currency)
    print(tickers_list)
    try:
        for ticker in tickers_list:
            if ticker not in ticker_currency:
                try:
                    info = yf.Ticker(ticker).info
                    ticker_currency[ticker] = info.get("currency"," UNKNOWN")
                except Exception as e:
                    print(f"An Error Occured: {e}")
                    ticker_currency[ticker] = "UNKNOWN"
    except Exception as e:
        print(f"Error resolving currencies: {e}")
        ticker_currency = {ticker: "UNKNOWN" for ticker in tickers_list if ticker not in ticker_currency}
        
    return ticker_currency



def get_prices_and_currency(tickers_list: list, ticker_prices:dict, ticker_currency:dict ) -> dict:
    """
    Combines ticker prices and their corresponding currencies into a single dictionary.
    Args:
        tickers_list (list): A list of stock tickers.
        ticker_prices (dict): A dictionary mapping tickers to their prices.
        ticker_currency (dict): A dictionary mapping tickers to their currencies.       

    Returns:
        dict: A dictionary mapping each ticker to its price and currency.

    Notes:
        - If a ticker's price or currency is not found, it will be set to None.
        - This function assumes that ticker_prices and ticker_currency have been populated correctly.
        - The function returns a dictionary in the format:
        - {ticker: {"price": price, "currency": currency}, ...}
        - Errors during processing are caught and logged, with None assigned to problematic tickers.
    """
    try:
       result = {ticker: {"price": ticker_prices.get(ticker), "currency": ticker_currency.get(ticker)} for ticker in tickers_list}
       
    except Exception as e:
        print(f"Error combining prices and currencies: {e}")
        result = {ticker: {"price": None, "currency": None} for ticker in tickers_list}    
    return result



def convert_current_prices_to_sgd(price_data:dict) -> dict:
    """
    Converts current prices of tickers to SGD using forex rates.
    Args:
        price_data (dict): A dictionary mapping tickers to their prices and currencies. Example format:
            {ticker: {"price": price, "currency": currency}, ...}      

    Returns:
        dict: A dictionary mapping each ticker to its price in SGD, original price, and currency.
            Example format:
            {ticker: {"price_sgd": price_in_sgd, "original_price": original_price, "currency": currency}, ...}

    Notes:
        - If a ticker's price or currency is not found, or if conversion fails, price_sgd will be set to None.
        - Uses yfinance to fetch forex rates.
    """
    result = {}
    fx_cache = {}
    
    for ticker, data in price_data.items():
        try:
            price = data["price"]
            currency = data["currency"]
            
            if price is None:
                price_sgd = None
            elif currency == "SGD":
                price_sgd = price
            else:
            
                if currency in fx_cache:
                    fx_rate = fx_cache[currency]
                else:
                    fx_ticker = f"{currency}SGD=X"
                    
                    try:
                        fx_data = yf.download(fx_ticker, period="5d",interval="1d")
                        fx_rate = fx_data["Close"].dropna().iloc[-1]
                        fx_cache[currency] = fx_rate
                    except Exception as e:
                        print(f"Could not fetch FX rate for {fx_ticker}: {e}")
                        fx_rate = None

                        
                if fx_rate is None:
                    price_sgd = None
                else:
                    price_sgd = float(price) * float(fx_rate)
                
            result[ticker] = {
                "price_sgd": price_sgd,
                "original_price": price,
                "currency": currency
            }
        except Exception as e:
            print(f"Error converting price for {ticker} {data}: {e}")
            result[ticker] = {
                "price_sgd": None,
                "original_price": data.get("price"),
                "currency": data.get("currency")
            }
    return result
                
    
                
def get_fx_rates(currencies: list, target_currency: str = "SGD") -> dict:
    """
    Fetches forex rates for a list of currencies against a target currency using yfinance.
    Args:
        currencies (list): A list of currency codes to fetch forex rates for.
        target_currency (str): The target currency code to convert to. Default is "SGD".   

    Returns:
        dict: A dictionary mapping each currency to its forex rate against the target currency.
            Example format:
            {currency: rate, ...}

    Notes:
        - If a currency is the same as the target currency, its rate will be set to 1.0.
        - If a currency's rate cannot be fetched, it will be set to 1.
    """
    fx_rates = {}
    
    for curr in currencies:
        if curr == target_currency:
            fx_rates[curr] = 1.0
            continue
        
        pair = f"{curr}{target_currency}=X"
        
        try:
            data = yf.download(pair, period="5d", interval="1d", progress=False)
            rate = data["Close"].dropna().iloc[-1]
            fx_rates[curr] = float(rate)
        except Exception as e:
            print(f" Cound not fetch rate for {pair}")
            print(f"Error occured: {e}")
            fx_rates[curr] = 1.0
        
    return fx_rates
    
    
    
def convert_invested_values(df: pd.DataFrame, fx_rates: dict, target_col="invested_value_sgd") -> pd.DataFrame:
    """
    Converts the invested values in a DataFrame to SGD using provided forex rates.
    Args:
        df (pd.DataFrame): A DataFrame containing at least 'invested_value' and 'currency' columns.
        fx_rates (dict): A dictionary mapping currencies to their forex rates against SGD.
        target_col (str): The name of the column to store the converted invested values. Default is "invested_value_sgd".    

    Returns:
        pd.DataFrame: The input DataFrame with an additional column for invested values in SGD.

    Notes:
        - If a currency is not found in fx_rates, a rate of 1.0 will be used (no conversion).
        - If an error occurs during conversion, the target column will be filled with NaN.
    """
    try:
        df[target_col] = df.apply(
            lambda row: row["invested_value"] * fx_rates.get(row["currency"], 1.0),
            axis=1
            
        )
    except Exception as e:
        print(f"Error converting invested values: {e}")
        df[target_col] = np.nan
        
    return df