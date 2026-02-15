from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
from app.services.asset_context import asset_context
from app.services.decision_engine import DecisionEngine
from app.services.feature_engine import FeatureEngine
from app.services.market_hours import get_market_status_ist
from app.services.connection_manager import manager as conn_manager
from app.services.market_levels import MarketLevels
from app.services.expert_engine import ExpertEngine
from app.services.candle_aggregator import CandleAggregator
from app.services.market_predictor import MarketPredictor

router = APIRouter()

@router.get("/latest")
async def get_latest_signal() -> Dict[str, Any]:
    """
    Get the latest computed signal for the CURRENT asset.
    """
    # 1. Get current asset context
    asset = asset_context.current_asset
    connector = asset_context.get_connector()
    symbol = asset_context.get_symbol()
    
    # 2. Market Status (NIFTY only)
    market_status = {"is_open": True, "status": "OPEN"}
    if asset == "NIFTY":
        market_status = get_market_status_ist()

    # 3. Fetch Data (Real-time for free edition)
    try:
        # Binance needs 500 candles for good EMA200
        limit = 500 if asset == "BITCOIN" else 200
        interval = "1m" if asset == "BITCOIN" else "5m"
        
        candles = await connector.get_historical_candles(symbol, "15m" if asset == "BITCOIN" else "5m", 100)
        print(f"Signals Endpoint: Fetched {len(candles)} candles for {asset}")
        latest_price = await connector.get_latest_price(symbol)
        
        if latest_price == 0 and candles:
             latest_price = candles[-1].close
             
    except Exception as e:
        return {
            "status": "ERROR", 
            "message": str(e), 
            "asset": asset,
            "market_status": market_status
        }

    # 4. Compute Features
    features = FeatureEngine.calculate_technical_indicators(candles, asset_type=asset)
    
    # 5. Compute Decision (Pass market status)
    decision = DecisionEngine.analyze(features, asset_type=asset, is_market_open=market_status["is_open"])

    return {
        "asset": asset,
        "price": latest_price,
        "signal": decision,
        "market_status": market_status,
        "timestamp": candles[-1].timestamp if candles else None,
        "provider": "Binance Public API" if asset == "BITCOIN" else "Yahoo Finance"
    }

@router.post("/toggle")
async def toggle_asset(asset: str) -> Dict[str, str]:
    """
    Switch the active asset (NIFTY / BITCOIN).
    """
    try:
        asset_context.set_asset(asset.upper())
        return {"status": "success", "current_asset": asset_context.current_asset}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/context")
async def get_context() -> Dict[str, Any]:
    return {
        "current_asset": asset_context.current_asset,
        "supported_assets": ["NIFTY", "BITCOIN"]
    }

@router.get("/levels")
async def get_market_levels(asset: str = "NIFTY") -> Dict[str, Any]:
    """
    Returns Support/Resistance levels based on Daily Pivots.
    """
    # Quick connector logical lookup (in real app, use factory)
    from app.services.connectors.binance_connector import BinanceConnector
    from app.services.connectors.yfinance_connector import YFinanceConnector
    
    if asset == "NIFTY":
        symbol = "^NSEI"
        connector = YFinanceConnector()
    else:
        symbol = "BTCUSDT"
        connector = BinanceConnector()
        
    return await MarketLevels.get_daily_pivots(connector, symbol)

@router.get("/expert")
async def get_expert_commentary(asset: str = "NIFTY") -> Dict[str, Any]:
    """
    Returns deterministic expert commentary.
    """
    from app.services.connectors.binance_connector import BinanceConnector
    from app.services.connectors.yfinance_connector import YFinanceConnector
    
    # 1. Setup Context
    if asset == "NIFTY":
        symbol = "^NSEI"
        connector = YFinanceConnector()
        market_status = get_market_status_ist()
    else:
        symbol = "BTCUSDT"
        connector = BinanceConnector()
        market_status = {"is_open": True, "status": "OPEN"}

    try:
        # 2. Fetch Data
        candles = await connector.get_historical_candles(symbol, "15m" if asset == "BITCOIN" else "5m", 100)
        latest_price = await connector.get_latest_price(symbol)
        
        if not candles:
             return {"error": "Insufficient data for expert analysis"}

        # 3. Compute Features & Decision
        features = FeatureEngine.calculate_technical_indicators(candles, asset_type=asset)
        decision = DecisionEngine.analyze(features, asset_type=asset, is_market_open=market_status["is_open"])
        
        # 4. Get Levels
        levels = await MarketLevels.get_daily_pivots(connector, symbol)
        
        # 5. Generate Commentary
        commentary = ExpertEngine.generate_commentary(asset, latest_price, decision, levels)
        
        return commentary
    except Exception as e:
        print(f"Error generating expert commentary: {e}")
        return {"error": str(e)}
