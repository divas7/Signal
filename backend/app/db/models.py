from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, JSON
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class MarketCandleModel(Base):
    __tablename__ = "market_candles"
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    timestamp = Column(DateTime, index=True)
    interval = Column(String)  # 1m, 5m, etc.
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Integer)
    source = Column(String)

class OptionChainSnapshot(Base):
    __tablename__ = "option_chain_snapshots"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, index=True)
    expiry = Column(DateTime, index=True)
    spot_price = Column(Float)
    source = Column(String)
    data = Column(JSON)  # Store the full chain as JSON for now to avoid massive normalization overhead

class NewsItemModel(Base):
    __tablename__ = "news_items"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, index=True)
    source = Column(String)
    title = Column(String)
    url = Column(String, unique=True)
    category = Column(String)
    sentiment = Column(Float)
    entities = Column(JSON)
    allowed = Column(Boolean, default=False)

class SignalLog(Base):
    __tablename__ = "signal_logs"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    action = Column(String)  # BUY, SELL, NO_TRADE
    bias = Column(String)
    strategy_type = Column(String)
    confidence = Column(Float)
    rationale = Column(JSON)
    rules_version = Column(String)
    model_version = Column(String)
