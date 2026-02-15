import yfinance as yf
from typing import List
from datetime import datetime
from app.services.connector_interface import MarketDataConnector
from app.schemas.market_data import MarketCandle

class YFinanceConnector(MarketDataConnector):
    """
    Fetches free data from Yahoo Finance.
    Mainly for NIFTY 50 (^NSEI).
    """
    async def get_latest_price(self, symbol: str) -> float:
        try:
            ticker = yf.Ticker(symbol)
            # fast_info is usually faster and live-ish
            return ticker.fast_info.last_price
        except Exception as e:
            print(f"Error fetching YF price for {symbol}: {e}")
            return 0.0

    async def get_historical_candles(self, symbol: str, interval: str, limit: int) -> List[MarketCandle]:
        try:
            # Map interval: 1m, 5m, 15m, 1h, 1d
            ticker = yf.Ticker(symbol)
            # YF requires 'period' if requesting recent data
            period = "1d" if interval in ["1m", "5m"] else "5d"
            
            df = ticker.history(period=period, interval=interval)
            
            candles = []
            for index, row in df.iterrows():
                # YF timestamp is index
                candles.append(MarketCandle(
                    timestamp=index.to_pydatetime(),
                    open=row['Open'],
                    high=row['High'],
                    low=row['Low'],
                    close=row['Close'],
                    volume=row.get('Volume', 0),
                    source="yfinance"
                ))
            
            # Return last 'limit' candles
            return candles[-limit:]
        except Exception as e:
            print(f"Error fetching YF history for {symbol}: {e}")
            return []
