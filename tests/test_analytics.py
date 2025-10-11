"""
tests/test_analytics.py

Purpose:
    This module contains unit tests for the analytics functions in src/analytics.py.

Functions (classes):
    - Test_upward_downward_runs
    - Test_max_profit_calculation
    - Test_calculate_daily_returns

Notes:
    Each test class contains multiple test cases to validate the correctness of the corresponding analytics functions.
    The tests cover various scenarios, including edge cases, to ensure robust functionality.
"""


import pytest
from unittest.mock import patch
import pandas as pd
from src.analytics import *





class Test_upward_downward_runs:

    def test_all_upward_trend(self):
        """Test case for a DataFrame with all upward trend."""
        df = pd.DataFrame({"Close": [1, 2, 3, 4, 5]}, 
                          index=pd.date_range("2024-01-01", periods=5))
        result_df, longest_up, longest_down = calculate_upward_and_Downward_runs(df)

        assert longest_up["length"] == 4
        assert longest_down["length"] == 0
        assert longest_up["start"] == result_df.index[0]
        assert longest_up["end"] == result_df.index[-1]


    
    def test_all_downward_trend(self):
        """Test case for a DataFrame with all downward trend."""
        df = pd.DataFrame({"Close":[10,8,7,3,1]},
                          index=pd.date_range("2024-01-01", periods=5))
        result_df, longest_up, longest_down = calculate_upward_and_Downward_runs(df)

        assert longest_down["length"] == 4
        assert longest_up["length"] == 0
        assert longest_down["start"] == result_df.index[0]
        assert longest_down["end"] == result_df.index[-1]


    def test_no_trend_flat_prices(self):
        """Test case for a DataFrame with flat prices (no trend)."""
        df = pd.DataFrame({"Close": [5, 5, 5, 5]}, 
                          index=pd.date_range("2024-01-01", periods=4))
        result_df, longest_up, longest_down = calculate_upward_and_Downward_runs(df)

        assert longest_up["length"] == 0
        assert longest_down["length"] == 0
        assert longest_down["start"] == None
        assert longest_down["end"] == None


    def test_mixed_trends(self):
        """Test case for a DataFrame with mixed upward and downward trends."""
        # Up (1→3), Down (3→1), Up (1→4)
        df = pd.DataFrame({"Close": [1, 2, 3, 2, 1, 2, 3, 4]}, 
                          index=pd.date_range("2024-01-01", periods=8))
        result_df, longest_up, longest_down = calculate_upward_and_Downward_runs(df.copy())

        assert longest_up["length"] == 3   # 1→4 is the longest upward
        assert longest_up["end"] ==  result_df.index[-1]
        assert longest_down["length"] == 2 # 3→1 downward
        assert longest_down["end"] == result_df.index[4]

class Test_max_profit_calculation:

    def test_increasing_prices(self):
        """Test case for a DataFrame with strictly increasing prices."""
        df = pd.DataFrame({"Close": [1,2,3,4,5]}
                          , index=pd.date_range("2024-01-01", periods=5))
        
        result_df, profit, buy_signal = max_profit_calculation(df)

        assert profit == 4
        assert buy_signal == 4
    
    def test_decreasing_prices(self):
        """Test case for a DataFrame with strictly decreasing prices."""
        df = pd.DataFrame({"Close": [5,4,3,2,1]}
                          , index=pd.date_range("2024-01-01", periods=5))
        
        result_df, profit, buy_signal = max_profit_calculation(df)

        assert profit == 0
        assert buy_signal == 0


    def test_flat_prices(self):
        """Test case for a DataFrame with flat prices."""
        df = pd.DataFrame({"Close": [3, 3, 3, 3]}, 
                          index=pd.date_range("2024-01-01", periods=4))
        result_df, profit, buy_signals = max_profit_calculation(df)

        assert profit == 0
        assert buy_signals == 0
        assert any(result_df["Buy_Signal"]) == False

    def test_mixed_prices(self):
        """Test case for a DataFrame with mixed price movements."""
        # Prices go up (profit) then down (no profit), then up again (profit)
        df = pd.DataFrame({"Close": [1, 3, 2, 4]}, 
                          index=pd.date_range("2024-01-01", periods=4))
        result_df, profit, buy_signals = max_profit_calculation(df.copy())

        assert profit == 4
        assert buy_signals == 2
        assert result_df["Buy_Signal"].iloc[0] == True
        assert result_df["Buy_Signal"].iloc[2] == True

class Test_calculate_daily_returns:
    
    @patch("src.ticker_utils.convert_current_prices_to_sgd")
    @patch("src.ticker_utils.resolve_unknown_currency")
    @patch("src.ticker_utils.categorize_tickers")
    @patch("src.analytics.yf.download")
    def test_successful_returns_calculation(self, mock_download, mock_categorize, mock_resolve, mock_convert):
        "Test successful daily return calculation for multiple tickers."
        
        tickers = ["AAPL","TSLA"]
        df_input = pd.DataFrame({"ticker": tickers})
        
        # Mock yfinance data (multiIndex)
        mock_data = pd.concat({
            "AAPL": pd.DataFrame({"Close": [100, 110]}),
            "TSLA": pd.DataFrame({"Close": [200, 180]})
        }, axis=1)
        mock_download.return_value = mock_data
        

        # Mock currency mapping
        mock_categorize.return_value = {"AAPL": "USD", "TSLA": "USD"}
        mock_resolve.return_value = {"AAPL": "USD", "TSLA": "USD"}
        mock_convert.return_value = {
            "AAPL": {"price_sgd": 150.0, "currency": "SGD"},
            "TSLA": {"price_sgd": 250.0, "currency": "SGD"},
        }
        
        result = calculate_daily_returns(df_input)
        print(result)
        # --- Assert statements ---
        assert "AAPL" in result
        assert "TSLA" in result
        assert result["AAPL"]["daily_return"] == 10.0
        assert result["TSLA"]["daily_return"] == -10.0

    @patch("src.analytics.yf.download", side_effect=Exception("API Error"))
    def test_yfinance_failure(self, mock_download):
        "Test function gracefully handles API failure."
        df_input = pd.DataFrame({"ticker": ["AAPL"]})
        result = calculate_daily_returns(df_input)
        assert isinstance(result,dict)
        assert result == {}
        
        mock_download.assert_called_once()
        
    