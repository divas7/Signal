from typing import Dict, Any, List
from datetime import datetime
from datetime import datetime

class ExpertEngine:
    """
    Deterministic engine to generate expert commentary based on technical indicators and levels.
    No LLM hallucination - purely rule-based logic.
    """

    @staticmethod
    def generate_commentary(
        asset: str, 
        current_price: float, 
        decision: Dict[str, Any], 
        levels: Dict[str, Any]
    ) -> Dict[str, Any]:
        
        # Unpack inputs
        action = decision.get("action", "NO_TRADE")
        bias = decision.get("bias", "NEUTRAL")
        buy_conf = decision.get("buy_confidence", 0)
        sell_conf = decision.get("sell_confidence", 0)
        indicators = decision.get("indicators_snapshot", {})
        
        ema20 = indicators.get("ema_20", 0)
        ema50 = indicators.get("ema_50", 0)
        rsi = indicators.get("rsi", 50)
        
        # 1. Market Snapshot
        regime = "Range Bound"
        if abs(ema20 - ema50) > (current_price * 0.005): # Diverging EMAs
             regime = "Trending"
        if indicators.get("atr", 0) > (current_price * 0.01):
             regime = "High Volatility"

        snapshot_reasons = []
        if current_price > ema20:
            snapshot_reasons.append("Price > EMA20")
        else:
            snapshot_reasons.append("Price < EMA20")
            
        if rsi > 60:
            snapshot_reasons.append("Momentum Strong (RSI > 60)")
        elif rsi < 40:
            snapshot_reasons.append("Momentum Weak (RSI < 40)")
        else:
            snapshot_reasons.append("RSI Neutral")

        # 2. Key Levels Analysis
        nearest_support = None
        nearest_resistance = None
        min_dist_s = float('inf')
        min_dist_r = float('inf')
        
        if levels and "levels" in levels:
            pivots = levels["levels"]
            # Check supports
            for key in ["s1", "s2", "s3"]:
                s_val = pivots.get(key)
                if s_val and current_price > s_val:
                    dist = (current_price - s_val) / current_price
                    if dist < min_dist_s:
                        min_dist_s = dist
                        nearest_support = {"level": key.upper(), "value": s_val, "dist_pct": round(dist * 100, 2)}
            
            # Check resistances
            for key in ["r1", "r2", "r3"]:
                r_val = pivots.get(key)
                if r_val and current_price < r_val:
                    dist = (r_val - current_price) / current_price
                    if dist < min_dist_r:
                        min_dist_r = dist
                        nearest_resistance = {"level": key.upper(), "value": r_val, "dist_pct": round(dist * 100, 2)}
        
        # 3. What an expert would do
        expert_action = ""
        if bias == "BULLISH":
            expert_action = "Look for pullbacks to nearest support (EMA20 or S1) to enter. Confirm with volume."
        elif bias == "BEARISH":
            expert_action = "Sell rallies towards resistance (EMA20 or R1). Watch for rejection wicks."
        else:
            expert_action = "Market is choppy/neutral. Trade edges of the range (Buy S1, Sell R1) or wait for a breakout."

        # 4. If/Then Playbook
        playbook = []
        
        # Bullish Scenarios
        if nearest_resistance:
             playbook.append(f"IF price breaks above {nearest_resistance['level']} ({nearest_resistance['value']}) with volume -> THEN Bullish Continuation.")
        
        # Bearish Scenarios
        if nearest_support:
             playbook.append(f"IF price breaks below {nearest_support['level']} ({nearest_support['value']}) -> THEN Bearish Breakdown to next level.")
             
        # Reversal Scenarios
        if rsi > 70:
            playbook.append("IF RSI prints Bearish Divergence -> THEN Possible Reversal top.")
        elif rsi < 30:
            playbook.append("IF RSI prints Bullish Divergence -> THEN Possible Reversal bottom.")

        # 5. Risk Tip
        risk_tip = "Always use a stop loss."
        if regime == "High Volatility":
            risk_tip = "Volatility is high. Reduce position size and widen stops."
        if asset == "NIFTY" and not decision.get("market_status", {}).get("is_open", True):
             risk_tip = "Standard Market Closed. Use these levels for next session planning."

        # 6. Beginner-Friendly Summary
        beginner_summary = ""
        simple_action = ""
        
        if bias == "BULLISH":
            beginner_summary = f"The market is showing upward momentum. Price is above key averages and momentum is strong."
            if nearest_resistance:
                simple_action = f"Wait for a dip towards ₹{nearest_support['value'] if nearest_support else int(current_price * 0.98)} to buy, or wait for a clear break above ₹{nearest_resistance['value']} to confirm strength."
            else:
                simple_action = "Price is in an uptrend. Consider buying on small pullbacks."
        elif bias == "BEARISH":
            beginner_summary = f"The market is showing downward pressure. Price is below key levels and momentum is weak."
            if nearest_support:
                simple_action = f"Avoid buying. If you're trading, wait for price to break below ₹{nearest_support['value']} to confirm weakness, or wait for a bounce to ₹{nearest_resistance['value'] if nearest_resistance else int(current_price * 1.02)} to sell."
            else:
                simple_action = "Price is in a downtrend. Avoid buying or consider selling rallies."
        else:
            beginner_summary = "The market is moving sideways without clear direction. This is a choppy, uncertain phase."
            if nearest_support and nearest_resistance:
                simple_action = f"Best to wait and watch. If you must trade, buy near support (₹{nearest_support['value']}) and sell near resistance (₹{nearest_resistance['value']}). A breakout above ₹{nearest_resistance['value']} or below ₹{nearest_support['value']} will give clearer signals."
            else:
                simple_action = "Avoid trading until a clear trend emerges. Wait for a breakout signal."

        return {
            "beginner": {
                "summary": beginner_summary,
                "simple_action": simple_action
            },
            "snapshot": {
                "bias": bias,
                "regime": regime,
                "reasons": snapshot_reasons
            },
            "levels": {
                "nearest_support": nearest_support,
                "nearest_resistance": nearest_resistance,
                "all_levels": levels.get("levels", {})
            },
            "expert_action": expert_action,
            "playbook": playbook,
            "risk_tip": risk_tip,
            "timestamp": datetime.now().isoformat()
        }
