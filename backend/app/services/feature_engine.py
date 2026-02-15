import pandas as pd
# import pandas_ta as ta # Still avoiding due to install issues, using manual calc
from typing import List, Dict, Any
from app.schemas.market_data import MarketCandle, OptionChain

class FeatureEngine:
    """
    Computes technical indicators for NIFTY and BITCOIN.
    Handles asset-specific quirks (e.g. NIFTY volume often 0 in some feeds).
    """

    @staticmethod
    def calculate_technical_indicators(candles: List[MarketCandle], asset_type: str = "NIFTY") -> Dict[str, float]:
        if not candles:
            print("FeatureEngine: No candles provided.")
            return {}

        data_dicts = []
        for c in candles:
            # Pydantic v2 support
            if hasattr(c, 'model_dump'):
                data_dicts.append(c.model_dump())
            else:
                data_dicts.append(c.dict())

        df = pd.DataFrame(data_dicts)
        print(f"FeatureEngine: DF Shape: {df.shape}")
        
        if 'timestamp' in df.columns:
            df['datetime'] = pd.to_datetime(df['timestamp'])
        else:
             print("FeatureEngine: timestamp column missing!")
             return {}
             
        df.set_index('datetime', inplace=True)
        
        # Sort just in case
        df.sort_index(inplace=True)

        close = df['close']
        high = df['high']
        low = df['low']
        volume = df['volume']

        # Helpers for manual calculation (since pandas_ta is out)
        def calc_ema(series, span):
            return series.ewm(span=span, adjust=False).mean()

        def calc_rsi(series, period=14):
            delta = series.diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
            rs = gain / loss
            return 100 - (100 / (1 + rs))
        
        def calc_atr(df, period=14):
            high_low = df['high'] - df['low']
            high_close = (df['high'] - df['close'].shift()).abs()
            low_close = (df['low'] - df['close'].shift()).abs()
            ranges = pd.concat([high_low, high_close, low_close], axis=1)
            true_range = ranges.max(axis=1)
            return true_range.rolling(window=period).mean()

        # 1. EMA
        df['EMA_20'] = calc_ema(close, 20)
        df['EMA_50'] = calc_ema(close, 50)
        df['EMA_200'] = calc_ema(close, 200)

        # 2. RSI
        df['RSI_14'] = calc_rsi(close, 14)

        # 3. ATR
        df['ATR_14'] = calc_atr(df, 14)

        # 4. VWAP (Volume Weighted Average Price)
        # NIFTY free feeds often have 0 volume. BTC usually has volume.
        vwap = 0.0
        if volume.sum() > 0:
            cum_vol = volume.cumsum()
            cum_vol_price = (close * volume).cumsum()
            df['VWAP'] = cum_vol_price / cum_vol
            vwap = float(df.iloc[-1].get('VWAP', 0))

        # 5. Asset Specific Features
        # BTC: Order Imbalance / Funding Rate (Mocked/Simplified for free feed)
        
        latest = df.iloc[-1]

        return {
            "ema_20": float(latest.get('EMA_20', 0)),
            "ema_50": float(latest.get('EMA_50', 0)),
            "ema_200": float(latest.get('EMA_200', 0)),
            "rsi": float(latest.get('RSI_14', 50)),
            "atr": float(latest.get('ATR_14', 0)),
            "vwap": vwap,
            "close": float(latest['close']),
            "volume": float(latest['volume'])
        }

    @staticmethod
    def calculate_options_metrics(chain: OptionChain) -> Dict[str, Any]:
        """
        No-op/Placeholder for Free Edition if Options Chain data is missing.
        """
        return {}
