"""
visualization.py
"""

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Technical Indicator Functions
from src.technical_indicators import *
from src.config import *

# Color Scheme
COLORS = {
    'bullish': '#E64C3D',      # Red for up candles
    'bearish': '#0FB36D',      # Green for down candles  
    'background': '#1E1E1E',   # Dark background
    'grid': '#2D2D2D',         # Grid lines
    'text': '#FFFFFF',         # White text
    'price_line': '#00FF00',   # Bright green
    'sma_20': '#FF6B6B',       # Coral
    'sma_50': '#4ECDC4',       # Teal
    'sma_200': '#45B7D1',      # Light blue
    'ema_12': '#FFA500',       # Orange
    'ema_26': '#9370DB',       # Purple
    'vwap': '#FFD700',         # Gold
    'macd': '#FFA500',         # Orange
    'signal': '#00BFFF',       # Deep sky blue
    'rsi': '#FFA500',          # Orange
    'buy_signal': '#00FF00',   # Bright green
    'sell_signal': '#FF0000',  # Bright red
}


def create_subplots(indicators):
    """
    Create optimized dynamic subplot configuration.
    """
    subplot_titles = ["Price"]
    indicator_positions = {}
    
    # Pre-calculate separate subplot count
    separate_subplot_count = sum(1 for indicator in indicators if indicator in SEPARATE_SUBPLOT_INDICATORS)
    total_rows = 1 + separate_subplot_count
    
    if total_rows == 1:
        row_heights = [1.0]
    elif total_rows == 2:
        row_heights = [0.7, 0.3]
    else:  # 3+ rows
        price_height = 0.6 if total_rows == 3 else 0.5
        indicator_height = (1.0 - price_height) / (total_rows - 1)
        row_heights = [price_height] + [indicator_height] * (total_rows - 1)
    
    current_row = 2
    for indicator in indicators:
        if indicator in SEPARATE_SUBPLOT_INDICATORS:
            subplot_titles.append(indicator)
            indicator_positions[indicator] = current_row
            current_row += 1
        elif indicator in OVERLAY_INDICATORS:
            indicator_positions[indicator] = 1
    
    return total_rows, row_heights, subplot_titles, indicator_positions

def create_indicator_traces(df, indicators, indicator_positions):
    """
    Pre-create all traces for better performance.
    Returns a list of traces with their row positions.
    """
    traces = []
    
    for indicator in indicators:
        row = indicator_positions.get(indicator, 1)
        
        if indicator == SMA_20_LABEL:
            traces.append((
                go.Scatter(
                    x=df['Date'], y=df['SMA_20'], mode='lines', 
                    line=dict(color=COLORS['sma_20'], width=1), 
                    name="SMA 20", showlegend=False
                ), row, 1
            ))
            
        elif indicator == SMA_50_LABEL:
            traces.append((
                go.Scatter(
                    x=df['Date'], y=df['SMA_50'], mode='lines', 
                    line=dict(color=COLORS['sma_50'], width=1), 
                    name="SMA 50", showlegend=False
                ), row, 1
            ))
            
        elif indicator == SMA_200_LABEL:
            traces.append((
                go.Scatter(
                    x=df['Date'], y=df['SMA_200'], mode='lines', 
                    line=dict(color=COLORS['sma_200'], width=1), 
                    name="SMA 200", showlegend=False
                ), row, 1
            ))
            
        elif indicator == MACD:
            traces.extend([
                (go.Scatter(
                    x=df['Date'], y=df["MACD"], mode="lines", 
                    line=dict(color=COLORS['macd'], width=1.5), 
                    name="MACD", showlegend=False
                ), row, 1),
                (go.Scatter(
                    x=df['Date'], y=df["Signal_Line"], mode="lines", 
                    line=dict(color=COLORS['signal'], width=1.5), 
                    name="Signal", showlegend=False
                ), row, 1),
                (go.Bar(
                    x=df['Date'], y=df["MACD_Histogram"], name="Histogram",
                    marker_color=[
                        '#00FF00' if val >= 0 else '#FF0000' 
                        for val in df["MACD_Histogram"]
                    ],
                    opacity=0.6, showlegend=False
                ), row, 1)
            ])
            
        elif indicator == RSI_14_LABEL:
            traces.append((
                go.Scatter(
                    x=df['Date'], y=df["RSI"], mode="lines", 
                    line=dict(color=COLORS['rsi'], width=1.5), 
                    name="RSI 14", showlegend=False
                ), row, 1
            ))
            
        elif indicator == EMA12:
            traces.append((
                go.Scatter(
                    x=df['Date'], y=df['EMA_12'], mode='lines',
                    line=dict(color=COLORS['ema_12'], width=1), 
                    name="EMA 12", showlegend=False
                ), row, 1
            ))
            
        elif indicator == EMA26:
            traces.append((
                go.Scatter(
                    x=df['Date'], y=df['EMA_26'], mode='lines',
                    line=dict(color=COLORS['ema_26'], width=1), 
                    name="EMA 26", showlegend=False
                ), row, 1
            ))
            
        elif indicator == VWAP:
            traces.append((
                go.Scatter(
                    x=df['Date'], y=df["VWAP"], mode="lines", 
                    line=dict(color=COLORS['vwap'], width=1), 
                    name="VWAP", showlegend=False
                ), row, 1
            ))
    
    return traces

