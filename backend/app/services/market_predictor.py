from typing import Dict, Any
from datetime import datetime

class MarketPredictor:
    """
    Predicts NIFTY market opening based on overnight momentum and technical levels.
    Pure deterministic logic - no external news APIs.
    """
    
    @staticmethod
    def predict_open(
        last_close: float,
        last_high: float,
        last_low: float,
        levels: Dict[str, Any],
        decision: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Predicts market open direction and level.
        
        Args:
            last_close: Previous day's closing price
            last_high: Previous day's high
            last_low: Previous day's low
            levels: Support/Resistance levels
            decision: Latest decision engine output
        """
        
        # 1. Analyze previous session behavior
        daily_range = last_high - last_low
        close_position = (last_close - last_low) / daily_range if daily_range > 0 else 0.5
        
        # 2. Momentum analysis
        bias = decision.get("bias", "NEUTRAL")
        buy_conf = decision.get("buy_confidence", 0)
        sell_conf = decision.get("sell_confidence", 0)
        
        # 3. Predict gap direction
        gap_direction = "FLAT"
        gap_pct = 0
        predicted_open = last_close
        confidence = 50
        reasons = []
        
        # Strong momentum continuation
        if bias == "BULLISH" and buy_conf > 70:
            if close_position > 0.7:  # Closed near high
                gap_direction = "UP"
                gap_pct = 0.3  # Conservative 0.3% gap
                predicted_open = last_close * (1 + gap_pct / 100)
                confidence = 65
                reasons.append("Strong bullish close near session high")
                reasons.append(f"Buy confidence: {buy_conf}%")
        
        elif bias == "BEARISH" and sell_conf > 70:
            if close_position < 0.3:  # Closed near low
                gap_direction = "DOWN"
                gap_pct = -0.3
                predicted_open = last_close * (1 + gap_pct / 100)
                confidence = 65
                reasons.append("Weak bearish close near session low")
                reasons.append(f"Sell pressure: {sell_conf}%")
        
        # Check proximity to levels
        pivots = levels.get("levels", {})
        r1 = pivots.get("r1", 0)
        s1 = pivots.get("s1", 0)
        
        if r1 and last_close > r1 * 0.998:  # Within 0.2% of R1
            gap_direction = "UP" if gap_direction != "DOWN" else gap_direction
            gap_pct = 0.2
            predicted_open = last_close * 1.002
            confidence = max(confidence, 60)
            reasons.append(f"Close above resistance (R1: {r1})")
        
        if s1 and last_close < s1 * 1.002:  # Within 0.2% of S1
            gap_direction = "DOWN" if gap_direction != "UP" else gap_direction
            gap_pct = -0.2
            predicted_open = last_close * 0.998
            confidence = max(confidence, 60)
            reasons.append(f"Close below support (S1: {s1})")
        
        # Default flat opening for choppy conditions
        if not reasons:
            reasons.append("Neutral momentum - expect flat opening")
            reasons.append("No clear overnight catalysts detected")
        
        # 4. Trading suggestion
        if gap_direction == "UP":
            suggestion = f"If opens above {predicted_open:.0f}, look for continuation or wait for pullback to {last_close:.0f}"
        elif gap_direction == "DOWN":
            suggestion = f"If opens below {predicted_open:.0f}, avoid catching falling knife. Wait for stabilization"
        else:
            suggestion = f"Flat opening expected near {last_close:.0f}. Trade within range or wait  for breakout"
        
        return {
            "predicted_open": round(predicted_open, 2),
            "gap_direction": gap_direction,
            "gap_pct": round(gap_pct, 2),
            "confidence": confidence,
            "last_close": last_close,
            "reasons": reasons,
            "suggestion": suggestion,
            "timestamp": datetime.now().isoformat()
        }
