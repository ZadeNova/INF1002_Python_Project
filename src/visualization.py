import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

#Technical Indicator Functions
from src.technical_indicators import *
from src.config import *

# Plotting Function
def plot_visualization(df: pd.DataFrame, stock_name: str, type_of_chart ,indicators=None):
    # Decide how many rows we need
    
    
    if indicators is None:
        indicators = []
    
    row_counter = 1 + len(indicators)
    
    if len(indicators) == 0:
        row_heights = [1.0]
    else:
        indicator_height = 0.4 / len(indicators)
        row_heights = [0.6] + [indicator_height] * len(indicators)
    
    # fix the rows
    
    fig = make_subplots(
        rows=row_counter, cols=1, shared_xaxes=True,
        vertical_spacing=0.05, subplot_titles=("Stock Price","RSI","MACD"),
        row_heights=row_heights
    )

    # Ensure first row has dates
    fig.update_xaxes(showticklabels=True, row=1, col=1)
    
    
    # print(df.head(10))
    # print(df.head(1))
    # print(df.head(2))
    #print(f"INDICATOR CHECK {indicators}")
    # To flatten multi column to single column
    #df.columns = ['_'.join(col).strip() for col in df.columns.values]
    df['Date'] = pd.to_datetime(df.index)
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
            close=df[f'Close']
        ),
        row=1, col=1
        )
        
        #fig.update_layout(xaxis_rangeslider_visible=False)
    
    
    
    
    
    current_row = 2
    
    for indicator in indicators:
        if indicator == SMA_20_LABEL:
            fig.add_trace(go.Scatter(x=df['Date'], y=df['SMA_20'], mode='lines', line=dict(color='green', width=2), name="SMA 20"))
        if indicator == SMA_50_LABEL:
            fig.add_trace(go.Scatter(x=df['Date'], y=df['SMA_50'], mode='lines', line=dict(color='orange', width=2), name="SMA 50"))
        if indicator == SMA_200_LABEL:
            fig.add_trace(go.Scatter(x=df['Date'], y=df['SMA_200'], mode='lines', line=dict(color='red', width=2), name="SMA 200"))

        if indicator == RSI_14_LABEL:
            
            fig.add_trace(go.Scatter(x=df['Date'], y=df["RSI"], mode="lines", name="RSI"), row=current_row, col=1)
            current_row += 1
        
        if indicator == MACD:
           
           fig.add_trace(go.Scatter(x=df['Date'], y=df["MACD"], mode="lines", name="MACD"), row=current_row, col=1)
           
           fig.add_trace(go.Scatter(x=df['Date'], y=df["Signal_Line"], mode="lines", name="Signal"), row=current_row, col=1)
           
           fig.add_trace(go.Bar(x=df['Date'], y=df["MACD_Histogram"], name="Histogram", 
                                   marker_color=['rgba(0, 128, 0, 1)' if val >= 0 else 'rgba(255, 0, 0, 1)' for val in df["MACD_Histogram"]],
                                   opacity=0.5,
                                   hovertemplate="Histogram: %{y:.4f}<extra></extra>"), row=current_row, col=1)
           current_row += 1
           
           
        
        if indicator == EMA:
            
            # I have not done  EMA cause I want to sleep.
            # Please help settle 
            fig.add_trace(
                    go.Scatter(
                        x=df.index, 
                        y=df[f"EMA_12"],  
                        mode="lines", 
                        name=f"EMA 12"
                    ), 
                    row=1, 
                    col=1
                )
        
        if indicator == VWAP:
             fig.add_trace(go.Scatter(x=df['Date'], y=df["VWAP"], mode="lines", name="VWAP"), row=1, col=1)
    
    
    
    
    #if indicators:
    #    if "SMA" in indicators:
    #        # Edit to change windows for SMA periods you want
    #        sma_windows = [50, 200]
    #        
    #        for window in sma_windows:
    #            df = calculate_SMA_pandas(df, window)
    #            fig.add_trace(
    #                go.Scatter(
    #                    x=df.index, 
    #                    y=df[f"SMA{window}"],
    #                    mode="lines", 
    #                    name=f"SMA{window}"
    #                ), 
    #                row=1, 
    #                col=1
    #            )
#
    #    if "EMA" in indicators:
    #        # Edit to change windows for EMA periods you want
    #        ema_periods = [20, 50]
    #        
    #        for period in ema_periods:
    #            df = calculate_EMA(df, period)
    #            fig.add_trace(
    #                go.Scatter(
    #                    x=df.index, 
    #                    y=df[f"EMA{period}"],  # Use f-string for dynamic column access
    #                    mode="lines", 
    #                    name=f"EMA{period}"
    #                ), 
    #                row=1, 
    #                col=1
    #            )
#
    #    if "VWAP" in indicators:
    #        df = calculate_VWAP(df)
    #        fig.add_trace(go.Scatter(x=df.index, y=df["VWAP"], mode="lines", name="VWAP"), row=1, col=1)
#
    #    if "MACD" in indicators:
    #        df = calculate_MACD(df)
    #        row_counter += 1
    #        fig.add_trace(go.Scatter(x=df.index, y=df["MACD"], mode="lines", name="MACD"), row=row_counter, #col=1)
    #        fig.add_trace(go.Scatter(x=df.index, y=df["Signal_Line"], mode="lines", name="Signal"), #row=row_counter, col=1)
    #        fig.add_trace(go.Bar(x=df.index, y=df["MACD_Histogram"], name="Histogram", 
    #                                marker_color=['rgba(0, 128, 0, 1)' if val >= 0 else 'rgba(255, 0, 0, 1)' #for val in df["MACD_Histogram"]],
    #                                opacity=0.5,
    #                                hovertemplate="Histogram: %{y:.4f}<extra></extra>"), row=row_counter, #col=1)
#
    #    if "RSI" in indicators:
    #        df = calculate_RSI_new(df)
    #        row_counter += 1
    #        fig.add_trace(go.Scatter(x=df.index, y=df["RSI"], mode="lines", name="RSI"), row=row_counter, #col=1)
    #        fig.add_hline(y=70, line_dash="dash", line_color="red", row=row_counter, col=1)
    #        fig.add_hline(y=30, line_dash="dash", line_color="green", row=row_counter, col=1)


    fig.update_layout(
        title=f"{stock_name} Price with Indicators",
        xaxis_title='Time',
        yaxis_title='Price (USD)',
        legend=dict(x=0, y=1, bgcolor="rgba(0,0,0,0)"),
        height=1000, width=1000
    )

    return fig
