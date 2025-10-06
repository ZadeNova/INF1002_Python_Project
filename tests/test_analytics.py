


import pytest
from unittest.mock import patch
import pandas as pd
from src.analytics import *





class Test_upward_downward_runs:

    def test_all_upward_trend(self):
        df = pd.DataFrame({"Close": [1, 2, 3, 4, 5]}, 
                          index=pd.date_range("2024-01-01", periods=5))
        result_df, longest_up, longest_down = calculate_upward_and_Downward_runs(df)

        assert longest_up["length"] == 4
        assert longest_down["length"] == 0
        assert longest_up["start"] == result_df.index[0]
        assert longest_up["end"] == result_df.index[-1]


    
    def test_all_downward_trend(self):
        df = pd.DataFrame({"Close":[10,8,7,3,1]},
                          index=pd.date_range("2024-01-01", periods=5))
        result_df, longest_up, longest_down = calculate_upward_and_Downward_runs(df)

        assert longest_down["length"] == 4
        assert longest_up["length"] == 0
        assert longest_down["start"] == result_df.index[0]
        assert longest_down["end"] == result_df.index[-1]


    def test_no_trend_flat_prices(self):
        df = pd.DataFrame({"Close": [5, 5, 5, 5]}, 
                          index=pd.date_range("2024-01-01", periods=4))
        result_df, longest_up, longest_down = calculate_upward_and_Downward_runs(df)

        assert longest_up["length"] == 0
        assert longest_down["length"] == 0
        assert longest_down["start"] == None
        assert longest_down["end"] == None


    def test_mixed_trends(self):
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
        df = pd.DataFrame({"Close": [1,2,3,4,5]}
                          , index=pd.date_range("2024-01-01", periods=5))
        
        result_df, profit, buy_signal = max_profit_calculation(df)

        assert profit == 4
        assert buy_signal == 4
    
    def test_decreasing_prices(self):
        df = pd.DataFrame({"Close": [5,4,3,2,1]}
                          , index=pd.date_range("2024-01-01", periods=5))
        
        result_df, profit, buy_signal = max_profit_calculation(df)

        assert profit == 0
        assert buy_signal == 0


    def test_flat_prices(self):
        df = pd.DataFrame({"Close": [3, 3, 3, 3]}, 
                          index=pd.date_range("2024-01-01", periods=4))
        result_df, profit, buy_signals = max_profit_calculation(df)

        assert profit == 0
        assert buy_signals == 0
        assert any(result_df["Buy_Signal"]) == False

    def test_mixed_prices(self):
        # Prices go up (profit) then down (no profit), then up again (profit)
        df = pd.DataFrame({"Close": [1, 3, 2, 4]}, 
                          index=pd.date_range("2024-01-01", periods=4))
        result_df, profit, buy_signals = max_profit_calculation(df.copy())

        assert profit == 4
        assert buy_signals == 2
        assert result_df["Buy_Signal"].iloc[0] == True
        assert result_df["Buy_Signal"].iloc[2] == True


    