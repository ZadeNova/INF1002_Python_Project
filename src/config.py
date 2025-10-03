"""
config.py

Purpose:
    This config file contains constants and configuration settings
    used across the stock analysis and visualization modules.

Notes:
    This file contains settings such as the select fields for technical indicators,
    the list of stock tickers to track, and default date ranges for data fetching.
"""



"""
# -----------------------------
# Configuration Settings
# -----------------------------

For the TA selected fields, these are the technical indicators that can be applied to stock data. These variables are used as labels in the application. The variables exist in multiple files, so they are defined here to ensure consistency across the project.

Files that the variables exist in:
- src/technical_indicators.py
- src/visualization.py 
- app.py
"""
# TA Select FIELDS
SMA_20_LABEL = "SMA 20 (Short Term)"
SMA_50_LABEL = "SMA 50 (Medium Term)"
SMA_200_LABEL = "SMA 200 (Long Term)"
RSI_14_LABEL = "RSI 14"
VWAP = "VWAP"
MACD = "MACD"
EMA12 = "EMA12"
EMA26 = "EMA26"

TECHNICAL_INDICATOR_OPTIONS = [
    SMA_20_LABEL,
    SMA_50_LABEL,
    SMA_200_LABEL,
    RSI_14_LABEL,
    VWAP,
    MACD,
    EMA12,
    EMA26
]

# Period Select Fields
PERIOD_SELECT_OPTIONS = [
    "1d",    # Last 1 day
    "5d",    # Last 5 days
    "1mo",   # Last 1 month
    "3mo",   # Last 3 months
    "6mo",   # Last 6 months
    "1y",    # Last 1 year
    "2y",    # Last 2 years
    "5y",    # Last 5 years
    "10y",   # Last 10 years
    "ytd",   # Year-to-date
    "max"    # Maximum available history
]


# List of stocks you want to track
TICKERS = [
    "AAPL",     # Apple
    "MSFT",     # Microsoft
    "NAS",      # NASDAQ 
    "AMZN",     # Amazon
    "META",     # Facebook
    "SPY",      # SNP500
    "C6L.SI"    # Singapore Airlines 
]

# Default start date for historical data
START_DATE = "2024-01-01"
END_DATE = "2026-01-01"
