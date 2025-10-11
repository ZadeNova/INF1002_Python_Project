"""
visualization.py

Purpose:
    This module implements visualization functions for stock market data and technical indicators.

Functions:
    - create_indicator_traces(df, indicators, indicator_positions) -> list
    - create_subplots(indicators) -> tuple
    - create_price_chart(df: pd.DataFrame, type_of_chart: str) -> go.Figure
    - add_trading_signals(fig, df, show_buy_signals, show_sell_signals) -> None
    - configure_layout_and_axes(fig, num_rows, subplot_titles, stock_name, total_height) -> None
    - plot_visualization(df: pd.DataFrame, stock_name: str, type_of_chart: str, indicators, show_buy_signals, show_sell_signals, show_upward_and_downward_trends, total_height) -> go.Figure

Notes:
    This module provides functions to create interactive stock charts with technical indicators
    using Plotly. It supports multiple chart types, subplot configurations, and trading signals.
"""

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from src.technical_indicators import *
from src.config import *

def create_indicator_traces(df, indicators, indicator_positions):
    """
    Create all indicator traces with simplified logic.

    Args:
        df: DataFrame containing stock data with indicator columns.
        indicators: List of technical indicators to visualize.
        indicator_positions: Dictionary mapping indicators to subplot rows.

    Returns:
        list: List of tuples containing (trace, row, col) for each indicator.
    """
    traces = []
    
    for indicator in indicators:
        row = indicator_positions.get(indicator, 1)
        config = INDICATOR_VISUAL_CONFIG.get(indicator, {})
        
        # Indicators with only one line (e.g., SMAs, EMAs, VWAP)
        if 'indicator' in config:
            traces.append((
                go.Scatter(
                    x=df['Date'], y=df[config['indicator']], mode='lines',
                    line=dict(color=COLORS[config['color']], width=1),
                    name=config.get('label', indicator), showlegend=False
                ), row, 1
            ))
        
        # RSI indicator
        elif indicator == RSI_14:
            rsi_traces = [
                (go.Scatter(x=df['Date'], y=df['RSI'], mode='lines',
                    line=dict(color=COLORS['rsi'], width=1.5), name=RSI_14, showlegend=False), row, 1)
            ]
            # Add RSI reference lines
            for level, color_key, name in [(70, 'rsi_overbought', 'Overbought'), 
                                         (30, 'rsi_oversold', 'Oversold'),
                                         (50, 'rsi_center', 'Center')]:
                rsi_traces.append((
                    go.Scatter(x=[df['Date'].iloc[0], df['Date'].iloc[-1]], y=[level, level], mode='lines',
                        line=dict(color=COLORS[color_key], width=1, dash='dash'), name=f'RSI {name}', showlegend=False
                    ), row, 1
                ))
            traces.extend(rsi_traces)
                
        # MACD indicator
        elif indicator == MACD:
            traces.extend([
                (go.Scatter(x=df['Date'], y=df["MACD"], mode="lines",
                    line=dict(color=COLORS['macd'], width=1.5), name="MACD Line", showlegend=False), row, 1),
                (go.Scatter(x=df['Date'], y=df["Signal_Line"], mode="lines",
                    line=dict(color=COLORS['signal'], width=1.5), name="Signal Line", showlegend=False), row, 1),
                (go.Bar(x=df['Date'], y=df["MACD_Histogram"], name="MACD Histogram", opacity=0.6,
                    marker_color=[COLORS['macd_histogram_positive'] if val >= 0 else COLORS['macd_histogram_negative'] 
                                for val in df["MACD_Histogram"]], showlegend=False), row, 1)
            ])
    
    return traces


def create_subplots(indicators):
    """
    Create optimized dynamic subplot configuration.

    Args:
        indicators: List of technical indicators to display.

    Returns:
        tuple: (total_rows, row_heights, subplot_titles, indicator_positions)
    """
    separate_indicators = [ind for ind in indicators if ind in SEPARATE_SUBPLOT_INDICATORS]
    total_rows = 1 + len(separate_indicators)
    
    # Row height configuration based on number of rows
    if total_rows == 1:
        row_heights = [1.0]
    elif total_rows == 2:
        row_heights = [0.7, 0.3]
    else:  # 3+ rows
        price_height = max(0.5, 1.0 - (total_rows - 1) * 0.15)
        indicator_height = (1.0 - price_height) / (total_rows - 1)
        row_heights = [price_height] + [indicator_height] * (total_rows - 1)
    
    # Assign indicator positions
    subplot_titles = ["Price"] + separate_indicators
    indicator_positions = {}
    
    for i, indicator in enumerate(separate_indicators, 1):
        indicator_positions[indicator] = i + 1
    
    # Overlay indicators always go on row 1
    for indicator in indicators:
        if indicator in OVERLAY_INDICATORS:
            indicator_positions[indicator] = 1
    
    return total_rows, row_heights, subplot_titles, indicator_positions


