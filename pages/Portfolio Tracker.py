import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Dict, Any
import os

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Portfolio Tracker", page_icon="💸", layout="wide")


# Get the correct file paths
# I will clean up this file when I have time 
# - Erfan

BASE_DIR = Path(__file__).resolve().parent.parent
#print(BASE_DIR)
USER_DATA_DIR = BASE_DIR / "data" / "user_data"
#print(USER_DATA_DIR)
#USER_DATA_DIR.mkdir(parents=True, exist_ok=True)




DATA_FILE = Path(__file__).resolve().parents[1] / "networth_data.json"
print(DATA_FILE)
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

#ensuring that the cache data file exists before any operations
def _ensure_data_file():
    """Create the data file if it doesn't exist."""
    if not DATA_FILE.exists():
        DATA_FILE.write_text(json.dumps({"holdings": []}), encoding="utf-8")

#load portfolio data from json file, read and parse json data into python dictionary
@st.cache_data(show_spinner=False)
def load_portfolio(portfolio_name: str):

    filename = f"user_data/portfolio_{portfolio_name}.json"
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return json.load(file)
    return []
    
    # data["holdings"] = [
    #     {
    #         "ticker": str(h.get("ticker", "")).upper(),
    #         "buy_price": float(h.get("buy_price", 0.0)),
    #         "amount": float(h.get("amount", 0.0)),
    #     }
    #     for h in data.get("holdings", [])
    # ]
    # return data

#save portfolio data to json file, translate python dictionary into json format and write to file
def save_portfolio(username: str, portfolio_data) -> None:
    #DATA_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")
    #load_portfolio.clear()  # bust cache
    print(type(portfolio_data))
    print(json.dumps(portfolio_data))
    print(type(portfolio_data))
    filename = USER_DATA_DIR / f"portfolio_{username}.json"
    
    # Currently its overwriting the existing file.
    # Write the logic to append to the exisiting file.
    # Save 1: AAPL. Save 2: TSLA. 
    # Result: TSLA will be shown not apple. Ideal is AAPL + TSLA.
    
    with open(filename, 'w') as file:
        json.dump(portfolio_data, file)


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
        st.session_state[f'portfolio_{portfolio_name}'] = load_portfolio(portfolio_name)
    
    # Get portfolio from session state
    # IF first time username , user_portfolio will be a []
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
                user_portfolio.append(asdict(new_holding))
                
                save_portfolio(portfolio_name, user_portfolio)

                st.success(f"Added {amount} shares(s) of {ticker} @ ${buy_price:.2f} to your portfolio.")
                
                # Rerun to update this page
                st.rerun()
