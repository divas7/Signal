from typing import List, Dict, Any
import pandas as pd
from app.schemas.market_data import MarketCandle

class CandleAggregator:
    """
    Service to aggregate base candles into higher timeframes.
    Necessary for NIFTY free data (Yahoo) which may not provide 2m, 3m etc.
    """
    
    @staticmethod
    def aggregate_candles(candles: List[MarketCandle], target_tf: str) -> List[Dict[str, Any]]:
        """
        Aggregates base candles to target timeframe.
        target_tf format: '2m', '3m', '10m', '15m'
        """
        if not candles:
            return []
            
        # Convert to DataFrame
        data = [c.dict() for c in candles]
        df = pd.DataFrame(data)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.set_index('timestamp', inplace=True)
        
        # Parse timeframe string (e.g. '2m' -> '2T' for pandas)
        # Simple mapping for now
        tf_map = {
            '1m': '1T', '2m': '2T', '3m': '3T', '5m': '5T', 
            '10m': '10T', '15m': '15T', '30m': '30T', 
            '1h': '1H', '2h': '2H', '1d': '1D'
        }
        resample_rule = tf_map.get(target_tf, target_tf.replace('m', 'T').replace('d', 'D').replace('h', 'H'))

        # Resample logic
        # OHLCV aggregation
        agg_dict = {
            'open': 'first',
            'high': 'max',
            'low': 'min',
            'close': 'last',
            'volume': 'sum'
        }
        
        try:
            resampled = df.resample(resample_rule).agg(agg_dict).dropna()
        except Exception as e:
            print(f"Aggregation failed: {e}")
            return []
        
        # Convert back to list of dicts suitable for Lightweight Charts
        # LWC expects: { time: timestamp/string, open, high, low, close }
        results = []
        for time, row in resampled.iterrows():
            results.append({
                "time": int(time.timestamp()), # Unix timestamp for charts
                "open": row['open'],
                "high": row['high'],
                "low": row['low'],
                "close": row['close'],
                "volume": row['volume']
            })
            
        return results
