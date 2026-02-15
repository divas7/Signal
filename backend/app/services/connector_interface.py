from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime
from app.schemas.market_data import MarketCandle, OptionChain, NewsItem

class MarketDataConnector(ABC):
    @abstractmethod
    async def get_latest_price(self, symbol: str) -> float:
        """Get the latest price."""
        pass

    @abstractmethod
    async def get_historical_candles(self, symbol: str, interval: str, limit: int) -> List[MarketCandle]:
        """Get historical candles."""
        pass
    
    # Options Chain might be N/A for Free Edition or handled differently
    # We'll keep it as optional or raise NotImplementedError

class NewsConnector(ABC):
    @abstractmethod
    async def fetch_news(self) -> List[NewsItem]:
        """Fetch news from allowed sources."""
        pass
