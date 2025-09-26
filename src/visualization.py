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
def plot_visualization(df: pd.DataFrame, stock_name: str, type_of_chart ,indicators=None ,show_buy_signals=False, show_sell_signals=False, show_upward_trends=False, show_downward_trends=False) -> go.Figure:
    """
    Plots stock data with selected technical indicators and trade signals. This function creates a Plotly figure with subplots for stock prices and selected technical indicators.

    Args:
        df (pd.DataFrame): DataFrame containing stock data with necessary columns.
        stock_name (str): Name of the stock for the chart title.
        type_of_chart (str): Type of chart to display ("LineChart" or "Candlestick").
        indicators (list, optional): List of technical indicators to include. Defaults to None.
        show_buy_signals (bool, optional): Whether to display buy signals. Defaults to False.
        show_sell_signals (bool, optional): Whether to display sell signals. Defaults to False.
        show_upward_trends (bool, optional): Whether to highlight upward trends. Defaults to False.
        show_downward_trends (bool, optional): Whether to highlight downward trends. Defaults to False.

    Returns:
        go.Figure: Plotly figure object with the visualizations.
    
    Notes:
        - The function dynamically creates subplots based on selected indicators.
        - The function supports both line and candlestick charts for stock prices.
        - The function uses Plotly's built-in features for interactivity.
        - Buy and sell signals are marked with distinct markers on the price chart.
        - Upward and downward trends can be highlighted with shaded regions. ( currently commented out and under development)
        
    """
    
    
    if indicators is None:
        indicators = []
    
    row_counter = 1 + len(indicators)
    


    subplot_titles = get_subplot_titles(indicators)

    fig = make_subplots(
    rows=3, cols=1, shared_xaxes=True,
    vertical_spacing=0.05,
    subplot_titles=subplot_titles,
    row_heights=[0.6, 0.2, 0.2]   # 60%, 20%, 20%
)

    # Ensure first row has dates
    fig.update_xaxes(showticklabels=True, row=1, col=1)
    
    

    
    print(df.info())
    
    
    if type_of_chart == "LineChart":
        pass
        # Linechart Code here
        #fig = go.Figure([go.Scatter(x=df['Date'], y=df[f'Close'])])
        fig.add_trace(
            go.Scatter(x=df['Date'], y=df[f'Close'], mode="lines", name="Close"),
            row=1, col=1
        )
    else:
        # Candlestick Chart here
        fig.add_trace(
        go.Candlestick(
            x=df['Date'],
            open=df[f'Open'],
            high=df[f'High'],
            low=df[f'Low'],
            close=df[f'Close'],
            increasing_line_color="green",     # outline for bullish candles
            increasing_fillcolor="green",      # fill bullish candles solid green
            decreasing_line_color="red",       # outline for bearish candles
            decreasing_fillcolor="red"         # fill bearish candles solid red
        ),
        row=1, col=1
        )
        fig.update_xaxes(rangeslider_visible=False)
        #fig.update_layout(xaxis_rangeslider_visible=False)
    
    
    current_row = 2
    
    for indicator in indicators:
        if indicator == SMA_20_LABEL:
            fig.add_trace(go.Scatter(x=df['Date'], y=df['SMA_20'], mode='lines', line=dict(color='green', width=2), name="SMA 20"))
        if indicator == SMA_50_LABEL:
            fig.add_trace(go.Scatter(x=df['Date'], y=df['SMA_50'], mode='lines', line=dict(color='orange', width=2), name="SMA 50"))
        if indicator == SMA_200_LABEL:
            fig.add_trace(go.Scatter(x=df['Date'], y=df['SMA_200'], mode='lines', line=dict(color='red', width=2), name="SMA 200"))

        if indicator == MACD:
            fig.add_trace(go.Scatter(x=df['Date'], y=df["MACD"], mode="lines", name="MACD"), row=2, col=1)
            fig.add_trace(go.Scatter(x=df['Date'], y=df["Signal_Line"], mode="lines", name="Signal"), row=2, col=1)
            fig.add_trace(go.Bar(
            x=df['Date'], y=df["MACD_Histogram"], name="Histogram",
            marker_color=['rgba(0, 128, 0, 1)' if val >= 0 else 'rgba(255, 0, 0, 1)' for val in df["MACD_Histogram"]],
            opacity=0.5,
            hovertemplate="Histogram: %{y:.4f}<extra></extra>"
    ), row=2, col=1)

        if indicator == RSI_14_LABEL:
            fig.add_trace(go.Scatter(x=df['Date'], y=df["RSI"], mode="lines", name="RSI"), row=3, col=1)
            fig.add_hline(y=70, line_dash="dash", line_color="red", row=3, col=1)
            fig.add_hline(y=30, line_dash="dash", line_color="green", row=3, col=1)

           
        if indicator == EMA12:
            fig.add_trace(
            go.Scatter(
            x=df['Date'],
            y=df['EMA_12'],
            mode="lines",
            name="EMA",
            line=dict(color="blue", width=2)
        ),
        row=1, col=1 )
            
        if indicator == EMA26:
            fig.add_trace(
            go.Scatter(
            x=df['Date'],
            y=df['EMA_26'],
            mode="lines",
            name="EMA",
            line=dict(color="yellow", width=2)
        ),
        row=1, col=1)
        
        if indicator == VWAP:
             fig.add_trace(go.Scatter(x=df['Date'], y=df["VWAP"], mode="lines", name="VWAP"), row=1, col=1)
    
    
    
    
    
    if show_buy_signals:
        
        fig.add_trace(
            go.Scatter(
                x=df.loc[df['Buy_Signal'], 'Date'],
                y=df.loc[df['Buy_Signal'], 'Close'],
                mode='markers',
                marker=dict(symbol='triangle-up', color='green', size=10),
                name='Buy Signal'
            ),
            row=1, col=1
        )
        print("Buy signals plotted")

    if show_sell_signals:
        
        fig.add_trace(
            go.Scatter(
                x=df.loc[df['Sell_Signal'], 'Date'],
                y=df.loc[df['Sell_Signal'], 'Close'],
                mode='markers',
                marker=dict(symbol='triangle-down', color='red', size=10),
                name='Sell Signal'
            ),
            row=1, col=1
        )
        
        
        
    streak_options = []
    if show_upward_trends:
        streak_options.append(("Up_Trend", "rgba(0, 0, 255, 0.3)"))

    if show_downward_trends:
        streak_options.append(("Down_Trend", "rgba(255, 0, 0, 0.3)"))
    
    
    
    
    
    
    
    
    
    
    
    #for streak_col, color in streak_options:
    #    in_streak = False
    #    for i in range(len(df)):
    #        if df[streak_col].iloc[i] > 0 and not in_streak:
    #            # Start of a streak
    #            in_streak = True
    #            start_date = df.index[i-1] if i > 0 else df.index[i]
    #        elif (df[streak_col].iloc[i] == 0 or i == len(df)-1) and in_streak:
    #            end_date = df.index[i] if df[streak_col].iloc[i] > 0 else df.index[i-1]
    #            fig.add_vrect(
    #                type='rect',
    #                xref='x',
    #                yref='paper',
    #                x0=start_date,
    #                x1=end_date,
    #                y0=0,
    #                y1=1,
    #                fillcolor=color,
    #                line=dict(width=0),
    #                layer="below"
    #                
    #            )
    #            in_streak = False
                
                
    fig.update_layout(
        title=f"{stock_name} Price with Indicators",
        xaxis_title='',
        yaxis_title='Price (USD)',
        legend=dict(x=0, y=1, bgcolor="rgba(0,0,0,0)"),
        height=1000, width=1000
    )

    return fig
