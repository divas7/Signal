import httpx
from typing import List
from datetime import datetime
from app.services.connector_interface import MarketDataConnector
from app.schemas.market_data import MarketCandle

class BinanceConnector(MarketDataConnector):
    """
    Fetches real-time data from Binance via direct HTTP requests (Public API).
    Robust against CCXT/SSL issues in some environments.
    """
    def __init__(self):
        self.base_url = "https://api.binance.com/api/v3"
        self.client = httpx.AsyncClient(timeout=10.0, verify=False, follow_redirects=True)

    async def get_latest_price(self, symbol: str) -> float:
        # symbol needs to be simpler for raw API, e.g. "BTC/USDT" -> "BTCUSDT"
        clean_symbol = symbol.replace("/", "").upper()
        try:
            response = await self.client.get(f"{self.base_url}/ticker/price", params={"symbol": clean_symbol})
            if response.status_code == 200:
                data = response.json()
                return float(data['price'])
            else:
                print(f"Error fetching Binance price: {response.status_code} {response.text}")
                return 0.0
        except Exception as e:
            print(f"Exception fetching Binance price for {symbol}: {e}")
            return 0.0

    async def get_historical_candles(self, symbol: str, interval: str, limit: int) -> List[MarketCandle]:
        clean_symbol = symbol.replace("/", "").upper()
        try:
            # klines: [Open time, Open, High, Low, Close, Volume, Close time, ...]
            response = await self.client.get(f"{self.base_url}/klines", params={
                "symbol": clean_symbol,
                "interval": interval,
                "limit": limit
            })
            
            if response.status_code == 200:
                data = response.json()
                candles = []
                for kline in data:
                    # kline[0] is Open Time in ms
                    ts = kline[0]
                    o = float(kline[1])
                    h = float(kline[2])
                    l = float(kline[3])
                    c = float(kline[4])
                    v = float(kline[5])
                    
                    candles.append(MarketCandle(
                        timestamp=datetime.fromtimestamp(ts / 1000.0),
                        open=o,
                        high=h,
                        low=l,
                        close=c,
                        volume=v,
                        source="binance"
                    ))
                return candles
            else:
                print(f"Error fetching Binance candles: {response.status_code} {response.text}")
                return []
        except Exception as e:
            print(f"Exception fetching Binance history for {symbol}: {e}")
            return []
    
    async def close(self):
        await self.client.aclose()
