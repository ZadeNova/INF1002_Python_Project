import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Dict, Any

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Networth Calculator", page_icon="💸", layout="wide")

DATA_FILE = Path(__file__).resolve().parents[1] / "networth_data.json"

st.title("💸Networth Calculator")
st.markdown(
    """
Welcome to BullBearAnalysis's **Networth Calculator**.
    
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
def load_portfolio() -> Dict[str, Any]:
    _ensure_data_file()
    data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    data["holdings"] = [
        {
            "ticker": str(h.get("ticker", "")).upper(),
            "buy_price": float(h.get("buy_price", 0.0)),
            "amount": float(h.get("amount", 0.0)),
        }
        for h in data.get("holdings", [])
    ]
    return data

#save portfolio data to json file, translate python dictionary into json format and write to file
def save_portfolio(data: Dict[str, Any]) -> None:
    DATA_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")
    load_portfolio.clear()  # bust cache


#main function to render the networth calculator page
def holdings_to_df(holdings: List[Dict[str, Any]]) -> pd.DataFrame:
    df = pd.DataFrame(holdings, columns=["ticker", "buy_price", "amount"])
    if df.empty:
        return df
    df["value"] = df["buy_price"] * df["amount"]
    return df


def format_currency(x: float) -> str:
    return f"${x:,.2f}"

#UI portion
portfolio_data = load_portfolio()
holdings = portfolio_data.get("holdings", [])

with st.form("holdings_form", clear_on_submit=True):
    st.subheader("Enter your stock holdings:")
    col1, col2, col3 = st.columns([1.2, 1, 1])
    with col1:
        ticker = st.text_input("Stock ticker", placeholder="e.g., AAPL").strip().upper()
    with col2:
        buy_price = st.number_input("Buy price ($)", min_value=0.0, value=0.0, step=0.01, format="%.2f")
    with col3:
        amount = st.number_input("Amount (shares)", min_value=0.0, value=0.0, step=1.0)
    submitted = st.form_submit_button("Add Holding")
    if submitted:
        if not ticker:
            st.warning("Please enter a stock ticker.")
        elif buy_price <= 0 or amount <= 0:
            st.warning("Buy price and amount must be greater than zero.")
        else:
            new_holding = holdings(ticker=ticker, buy_price=buy_price, amount=amount)
            holdings.append(asdict(new_holding))
            portfolio_data["holdings"] = holdings
            save_portfolio(portfolio_data)
            st.success(f"Added {ticker} — {amount} @ ${buy_price:.2f}")
            st.experimental_rerun()