@router.get("/candles")
async def get_market_candles(asset: str = "NIFTY", tf: str = "5m") -> List[Dict[str, Any]]:
    """
    Returns aggregated candlesticks for charts.
    Supported tf: 1m, 2m, 3m, 5m, 10m, 15m, 30m, 1h, 2h, 1d
    """
    from app.services.connectors.binance_connector import BinanceConnector
    from app.services.connectors.yfinance_connector import YFinanceConnector
    
    if asset == "NIFTY":
        symbol = "^NSEI"
        connector = YFinanceConnector()
        # Yahoo supports: 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo
        # We need to map requested TF to a base TF we can fetch, then aggregate if needed.
        # Simple strategy: Fetch 1m if target < 5m, else 5m if target < 15m, else 15m...
        # For simplicity in this iteration: Fetch 1m or 5m base.
        # Determine base timeframe and limit based on requested tf
        if tf in ['1m', '2m', '3m', '5m']:
            base_tf = "1m"
            limit = 500 # Aggr 5m from 1m needs 5x candles
        elif tf in ['10m', '15m', '30m']:
            base_tf = "5m"
            limit = 300 # Aggr 30m from 5m needs 6x candles
        elif tf in ['1h', '2h']:
            base_tf = "60m" # Yahoo uses 60m
            limit = 200
        else: # 1d
            base_tf = "1d"
            limit = 100
    else:
        symbol = "BTCUSDT"
        connector = BinanceConnector()
        # For Bitcoin, we can just fetch close to what we need
        # But our aggregator works best with granular data
        if tf in ['1d']:
            base_tf = "1d"
            limit = 100
        elif tf in ['1h', '2h']:
            base_tf = "1h"
            limit = 200
        else:
            base_tf = "1m"
            limit = 1000

    try:
        # Fetch base candles
        # Note: YF 1m data is limited to 7 days.
        candles = await connector.get_historical_candles(symbol, base_tf, limit)
        
        # Aggregate
        aggregated = CandleAggregator.aggregate_candles(candles, tf)
        
        return aggregated
    except Exception as e:
        print(f"Error serving candles: {e}")
        return []

@router.get("/predict")
async def get_market_open_prediction(asset: str = "NIFTY") -> Dict[str, Any]:
    """
    Predicts next market open for NIFTY when market is closed.
    Returns empty dict if market is open or asset is not NIFTY.
    """
    from app.services.connectors.yfinance_connector import YFinanceConnector
    from app.services.market_predictor import MarketPredictor
    
    # Only for NIFTY
    if asset != "NIFTY":
        return {}
    
    # Check if market is closed
    market_status = get_market_status_ist()
    if market_status.get("is_open", True):
        return {}
    
    try:
        symbol = "^NSEI"
        connector = YFinanceConnector()
        
        # Fetch last session data
        candles = await connector.get_historical_candles(symbol, "1d", 5)
        if not candles or len(candles) < 1:
            return {"error": "Insufficient historical data"}
        
        last_candle = candles[-1]
        
        # Get current decision and levels
        features = FeatureEngine.calculate_technical_indicators(candles, asset_type="NIFTY")
        decision = DecisionEngine.analyze(features, asset_type="NIFTY", is_market_open=False)
        levels = await MarketLevels.get_daily_pivots(connector, symbol)
        
        # Generate prediction
        prediction = MarketPredictor.predict_open(
            last_close=last_candle.close,
            last_high=last_candle.high,
            last_low=last_candle.low,
            levels=levels,
            decision=decision
        )
        
        return prediction
    except Exception as e:
        print(f"Error predicting market open: {e}")
        return {"error": str(e)}
