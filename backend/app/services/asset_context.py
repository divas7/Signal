from typing import Optional
from app.services.connector_interface import MarketDataConnector
from app.services.connectors.yfinance_connector import YFinanceConnector
from app.services.connectors.binance_connector import BinanceConnector

class AssetContext:
    """
    Manages the current asset context (NIFTY or BITCOIN).
    Provides the appropriate connector and settings.
    """
    def __init__(self):
        self._current_asset = "NIFTY" # Default
        self._connectors = {
            "NIFTY": YFinanceConnector(),
            "BITCOIN": BinanceConnector()
        }
        self._symbols = {
            "NIFTY": "^NSEI",
            "BITCOIN": "BTC/USDT"
        }
        self._update_intervals = {
            "NIFTY": 15, # Yahoo Finance is slower
            "BITCOIN": 3 # Binance is fast
        }

    @property
    def current_asset(self) -> str:
        return self._current_asset

    def set_asset(self, asset: str):
        if asset not in self._connectors:
            raise ValueError(f"Unknown asset: {asset}")
        self._current_asset = asset

    def get_connector(self) -> MarketDataConnector:
        return self._connectors[self._current_asset]

    def get_symbol(self) -> str:
        return self._symbols[self._current_asset]
    
    def get_update_interval(self) -> int:
        return self._update_intervals[self._current_asset]

asset_context = AssetContext()
