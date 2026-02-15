from datetime import datetime, timedelta
from app.schemas.market_data import MarketCandle, OptionChain

class DataValidator:
    @staticmethod
    def is_spot_fresh(candle: MarketCandle, max_age_seconds: int = 6) -> bool:
        """Check if spot price is fresh (<= 6s)."""
        age = datetime.utcnow() - candle.timestamp
        return age.total_seconds() <= max_age_seconds

    @staticmethod
    def is_chain_fresh(chain: OptionChain, max_age_seconds: int = 10) -> bool:
        """Check if options chain is fresh (<= 10s)."""
        age = datetime.utcnow() - chain.timestamp
        return age.total_seconds() <= max_age_seconds

    @staticmethod
    def validate_liquidity(chain: OptionChain, min_volume: int = 100) -> bool:
        """Check if there is sufficient liquidity."""
        # This is a simplified check. Real check would look at ATM volume.
        total_volume = sum(c.volume for c in chain.contracts)
        return total_volume >= min_volume

class StaleDataError(Exception):
    """Raised when data is too old to be reliable."""
    pass