def create_price_chart(df: pd.DataFrame, type_of_chart: str) -> go.Figure:
    """
    Create price chart trace based on selected chart type.

    Args:
        df: DataFrame containing stock price data.
        type_of_chart: Type of chart to create ("LineChart" or "Candlestick").

    Returns:
        go.Figure: Plotly figure object for the price chart.
    """
    common_params = dict(x=df['Date'], name="Price", showlegend=False)
    
    if type_of_chart == "LineChart":
        return go.Scatter(y=df['Close'], mode="lines", 
            line=dict(color=COLORS['price_line'], width=1.5), connectgaps=True, **common_params)
    elif type_of_chart == "CandleStick":
        return go.Candlestick(open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'],
            increasing_line_color=COLORS['bullish'], increasing_fillcolor=COLORS['bullish'],
            decreasing_line_color=COLORS['bearish'], decreasing_fillcolor=COLORS['bearish'], **common_params)
    else:
        raise ValueError(f"Unsupported chart type: {type_of_chart}")


def add_trading_signals(fig, df, show_buy_signals, show_sell_signals):
    """
    Add buy/sell signal markers to the price chart.

    Args:
        fig: Plotly figure to add signals to.
        df: DataFrame containing signal data.
        show_buy_signals: Boolean to show buy signals.
        show_sell_signals: Boolean to show sell signals.
    """
    signal_values = [
        (show_buy_signals, 'Buy_Signal', 'triangle-up', COLORS['buy_signal'], 'Buy'),
        (show_sell_signals, 'Sell_Signal', 'triangle-down', COLORS['sell_signal'], 'Sell')
    ]
    
    for show_flag, signal_col, symbol, color, name in signal_values:
        if show_flag and signal_col in df.columns:
            mask = df[signal_col]
            if mask.any():
                fig.add_trace(go.Scatter(
                    x=df.loc[mask, 'Date'], y=df.loc[mask, 'Close'], mode='markers',
                    marker=dict(symbol=symbol, color=color, size=10, line=dict(width=2, color='white')),
                    name=name, showlegend=False
                ), row=1, col=1)


def configure_layout_and_axes(fig, num_rows, subplot_titles, stock_name, total_height):
    """
    Configure axes properties and overall layout styling.

    Args:
        fig: Plotly figure to configure.
        num_rows: Number of subplot rows.
        subplot_titles: List of titles for each subplot.
        stock_name: Name of the stock for the chart title.
        total_height: Total height of the chart in pixels.
    """
    # Update main layout
    fig.update_layout(
        title=dict(text=f"{stock_name}", x=0.5, font=dict(color=COLORS['text'], size=16)),
        height=total_height, width=1000, plot_bgcolor=COLORS['background'],
        paper_bgcolor=COLORS['background'], font=dict(color=COLORS['text']),
        margin=dict(t=50, b=30, l=50, r=30), hovermode='x unified'
    )
    
    # Configure all axes uniformly
    axis_config = dict(
        showgrid=True, gridcolor=COLORS['grid'], gridwidth=0.5,
        showline=True, linecolor=COLORS['grid'], linewidth=1, zeroline=False
    )
    
    for i in range(1, num_rows + 1):
        fig.update_xaxes(**axis_config, rangeslider_visible=False, nticks=5, 
                        type='category', matches='x', row=i, col=1)
        fig.update_yaxes(**axis_config, tickformat=".3f", row=i, col=1)
        
        # Update subplot title styling
        if i <= len(subplot_titles):
            fig.layout.annotations[i-1].update(font=dict(color=COLORS['text'], size=12))
        
        # Only show x-axis labels on bottom subplot
        if i < num_rows:
            fig.update_xaxes(showticklabels=False, row=i, col=1)


def plot_visualization(df: pd.DataFrame, stock_name: str, type_of_chart: str, 
                      indicators=None, show_buy_signals=False, show_sell_signals=False, 
                      show_upward_and_downward_trends=False, total_height=600) -> go.Figure:
    """
    Create a comprehensive stock market visualization with technical indicators.

    Args:
        df: DataFrame containing stock data with indicator columns.
        stock_name: Name of the stock for display.
        type_of_chart: Type of price chart ("LineChart" or "Candlestick").
        indicators: List of technical indicators to display.
        show_buy_signals: Boolean to show buy signals.
        show_sell_signals: Boolean to show sell signals.
        show_upward_and_downward_trends: Boolean to show trend lines.
        total_height: Total height of the chart in pixels.

    Returns:
        go.Figure: Plotly figure object with the complete visualization.
    """
    indicators = indicators or []
    
    # Create dynamic subplot configuration
    num_rows, row_heights, subplot_titles, indicator_positions = create_subplots(indicators)
    
    # Create subplots with dark theme
    fig = make_subplots(
        rows=num_rows, 
        cols=1, 
        shared_xaxes=True, 
        vertical_spacing=0.02,
        subplot_titles=subplot_titles, 
        row_heights=row_heights
    )
    
    # Add price chart
    price_trace = create_price_chart(df, type_of_chart)
    fig.add_trace(price_trace, row=1, col=1)
    
    # Add indicators and signals
    for trace, row, col in create_indicator_traces(df, indicators, indicator_positions):
        fig.add_trace(trace, row=row, col=col)
    
    add_trading_signals(fig, df, show_buy_signals, show_sell_signals)
    
    # Configure layout
    configure_layout_and_axes(fig, num_rows, subplot_titles, stock_name, total_height)
    
    return fig