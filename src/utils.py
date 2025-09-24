import pandas as pd
import streamlit as st


def filter_dataframe_by_date_range(df: pd.DataFrame, start_date: pd.Timestamp, end_date: pd.Timestamp) -> pd.DataFrame:



    df['Date'] = pd.to_datetime(df.index)
    

    mask = (df['Date'].dt.date >= start_date) & (df['Date'].dt.date <= end_date) 
    
    
    return df.loc[mask].copy()

# Function to verify if data is in correct format
def verify_data_format(data: pd.DataFrame) -> bool:
    required_columns = ['Date', 'Close', 'High', 'Low', 'Open', 'Volume']
    for col in required_columns:
        if col in data.columns:
            return True
    return False

