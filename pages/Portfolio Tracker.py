import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Dict, Any
from src.analytics import calculate_daily_returns
import os

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
    quantity: float
    price_per_share: float

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
                #print(new_holding)
                #user_portfolio.append(asdict#(new_holding))
                
                save_portfolio(portfolio_name, new_stock_holding=new_holding)
                st.success(f"Added {amount} shares(s) of {ticker} @ ${buy_price:.2f} to your portfolio.")
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
        #print(updated_stock_portfolio)
        # Save to JSON file
        st.session_state[f'portfolio_{portfolio_name}'] = updated_stock_portfolio  # Update session state
        with open(USER_DATA_DIR / f"portfolio_{portfolio_name}.json", 'w', encoding='utf-8') as file:
            json.dump(updated_stock_portfolio, file)

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
    
