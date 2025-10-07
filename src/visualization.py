"""
visualization.py

Purpose:
    This module contains functions for visualizing stock data and technical indicators.

Functions:
    - plot_visualization(df: pd.DataFrame, stock_name: str, type_of_chart ,indicators=None ,show_buy_signals=False, show_sell_signals=False, show_upward_trends=False, show_downward_trends=False) -> go.Figure
    
    
Notes:
    The main function creates a Plotly figure with subplots for stock prices and selected technical indicators.
"""



import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

#Technical Indicator Functions
from src.technical_indicators import *
from src.config import *

def get_subplot_titles(indicators):
    titles = ["Stock Price"]  # Always include the stock price chart
    
    # Add indicator titles based on the selected indicators
    if MACD in indicators:
        titles.append("MACD")
    if RSI_14_LABEL in indicators:
        titles.append("RSI")
    
    return titles

# Plotting Function

def plot_visualization(df: pd.DataFrame, stock_name: str, type_of_chart, indicators=None,
                       show_buy_signals=False, show_sell_signals=False,
                       show_upward_and_downward_trends=False) -> go.Figure:
    """
    Plots stock data with technical indicators and buy/sell signals.

    Args:
        df (pd.DataFrame): DataFrame with stock data.
        stock_name (str): Name of the stock.
        type_of_chart (str): "LineChart" or "Candlestick".
        indicators (list, optional): List of indicators to plot.
        show_buy_signals (bool, optional): Show buy signals on chart.
        show_sell_signals (bool, optional): Show sell signals on chart.

    Returns:
        go.Figure: Plotly figure.
    """
    if indicators is None:
        indicators = []

    # Determine which RSI/MACD indicators are selected and order them dynamically
    indicator_order = [i for i in indicators if i in [MACD, RSI_14_LABEL]]

    # Set number of rows: row 1 always for price, plus up to 2 for RSI/MACD
    num_rows = 1 + len(indicator_order)
    row_heights = [0.6] + [0.2] * (num_rows - 1)

    # Prepare subplot titles
    subplot_titles = ["Stock Price"] + [i for i in indicator_order]

    fig = make_subplots(
        rows=num_rows,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.05,
        row_heights=row_heights,
        subplot_titles=subplot_titles
    )

    # --- Price Chart ---
    if type_of_chart == "LineChart":
        fig.add_trace(
            go.Scatter(x=df['Date'], y=df['Close'], mode="lines", name="Close"),
            row=1, col=1
        )
    else:  # Candlestick
        fig.add_trace(
            go.Candlestick(
                x=df['Date'],
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'],
                increasing_line_color="green",     # outline for bullish candles
                increasing_fillcolor="green",      # fill bullish candles solid green
                decreasing_line_color="red",       # outline for bearish candles
                decreasing_fillcolor="red"         # fill bearish candles solid red
            ),
            row=1, col=1
        )
        fig.update_xaxes(rangeslider_visible=False)

    # --- Overlay Indicators on Price Chart (row 1) ---
    for indicator in indicators:
        if indicator == SMA_20_LABEL:
            fig.add_trace(go.Scatter(x=df['Date'], y=df['SMA_20'], mode='lines',
                                     line=dict(color='goldenrod', width=2), name="SMA 20"), row=1, col=1)
        if indicator == SMA_50_LABEL:
            fig.add_trace(go.Scatter(x=df['Date'], y=df['SMA_50'], mode='lines',
                                     line=dict(color='teal', width=2), name="SMA 50"), row=1, col=1)
        if indicator == SMA_200_LABEL:
            fig.add_trace(go.Scatter(x=df['Date'], y=df['SMA_200'], mode='lines',
                                     line=dict(color='dimgray', width=2), name="SMA 200"), row=1, col=1)
        if indicator == EMA12:
            fig.add_trace(go.Scatter(x=df['Date'], y=df['EMA_12'], mode='lines',
                                     line=dict(color='darkorange', width=2), name="EMA 12"), row=1, col=1)
        if indicator == EMA26:
            fig.add_trace(go.Scatter(x=df['Date'], y=df['EMA_26'], mode='lines',
                                     line=dict(color='slateblue', width=2), name="EMA 26"), row=1, col=1)
        if indicator == VWAP:
            fig.add_trace(go.Scatter(x=df['Date'], y=df['VWAP'], mode='lines',
                                     line=dict(color='indigo', width=1.8), name="VWAP"), row=1, col=1)

    # --- RSI/MACD Subplots (rows 2+) ---
    for idx, indicator in enumerate(indicator_order):
        row_num = idx + 2  # row 2 for first indicator
        if indicator == MACD:
            fig.add_trace(go.Scatter(x=df['Date'], y=df['MACD'], mode='lines', name="MACD",line=dict(color='mediumblue', width=2)), row=row_num, col=1)
            fig.add_trace(go.Scatter(x=df['Date'], y=df['Signal_Line'], mode='lines', name="Signal",line=dict(color='orangered', width=2)), row=row_num, col=1)
            fig.add_trace(go.Bar(
                x=df['Date'], y=df['MACD_Histogram'], name="Histogram",
                marker_color=['seagreen' if val >= 0 else 'crimson' for val in df["MACD_Histogram"]],
                opacity=0.5,
                hovertemplate="Histogram: %{y:.4f}<extra></extra>"
            ), row=row_num, col=1)
        elif indicator == RSI_14_LABEL:
            fig.add_trace(go.Scatter(x=df['Date'], y=df['RSI'], mode='lines', name="RSI",line=dict(color='darkorange', width=2)), row=row_num, col=1)
            fig.add_hline(y=70, line_dash="dash", line_color="red", row=row_num, col=1)
            fig.add_hline(y=30, line_dash="dash", line_color="green", row=row_num, col=1)

    # --- Buy/Sell Signals ---
    if show_buy_signals:
        fig.add_trace(go.Scatter(
            x=df.loc[df['Buy_Signal'], 'Date'],
            y=df.loc[df['Buy_Signal'], 'Close'],
            mode='markers',
            marker=dict(symbol='triangle-up', color='deepskyblue', size=10),
            name='Buy Signal'
        ), row=1, col=1)

    if show_sell_signals:
        fig.add_trace(go.Scatter(
            x=df.loc[df['Sell_Signal'], 'Date'],
            y=df.loc[df['Sell_Signal'], 'Close'],
            mode='markers',
            marker=dict(symbol='triangle-down', color='darkmagenta', size=10),
            name='Sell Signal'
        ), row=1, col=1)

    # --- Layout ---
    fig.update_layout(
        title=f"{stock_name} Price with Indicators",
        xaxis_title='',
        yaxis_title='Price (USD)',
        legend=dict(x=0, y=1, bgcolor="rgba(0,0,0,0)"),
        height=1000, width=1000
    )

    return fig
