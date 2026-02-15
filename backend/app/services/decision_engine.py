from typing import Dict, Any, List
from app.services.asset_context import asset_context

class DecisionEngine:
    """
    Multi-Asset Decision Engine.
    Produces BUY/SELL confidence separately.
    """

    @staticmethod
    def analyze(features: Dict[str, float], asset_type: str = "NIFTY", is_market_open: bool = True) -> Dict[str, Any]:
        action = "NEUTRAL"
        bias = "NEUTRAL"
        buy_confidence = 0.0
        sell_confidence = 0.0
        rationale = []

        close = features.get('close', 0)
        ema_20 = features.get('ema_20', 0)
        ema_50 = features.get('ema_50', 0)
        rsi = features.get('rsi', 50)
        vwap = features.get('vwap', 0)

        # Basic validation
        if close == 0:
            return {
                "action": "NEUTRAL",
                "bias": "NEUTRAL",
                "buy_confidence": 0,
                "sell_confidence": 0,
                "rationale": ["Price data missing or zero."]
            }

        # --- LOGIC ---
        
        # 1. Trend Analysis
        if close > ema_20:
            buy_confidence += 20
            rationale.append("Price above EMA20 (Short-term Bullish).")
        if ema_20 > ema_50:
            buy_confidence += 20
            rationale.append("EMA20 > EMA50 (Trend Alignment).")
        
        if close < ema_20:
            sell_confidence += 20
            rationale.append("Price below EMA20 (Short-term Bearish).")
        if ema_20 < ema_50:
            sell_confidence += 20
            rationale.append("EMA20 < EMA50 (Trend Alignment).")

        # 2. Momentum (RSI)
        if 50 < rsi < 70:
            buy_confidence += 10
            rationale.append("RSI Bullish Momentum (50-70).")
        elif rsi >= 70:
            sell_confidence += 30
            rationale.append("RSI Overbought (>70) - Partial Reversal Risk.")
        
        if 30 < rsi < 50:
            sell_confidence += 10
            rationale.append("RSI Bearish Momentum (30-50).")
        elif rsi <= 30:
            buy_confidence += 30
            rationale.append("RSI Oversold (<30) - Value Territory.")

        # 3. Asset Specifics
        if asset_type == "NIFTY":
            if not is_market_open:
                rationale.append("[WARN] Market Closed - Signals based on EOD/Last Tick.")
            
            # VWAP Logic (Intraday only)
            if is_market_open and vwap > 0:
                if close > vwap:
                    buy_confidence += 10
                    rationale.append("Price > VWAP (Intraday Strength).")
                else:
                    sell_confidence += 10
                    rationale.append("Price < VWAP (Intraday Weakness).")
        
        elif asset_type == "BITCOIN":
             # Crypto Volatility logic
             if rsi > 60 and close > ema_20:
                 buy_confidence += 10
                 rationale.append("Strong Crypto Momentum.")
             if rsi < 40 and close < ema_20:
                 sell_confidence += 10
                 rationale.append("Crypto Clean Breakdown.")

        # --- FINAL AGGREGATION ---
        
        # Cap confidence
        buy_confidence = min(buy_confidence, 100)
        sell_confidence = min(sell_confidence, 100)

        # Determine Signal
        if buy_confidence > 60 and buy_confidence > sell_confidence:
            action = "BUY"
            bias = "BULLISH"
        elif sell_confidence > 60 and sell_confidence > buy_confidence:
            action = "SELL"
            bias = "BEARISH"
        else:
            action = "NEUTRAL"
            bias = "NEUTRAL"
            rationale.append("Confidence below threshold or conflicting signals.")

        # OPTIONS SIGNAL (NIFTY only)
        options_signal = None
        intraday_volatility = 0
        
        if asset_type == "NIFTY":
            # Calculate volatility score (simple: RSI deviation from 50)
            intraday_volatility = abs(rsi - 50) * 2  # 0-100 scale
            
            # Options direction based on confidence spread
            if buy_confidence > sell_confidence + 15:
                options_signal = {
                    "direction": "CALL",
                    "confidence": min(buy_confidence, 85),
                    "reasoning": "Bullish momentum favors CALL options"
                }
            elif sell_confidence > buy_confidence + 15:
                options_signal = {
                    "direction": "PUT",
                    "confidence": min(sell_confidence, 85),
                    "reasoning": "Bearish momentum favors PUT options"
                }
            else:
                options_signal = {
                    "direction": "NEUTRAL",
                    "confidence": max(buy_confidence, sell_confidence),
                    "reasoning": "Mixed signals - consider straddles or avoid options"
                }

        result = {
            "action": action,
            "bias": bias,
            "buy_confidence": buy_confidence,
            "sell_confidence": sell_confidence,
            "rationale": rationale,
            "indicators_snapshot": features
        }
        
        # Add NIFTY-specific fields
        if options_signal:
            result["options_signal"] = options_signal
            result["intraday_volatility"] = intraday_volatility
            
        return result
