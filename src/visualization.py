import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

#Technical Indicator Functions
from src.SMA import calculate_SMA_pandas
from src.EMA import calculate_EMA
from src.RSI import calculate_RSI_new
from src.MACD import calculate_MACD
from src.VWAP import calculate_VWAP


# Plotting Function
def plot_visualization(df, stock_name, indicators=None):
    # Decide how many rows we need
    rows = 1
    if indicators and "MACD" in indicators:
        rows += 1
    if indicators and "RSI" in indicators:
        rows += 1

    # Create subplots for indicators
    subplot_titles = [f"{stock_name} Price"]
    if indicators and "MACD" in indicators:
        subplot_titles.append("MACD")
    if indicators and "RSI" in indicators:
        subplot_titles.append("RSI")

    fig = make_subplots(
        rows=rows, cols=1, shared_xaxes=True,
        vertical_spacing=0.05, subplot_titles=subplot_titles,
        row_heights=[0.6] + [0.2] * (rows - 1)  # Price bigger, indicators smaller
    )

    row_counter = 1

    # Price chart
    fig.add_trace(
        go.Scatter(x=df.index, y=df["Close"], mode="lines", name="Close"),
        row=row_counter, col=1
    )

    if indicators:
        if "SMA" in indicators:
            # Edit to change windows for SMA periods you want
            sma_windows = [50, 200]
            
            for window in sma_windows:
                df = calculate_SMA_pandas(df, window)
                fig.add_trace(
                    go.Scatter(
                        x=df.index, 
                        y=df[f"SMA{window}"],
                        mode="lines", 
                        name=f"SMA{window}"
                    ), 
                    row=1, 
                    col=1
                )

        if "EMA" in indicators:
            # Edit to change windows for EMA periods you want
            ema_periods = [20, 50]
            
            for period in ema_periods:
                df = calculate_EMA(df, period)
                fig.add_trace(
                    go.Scatter(
                        x=df.index, 
                        y=df[f"EMA{period}"],  # Use f-string for dynamic column access
                        mode="lines", 
                        name=f"EMA{period}"
                    ), 
                    row=1, 
                    col=1
                )

        if "VWAP" in indicators:
            df = calculate_VWAP(df)
            fig.add_trace(go.Scatter(x=df.index, y=df["VWAP"], mode="lines", name="VWAP"), row=1, col=1)

        if "MACD" in indicators:
            df = calculate_MACD(df)
            row_counter += 1
            fig.add_trace(go.Scatter(x=df.index, y=df["MACD"], mode="lines", name="MACD"), row=row_counter, col=1)
            fig.add_trace(go.Scatter(x=df.index, y=df["Signal_Line"], mode="lines", name="Signal"), row=row_counter, col=1)
            fig.add_trace(go.Bar(x=df.index, y=df["MACD_Histogram"], name="Histogram", 
                                    marker_color=['rgba(0, 128, 0, 1)' if val >= 0 else 'rgba(255, 0, 0, 1)' for val in df["MACD_Histogram"]],
                                    opacity=0.5,
                                    hovertemplate="Histogram: %{y:.4f}<extra></extra>"), row=row_counter, col=1)

        if "RSI" in indicators:
            df = calculate_RSI_new(df)
            row_counter += 1
            fig.add_trace(go.Scatter(x=df.index, y=df["RSI"], mode="lines", name="RSI"), row=row_counter, col=1)
            fig.add_hline(y=70, line_dash="dash", line_color="red", row=row_counter, col=1)
            fig.add_hline(y=30, line_dash="dash", line_color="green", row=row_counter, col=1)


    fig.update_layout(
        title=f"{stock_name} Price with Indicators",
        legend=dict(x=0, y=1, bgcolor="rgba(0,0,0,0)"),
        height=600 if rows == 1 else 300 * rows
    )

    return fig
