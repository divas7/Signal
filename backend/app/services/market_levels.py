from typing import Dict, Any, Optional
from datetime import datetime
import pandas as pd
from app.services.connector_interface import MarketDataConnector
from app.schemas.market_data import MarketCandle

class MarketLevels:
    """
    Calculates Pivot Points (Classic) and Support/Resistance levels.
    """
    
    @staticmethod
    def calculate_pivots(high: float, low: float, close: float) -> Dict[str, float]:
        """
        Classic Pivot Point Formula:
        P = (H + L + C) / 3
        R1 = 2P - L
        S1 = 2P - H
        R2 = P + (H - L)
        S2 = P - (H - L)
        R3 = H + 2(P - L)
        S3 = L - 2(H - P)
        """
        p = (high + low + close) / 3
        r1 = (2 * p) - low
        s1 = (2 * p) - high
        r2 = p + (high - low)
        s2 = p - (high - low)
        r3 = high + 2 * (p - low)
        s3 = low - 2 * (high - p)
        
        return {
            "p": round(p, 2),
            "r1": round(r1, 2),
            "s1": round(s1, 2),
            "r2": round(r2, 2),
            "s2": round(s2, 2),
            "r3": round(r3, 2),
            "s3": round(s3, 2)
        }

    @staticmethod
    async def get_daily_pivots(connector: MarketDataConnector, symbol: str) -> Dict[str, Any]:
        """
        Fetches previous day's candle and calculates pivots.
        """
        try:
            # Fetch last 2 daily candles to ensure we have the completed previous day
            candles = await connector.get_historical_candles(symbol, "1d", 2)
            
            if not candles or len(candles) < 2:
                # Fallback if only 1 candle (e.g. new listing or data issue) or empty
                if len(candles) == 1:
                     target_candle = candles[0]
                else:
                    return {}
            else:
                 # Use the second to last candle (completed previous day)
                 # The last candle is usually the "current/forming" day
                 target_candle = candles[-2]

            pivots = MarketLevels.calculate_pivots(
                target_candle.high, 
                target_candle.low, 
                target_candle.close
            )
            
            return {
                "basis": "Daily (Previous Day)",
                "date": target_candle.timestamp.strftime("%Y-%m-%d"),
                "levels": pivots
            }
            
        except Exception as e:
            print(f"Error calculating pivots for {symbol}: {e}")
            return {}
