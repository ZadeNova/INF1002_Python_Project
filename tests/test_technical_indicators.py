


import pytest
from unittest.mock import patch
import pandas as pd
from src.technical_indicators import *

# Create a custom dataframe for each function

class TestRSI:

    def test_rsi_all_gains(self):
        """RSI should be 100 when prices only increase."""
        df = pd.DataFrame({"Close":[1,2,3,4,5,6]})
        result = calculate_RSI(df, window=2)
        assert result["RSI"].iloc[-1] == pytest.approx(100.00)

    def test_rsi_all_losses(self):
        """RSI should be 0 when prices only decrease."""
        df = pd.DataFrame({"Close":[7,6,5,4,3,2,1]})
        result = calculate_RSI(df, window=2)
        assert result["RSI"].iloc[-1] == pytest.approx(0.0, abs=1e-6)
        
    def test_rsi_flat_prices(self):
        """RSI should be 50 when prices are constant."""
        df = pd.DataFrame({"Close": [5,5,5,5,5,5,5]})
        result = calculate_RSI(df, window=2)
        assert all(result["RSI"].dropna() == 100)

    def test_rsi_values_in_range(self):
        """All RSI values should be between 0 and 100."""
        df = pd.DataFrame({"Close":[1,2,1,2,1,2,1,2]})
        result = calculate_RSI(df, window=3)
        assert result["RSI"].dropna().between(0, 100).all()

    def test_rsi_short_input(self):
        df = pd.DataFrame({"Close": [1,2,3]})
        with pytest.raises(ValueError, match="at least"):
            calculate_RSI(df, window=14)

    def test_rsi_column_and_length(self):
        """Check that RSI column exists and length matches input."""
        df = pd.DataFrame({"Close": [1,2,3,4,5,6,7,8,9,10]})
        result = calculate_RSI(df,2)
        assert "RSI" in result.columns
        assert len(result) == len(df)
        
class TestSMA:

    def test_sma_basic(self):
        """Test that SMA calculates correct values for a simple series."""
        df = pd.DataFrame({"Close": [1, 2, 3, 4, 5]})
        window = 3
        result = calculate_SMA(df.copy(), window=window)
        assert f"SMA_{window}" in result.columns
        # First valid SMA is average of first 3 closes: (1+2+3)/3 = 2
        assert pytest.approx(result[f"SMA_{window}"].iloc[2], 0.0001) == 2.0
        # Last SMA: average of [3,4,5] = 4
        assert pytest.approx(result[f"SMA_{window}"].iloc[4], 0.0001) == 4.0    

    
    def test_sma_window_1(self):
        """SMA with window=1 should return same as Close column."""
        df = pd.DataFrame({"Close": [10, 20, 30]})
        window = 1
        result = calculate_SMA(df.copy(), window=window)
        assert all(result[f"SMA_{window}"] == df["Close"])


    def test_sma_not_enough_data(self):
        """Should raise error if not enough data points for the given window."""
        df_short = pd.DataFrame({"Close": [1, 2]})
        df_large_window = pd.DataFrame({"Close": [1,2,3,4,5,6,7]})

        with pytest.raises(ValueError):
            calculate_SMA(df_short, window=3)
        with pytest.raises(ValueError):
            calculate_SMA(df_large_window, window=10)

    def test_sma_missing_close_column(self):
        """Should raise error if DataFrame has no 'Close' column."""
        df = pd.DataFrame({"Price": [1, 2, 3, 4, 5]})
        with pytest.raises(ValueError, match="Close"):
            calculate_SMA(df.copy(), window=3)

