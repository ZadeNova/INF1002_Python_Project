"""
portfolio_tracker.py

Purpose:
    This module is the Portfolio Tracker page of the BullBearAnalysis Streamlit application.
    It allows users to input their stock holdings and calculates the total value of their portfolio.

Functions:
    - None (main application script for the Portfolio Tracker page)
Notes:
    The module uses a dataclass to represent stock holdings and stores user data in JSON files.
    The Json files are read and written to manage user portfolios.
    
    Discussion on JSON files and its scalability:
        - Yes its true that JSON files are not scalable for large applications, but for the purpose of this project and simplicity, it is sufficient.
        - The ideal would be to use a database like SQLite or PostgreSQL for better scalability and data management.
"""



import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Dict, Any
from src.analytics import calculate_daily_returns, calculate_networth
import os
import yfinance as yf
import numpy as np

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Portfolio Tracker", page_icon="💸", layout="wide")

BASE_DIR = Path(__file__).resolve().parent.parent
USER_DATA_DIR = BASE_DIR / "data" / "user_data"


st.title("💸Portfolio Tracker")
st.markdown(
    """
Welcome to BullBearAnalysis's **Portfolio Tracker**.
    
This tool helps you calculate your net worth by inputting your stock holdings. Simply enter the values in the input fields below, and your net worth will be calculated automatically.
"""
)

@dataclass
class StockHoldings:
    ticker: str
    price_per_share: float
    quantity: float

    def total_value(self) -> float:
        return self.quantity * self.price_per_share

#load portfolio data from json file, read and parse json data into python dictionary
@st.cache_data(show_spinner=False)
def load_portfolio(portfolio_name: str):

    filename = USER_DATA_DIR / f"portfolio_{portfolio_name}.json"
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            data = json.load(file)
            st.session_state[f'portfolio_{portfolio_name}'] = data
            return data
    return []
    
#save portfolio data to json file, translate python dictionary into json format and write to file
def save_portfolio(username: str, new_stock_holding: StockHoldings) -> None:

    filename = USER_DATA_DIR / f"portfolio_{username}.json"

    # Check if file exists
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            try:
                
                existing_data = json.load(file)
            except json.JSONDecodeError:
                # File exists but is empty or invalid JSON
                print(f"Error with JSON file")
                existing_data = []
    else:
        # File does not exist, intialize a empty list
        existing_data = []

    # Append new data to existing data
    if isinstance(existing_data, list):
        
        # Create new entry in JSON format
        existing_data.append(asdict(new_stock_holding))
    
    # Write back to file with added data
    # OR create a file if it has not been created before
    with open(filename, 'w',encoding='utf-8') as file:
        json.dump(existing_data,file)
    
    st.session_state[f'portfolio_{username}'] = existing_data
    




#main function to render the Portfolio Tracker page
def holdings_to_df(holdings: List[Dict[str, Any]]) -> pd.DataFrame:
    df = pd.DataFrame(holdings, columns=["ticker", "buy_price", "amount"])
    if df.empty:
        return df
    df["value"] = df["buy_price"] * df["amount"]
    return df


def format_currency(x: float) -> str:
    return f"${x:,.2f}"

#UI portion
#portfolio_data = load_portfolio()
#holdings = portfolio_data.get("holdings", [])

portfolio_name = st.text_input("Enter your portfolio name:", key="portfolio_name")

