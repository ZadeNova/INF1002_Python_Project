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
# =============================================================================
# TECHNICAL INDICATOR CONFIGURATION
# =============================================================================

# Technical Indicator Names
SMA_20 = "SMA 20"
SMA_50 = "SMA 50"
SMA_200 = "SMA 200"
VWAP = "VWAP"
EMA12 = "EMA12"
EMA26 = "EMA26"
RSI_14 = "RSI"
MACD = "MACD"

# Available Technical Indicators for Selection
TECHNICAL_INDICATOR_OPTIONS = [
    SMA_20,
    SMA_50,
    SMA_200,
    VWAP,
    EMA12,
    EMA26,
    RSI_14,
    MACD
]

# =============================================================================
# VISUALIZATION CONFIGURATION
# =============================================================================

# Subplot Configuration
SEPARATE_SUBPLOT_INDICATORS = [MACD, RSI_14]
OVERLAY_INDICATORS = [SMA_20, SMA_50, SMA_200, EMA12, EMA26, VWAP]

# Technical Indicator Visualization Configuration
INDICATOR_VISUAL_CONFIG = {
    SMA_20: {
        'indicator': 'SMA_20',
        'color': 'sma_20',
        'label': SMA_20
    },
    SMA_50: {
        'indicator': 'SMA_50',
        'color': 'sma_50',
        'label': SMA_50
    },
    SMA_200: {
        'indicator': 'SMA_200',
        'color': 'sma_200',
        'label': SMA_200
    },
    EMA12: {
        'indicator': 'EMA_12',
        'color': 'ema_12',
        'label': EMA12
    },
    EMA26: {
        'indicator': 'EMA_26',
        'color': 'ema_26',
        'label': EMA26
    },
    VWAP: {
        'indicator': 'VWAP',
        'color': 'vwap',
        'label': VWAP
    },
    RSI_14: {
        'label': RSI_14
    },
    MACD: {
        'label': MACD
    }
}

# Color Scheme for Charts
COLORS = {
    # Price Action
    'bullish': '#0FB36D',
    'bearish': '#E64C3D', 
    'price_line': '#00FF00',
    
    # Moving Averages
    'sma_20': '#FF6B6B',
    'sma_50': '#4ECDC4',
    'sma_200': '#45B7D1',
    'ema_12': '#FFA500',
    'ema_26': '#9370DB',
    'vwap': '#FFD700',
    
    # MACD
    'macd': '#FFA500',
    'signal': '#00BFFF',
    'macd_histogram_positive': '#00FF00',
    'macd_histogram_negative': '#FF0000',
    
    # RSI
    'rsi': '#FFA500',
    'rsi_overbought': '#FF4444',
    'rsi_oversold': '#44FF44',
    'rsi_center': '#888888',
    
    # Trading Signals
    'buy_signal': '#00FF00',
    'sell_signal': '#FF0000',
    
    # Chart Layout
    'background': '#1E1E1E',
    'grid': '#2D2D2D',
    'text': '#FFFFFF'
}

# =============================================================================
# DATA FETCHING CONFIGURATION
# =============================================================================

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

"""
# Exchange Mapping for determining currency based on ticker suffix
# Source: https://help.yahoo.com/kb/SLN2310.html
"""
EXCHANGE_MAP = {
    ".T":  {"exchange": "Tokyo Stock Exchange", "country": "Japan", "currency": "JPY"},
    ".DE": {"exchange": "XETRA", "country": "Germany", "currency": "EUR"},
    ".L":  {"exchange": "London Stock Exchange", "country": "UK", "currency": "GBP"},
    ".HK": {"exchange": "Hong Kong Exchange", "country": "Hong Kong", "currency": "HKD"},
    ".SI": {"exchange": "Singapore Exchange", "country": "Singapore", "currency": "SGD"}
}