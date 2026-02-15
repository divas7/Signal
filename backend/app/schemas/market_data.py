from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class MarketCandle(BaseModel):
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float
    source: str

class OptionContract(BaseModel):
    strike: float
    option_type: str  # CE or PE
    ltp: float
    iv: float
    oi: int
    oi_change: int
    volume: int
    bid: Optional[float]
    ask: Optional[float]
    timestamp: datetime
    source: str

class OptionChain(BaseModel):
    timestamp: datetime
    expiry: datetime
    spot_price: float
    contracts: List[OptionContract]
    source: str

class NewsItem(BaseModel):
    timestamp: datetime
    source: str
    title: str
    url: str
    category: str
    sentiment: float
    entities: List[str]
    allowed: bool