if portfolio_name:
    # Initialize a session state for this portfolio if it does not exist.
    if f'portfolio_{portfolio_name}' not in st.session_state:

        the_data = load_portfolio(portfolio_name=portfolio_name)
        st.session_state[f'portfolio_{portfolio_name}'] = load_portfolio(portfolio_name)
    
    # Get portfolio from session state
    # IF first time username , user_portfolio will be a []
    #st.session_state[f'portfolio_{portfolio_name}'] = load_portfolio(portfolio_name)
    user_portfolio = st.session_state[f'portfolio_{portfolio_name}']
    
    # Form to add stock
        
    with st.form("holdings_form", clear_on_submit=True):
        st.subheader("Enter your stock holdings:")
        col1, col2, col3 = st.columns([1.2, 1, 1])
        with col1:
            ticker = st.text_input("Stock ticker", placeholder="e.g., AAPL").strip().upper()
        with col2:
            buy_price = st.number_input("Buy price ($)", min_value=0.0, value=0.0, step=0.01, format="%.2f")
        with col3:
            amount = st.number_input("Quantity (shares)", min_value=0.0, value=0.0, step=0.01)
        submitted = st.form_submit_button("Add Holding to Portfolio")
        if submitted:
            if not ticker:
                st.warning("Please enter a stock ticker.")
            elif buy_price <= 0 or amount <= 0:
                st.warning("Buy price and share quantity must be greater than zero.")
            else:
                new_holding = StockHoldings(ticker=ticker, price_per_share=buy_price, quantity=amount)
                save_portfolio(portfolio_name, new_stock_holding=new_holding)
                st.success(f"Added {amount} shares(s) of {ticker} @ ${buy_price:.2f} to your portfolio.")
                st.cache_data.clear()
                st.session_state[f'portfolio_{portfolio_name}'] = load_portfolio(portfolio_name)
                #Rerun to update this page
                st.rerun()
    
    # Add the table to display Portfolio
    stock_dataframe = pd.DataFrame(user_portfolio)
    #print(stock_dataframe)
    edited_stock_dataframe = st.data_editor(
        stock_dataframe,
        num_rows='dynamic',
        use_container_width=True
    )
    if st.button("Save Changes"):
        # Convert back to list of dicts
        updated_stock_portfolio = edited_stock_dataframe.to_dict('records')
        # Save to JSON file
        st.session_state[f'portfolio_{portfolio_name}'] = updated_stock_portfolio  # Update session state
        with open(USER_DATA_DIR / f"portfolio_{portfolio_name}.json", 'w', encoding='utf-8') as file:
            json.dump(updated_stock_portfolio, file)
        st.rerun()


#Calculate and display net worth for every stock holding with def calculate_networth
    st.sidebar.header("Net Worth Summary")
    if not stock_dataframe.empty:
        net_worth_data = calculate_networth(stock_dataframe)
        if net_worth_data:
            net_worth_table = net_worth_data.get("table")
            total_invested = float(net_worth_data.get("total_invested", 0.0))
            total_current_value = float(net_worth_data.get("total_current_value", 0.0))
            profit_loss = float(net_worth_data.get("profit_loss", 0.0))
            profit_loss_pct = float(net_worth_data.get("profit_loss_pct", 0.0))

            if net_worth_table is not None and not net_worth_table.empty:

                df = net_worth_table.copy()
                if "profit_loss" not in df.columns:
                    df["profit_loss"] = df["current_value"] - df["invested_value"]
                if "profit_loss_pct" not in df.columns:
                    df["profit_loss_pct"] = np.where(df["invested_value"] > 0, df["profit_loss"] / df["invested_value"] * 100.0,np.nan)

            # Display summary metrics
            st.sidebar.metric("Total Invested", format_currency(total_invested))
            st.sidebar.metric("Current Value", format_currency(total_current_value))
            if profit_loss >= 0:
                st.sidebar.metric("Profit/Loss", format_currency(profit_loss), delta=f"{profit_loss_pct:.2f}%")
            else:
                st.sidebar.metric("Profit/Loss", format_currency(profit_loss), delta=f"{profit_loss_pct:.2f}%")

        else:
            st.sidebar.write("Could not calculate net worth. Please check your portfolio data.")
    else:
        st.sidebar.write("Portfolio is empty. Add stocks to see net worth calculation.")



#Daily returns UI on sidebar (api data to get current stock price and calculate daily returns)
    st.sidebar.header("Daily Returns")
    if not stock_dataframe.empty:
        daily_returns = calculate_daily_returns(stock_dataframe)
        if daily_returns:
            for ticker, values in daily_returns.items():
                daily_return = values['daily_return']
                value = values['value']
                if daily_return is not None:
                    if daily_return <= 0:
                        st.sidebar.metric(label=f"{ticker}", value=f"${value:.2f}", delta=f"{daily_return:.2f}%")
                    else:
                        st.sidebar.metric(label=f"{ticker}", value=f"${value:.2f}", delta=f"{daily_return:.2f}%")
                else:
                    st.sidebar.write(f"{ticker}: Data not available")
        else:
            st.sidebar.write("No tickers found in portfolio.")
    else:
        st.sidebar.write("Portfolio is empty. Add stocks to see daily returns.")
    