def plot_visualization(df: pd.DataFrame, stock_name: str, type_of_chart: str, 
                      indicators=None, show_buy_signals=False, show_sell_signals=False, 
                      show_upward_and_downward_trends=False, total_height=600) -> go.Figure:

    
    if indicators is None:
        indicators = []
    
    # Create dynamic subplot configuration
    num_rows, row_heights, subplot_titles, indicator_positions = create_subplots(indicators)
    
    # Create subplots with dark theme
    fig = make_subplots(
        rows=num_rows, 
        cols=1, 
        shared_xaxes=True,
        vertical_spacing=0.02,  # Tighter spacing
        subplot_titles=subplot_titles,
        row_heights=row_heights
    )
    
    # Add price chart (optimized)
    if type_of_chart == "LineChart":
        fig.add_trace(
            go.Scatter(
                x=df['Date'], y=df['Close'], mode="lines", 
                line=dict(color=COLORS['price_line'], width=1.5), 
                name="Price", showlegend=False
            ),
            row=1, col=1
        )
    else:
        fig.add_trace(
            go.Candlestick(
                x=df['Date'],
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'],
                increasing_line_color=COLORS['bearish'],    # Green for up
                increasing_fillcolor=COLORS['bearish'],
                decreasing_line_color=COLORS['bullish'],    # Red for down
                decreasing_fillcolor=COLORS['bullish'],
                name="Price",
                showlegend=False
            ),
            row=1, col=1
        )
    
    # Pre-create and add all indicator traces at once (performance optimization)
    indicator_traces = create_indicator_traces(df, indicators, indicator_positions)
    for trace, row, col in indicator_traces:
        fig.add_trace(trace, row=row, col=col)
    
    # Add trading signals (optimized)
    if show_buy_signals and 'Buy_Signal' in df.columns:
        buy_mask = df['Buy_Signal']
        if buy_mask.any():
            fig.add_trace(
                go.Scatter(
                    x=df.loc[buy_mask, 'Date'],
                    y=df.loc[buy_mask, 'Close'],
                    mode='markers',
                    marker=dict(
                        symbol='triangle-up', 
                        color=COLORS['buy_signal'], 
                        size=10, 
                        line=dict(width=2, color='white')
                    ),
                    name='Buy', showlegend=False
                ),
                row=1, col=1
            )
    
    if show_sell_signals and 'Sell_Signal' in df.columns:
        sell_mask = df['Sell_Signal']
        if sell_mask.any():
            fig.add_trace(
                go.Scatter(
                    x=df.loc[sell_mask, 'Date'],
                    y=df.loc[sell_mask, 'Close'],
                    mode='markers',
                    marker=dict(
                        symbol='triangle-down', 
                        color=COLORS['sell_signal'], 
                        size=10, 
                        line=dict(width=2, color='white')
                    ),
                    name='Sell', showlegend=False
                ),
                row=1, col=1
            )
    
    fig.update_layout(
        title=dict(
            text=f"{stock_name}",
            x=0.5,
            font=dict(color=COLORS['text'], size=16)
        ),
        height=total_height,
        width=1000,
        plot_bgcolor=COLORS['background'],
        paper_bgcolor=COLORS['background'],
        font=dict(color=COLORS['text']),
        margin=dict(t=50, b=30, l=50, r=30),
        xaxis=dict(showgrid=True, gridcolor=COLORS['grid']),
        yaxis=dict(showgrid=True, gridcolor=COLORS['grid']),
        hovermode='x unified'
    )
    
    for i in range(1, num_rows + 1):
        fig.update_xaxes(
            showgrid=True, 
            gridcolor=COLORS['grid'], 
            gridwidth=0.5,
            showline=True, 
            linecolor=COLORS['grid'], 
            linewidth=1,
            zeroline=False,
            rangeslider_visible=False,  
            row=i, 
            col=1
        )
        fig.update_yaxes(
            showgrid=True, 
            gridcolor=COLORS['grid'], 
            gridwidth=0.5,
            showline=True, 
            linecolor=COLORS['grid'], 
            linewidth=1,
            zeroline=False,
            row=i, 
            col=1
        )
        
        # Update subplot title styling
        if i <= len(subplot_titles):
            fig.layout.annotations[i-1].update(
                font=dict(color=COLORS['text'], size=12)
            )
    
    # Add RSI reference lines if RSI is selected
    if RSI_14_LABEL in indicators:
        rsi_row = indicator_positions.get(RSI_14_LABEL, 1)
        fig.add_hline(y=70, line_dash="dash", line_color="#FF4444", line_width=1, row=rsi_row, col=1)
        fig.add_hline(y=30, line_dash="dash", line_color="#44FF44", line_width=1, row=rsi_row, col=1)
        fig.add_hline(y=50, line_dash="dot", line_color="#888888", line_width=0.5, row=rsi_row, col=1)
    
    # Only show x-axis labels on bottom subplot
    for i in range(1, num_rows):
        fig.update_xaxes(showticklabels=False, row=i, col=1)
    fig.update_xaxes(showticklabels=True, row=num_rows, col=1)
    
    return fig