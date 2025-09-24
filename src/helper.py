"""
helper.py

Purpose:
    This module contains helper functions for data manipulation and validation.

Functions:
    - filter_dataframe_by_date_range(df: pd.DataFrame, start_date: pd.Timestamp, end_date: pd.Timestamp) -> pd.DataFrame
    - verify_data_format(data: pd.DataFrame) -> bool  

Notes:
    Each function is designed to assist in preprocessing and validating data
    for further analysis or visualization.
"""




import pandas as pd
import streamlit as st


def filter_dataframe_by_date_range(df: pd.DataFrame, start_date: pd.Timestamp, end_date: pd.Timestamp) -> pd.DataFrame:

    """
    This function filters a DataFrame to include only rows within a specified date range selected by the user.

    Args:
        df (pd.DataFrame): The input DataFrame containing stock data with a DateTime index.
        start_date (pd.Timestamp): The start date of the desired date range.
        end_date (pd.Timestamp): The end date of the desired date range.
        

    Returns:
        pd.DataFrame: A DataFrame filtered to include only rows within the specified date range.
    
    Notes:
        - The function assumes that the DataFrame index is of DateTime type.
        - The function uses boolean masking to filter the DataFrame.
        - How boolean masking works: A boolean mask is created by evaluating a condition on the DataFrame's Date column. This mask is then used to filter the DataFrame, returning only the rows where the condition is True.
        - The function returns a copy of the filtered DataFrame to avoid SettingWithCopyWarning.
    """


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

