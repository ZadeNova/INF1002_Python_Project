# config.py


# TA Select FIELDS
SMA_20_LABEL = "SMA 20 (Short Term)"
SMA_50_LABEL = "SMA 50 (Medium Term)"
SMA_200_LABEL = "SMA 200 (Long Term)"
RSI_14_LABEL = "RSI 14"
VWAP = "VWAP"
MACD = "MACD"
EMA = "EMA"


TECHNICAL_INDICATOR_OPTIONS = [
    SMA_20_LABEL,
    SMA_50_LABEL,
    SMA_200_LABEL,
    RSI_14_LABEL,
    VWAP,
    MACD,
    EMA,
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