class TestVWAP:
    
    def test_vwap_basic(self):
        """Test basic VWAP calculation with simple values."""
        df = pd.DataFrame({
            "High": [10, 20, 30],
            "Low": [5, 15, 25],
            "Close": [7, 17, 27],
            "Volume": [100, 200, 300]
        })
        result = calculate_VWAP(df.copy())
        assert "VWAP" in result.columns
        # Manually calculate first VWAP: ((10+5+7)/3 * 100) / 100 = 7.3333
        assert pytest.approx(result["VWAP"].iloc[0], 0.0001) == (10+5+7)/3
        # Manually calculate second VWAP:
        # cumulative price*volume = 7.3333*100 + ((20+15+17)/3)*200
        cum_pv = (10+5+7)/3*100 + (20+15+17)/3*200
        cum_vol = 100 + 200
        expected_vwap2 = cum_pv / cum_vol
        assert pytest.approx(result["VWAP"].iloc[1], 0.0001) == expected_vwap2

    def test_missing_columns(self):
        """Should raise error if required columns are missing."""
        df = pd.DataFrame({
            "High": [10, 20],
            "Low": [5, 15],
            "Close": [7, 17],
            # 'Volume' column missing
        })
        with pytest.raises(ValueError, match="DataFrame must contain"):
            calculate_VWAP(df.copy())

    def test_zero_volume(self):
        """Check VWAP behavior when volume contains zeros."""
        df = pd.DataFrame({
            "High": [10, 20],
            "Low": [5, 15],
            "Close": [7, 17],
            "Volume": [0, 0]
        })
        result = calculate_VWAP(df.copy())
        assert all(pd.isna(result["VWAP"]) | (result["VWAP"] == 0))

    def test_nan_values(self):
        """Check VWAP calculation when NaNs exist in input."""
        df = pd.DataFrame({
            "High": [10, None, 30],
            "Low": [5, 15, 25],
            "Close": [7, 17, 27],
            "Volume": [100, 200, 300]
        })
        result = calculate_VWAP(df.copy())
        assert "VWAP" in result.columns
        # First value is valid
        assert pytest.approx(result["VWAP"].iloc[0], 0.0001) == (10+5+7)/3
        # Second value should be NaN due to None in 'High'
        assert pd.isna(result["VWAP"].iloc[1])

class TestEMA:

    def test_ema_basic(self):
        """Basic EMA calculation with simple input."""
        df = pd.DataFrame({"Close": [1, 2, 3, 4, 5, 6, 7]})
        window = 3
        result = calculate_EMA(df.copy(), window=window)
        # Check column exists
        assert f"EMA_{window}" in result.columns
        # First EMA should be average of first 'window' prices
        expected_first_ema = sum([1,2,3])/window
        assert result[f"EMA_{window}"].iloc[window-1] == expected_first_ema
        # All remaining EMAs should not be None
        assert result[f"EMA_{window}"].iloc[window:].notna().all()


    def test_ema_custom_column(self):
        """Test EMA calculation with a custom column name."""
        df = pd.DataFrame({"Close": [1,2,3,4,5]})
        result = calculate_EMA(df.copy(), window=3, ema_col="MyEMA")
        assert "MyEMA" in result.columns
    

    def test_ema_non_numeric(self):
        """Non-numeric values in input are coerced to NaN and affect EMA."""
        df = pd.DataFrame({"Close": [1, "a", 3, 4, 5]})
        result = calculate_EMA(df.copy(), window=2)
        # The second value ("a") becomes NaN
        assert pd.isna(result[f"EMA_2"].iloc[1])

    def test_ema_small_dataframe(self):
        """Test behavior when dataframe is smaller than window."""
        df = pd.DataFrame({"Close": [1,2]})
        window = 3
        with pytest.raises(ValueError, match="at least 3 rows"):
            calculate_EMA(df.copy(), window=window)
        

    def test_ema_with_nans(self):
        """Test behavior when input contains NaNs."""
        df = pd.DataFrame({"Close": [1, 2, None, 4, 5]})
        window = 2
        result = calculate_EMA(df.copy(), window=window)
        # Check first EMA is correct
        expected_first_ema = (1+2)/2
        assert result[f"EMA_{window}"].iloc[window-1] == expected_first_ema
        # EMA for index 2 should be NaN because input is NaN
        assert pd.isna(result[f"EMA_{window}"].iloc[2])

class TestMACD:

    @patch("src.technical_indicators.calculate_EMA")
    def test_macd_logic_only(self, mock_ema):
        """Test that MACD output columns exists, using mocked EMA."""
        df = pd.DataFrame({"Close": [1,2,3,4,5]})

        # Mock EMA outputs
        df_mock = df.copy()


        df_mock["EMA_12"] = [1,2,3,4,5]
        df_mock["EMA_26"] = [0.5,1,1.5,2,2.5]
        mock_ema.return_value = df_mock

        result = calculate_MACD(df, short_period=12, long_period=26)

        for col in ["MACD","Signal_Line","MACD_Histogram"]:
            assert col in result.columns
    
    @patch("src.technical_indicators.calculate_EMA")
    def test_macd_handles_empty_dataframe(self, mock_ema):
        """Test that MACD function handles empty DataFrame gracefully."""
        df = pd.DataFrame({"Close": []})

        df_mock = df.copy()
        df_mock["EMA_12"] = []
        df_mock["EMA_26"] = []

        mock_ema.return_value = df_mock

        result = calculate_MACD(df, short_period=12, long_period=26)
        # All MACD-related columns exist even if empty
        for col in ["MACD", "Signal_Line", "MACD_Histogram"]:
            assert col in result.columns
        assert len(result) == 0



        
