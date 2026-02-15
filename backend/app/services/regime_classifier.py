from typing import Dict, Any

class RegimeClassifier:
    """
    Classifies the market into one of the following regimes:
    - TRENDING_BULLISH
    - TRENDING_BEARISH
    - RANGE_BOUND
    - VOLATILE_NEWS
    """

    @staticmethod
    def classify(features: Dict[str, float], news_impact_score: float = 0) -> Dict[str, Any]:
        regime = "RANGE_BOUND"
        confidence = 0.0
        details = []

        adx = features.get('adx', 0)
        atr = features.get('atr', 0)
        ema_20 = features.get('ema_20', 0)
        ema_50 = features.get('ema_50', 0)
        close = features.get('close', 0)

        # 1. Check for High Volatility / News Event
        if news_impact_score > 70 or atr > (close * 0.01): # Example 1% ATR threshold
            regime = "VOLATILE_NEWS"
            confidence = 80.0
            details.append("High volatility or significant news impact detected.")
            return {"regime": regime, "confidence": confidence, "details": details}

        # 2. Check for Trend
        if adx > 25:
            if close > ema_20 > ema_50:
                regime = "TRENDING_BULLISH"
                confidence = 70.0 + (adx - 25) # Increase condifence with trend strength
                details.append(f"Strong uptrend (ADX {adx:.1f}). Price above EMAs.")
            elif close < ema_20 < ema_50:
                regime = "TRENDING_BEARISH"
                confidence = 70.0 + (adx - 25)
                details.append(f"Strong downtrend (ADX {adx:.1f}). Price below EMAs.")
        
        # 3. Default to Range
        if regime == "RANGE_BOUND":
             confidence = 60.0
             details.append("Low ADX indicates sideways market.")

        return {
            "regime": regime, 
            "confidence": min(confidence, 100.0), 
            "details": details
        }
