from datetime import datetime, time
import pytz

def get_market_status_ist():
    """
    Returns the market status for NIFTY (NSE).
    Timezone: Asia/Kolkata
    Open: 09:15 - 15:30 (Mon-Fri)
    """
    tz_ist = pytz.timezone('Asia/Kolkata')
    now_ist = datetime.now(tz_ist)
    
    # Check Weekend
    if now_ist.weekday() >= 5: # 5=Sat, 6=Sun
        return {
            "is_open": False,
            "status": "CLOSED",
            "message": "Market Closed (Weekend)",
            "timestamp": now_ist.strftime("%Y-%m-%d %H:%M:%S IST")
        }

    # Check Time
    current_time = now_ist.time()
    market_open = time(9, 15)
    market_close = time(15, 30)

    if market_open <= current_time <= market_close:
        return {
            "is_open": True,
            "status": "OPEN",
            "message": "Market Open",
            "timestamp": now_ist.strftime("%Y-%m-%d %H:%M:%S IST")
        }
    else:
        return {
            "is_open": False,
            "status": "CLOSED",
            "message": "Market Closed (Outside Hours)",
            "timestamp": now_ist.strftime("%Y-%m-%d %H:%M:%S IST")
        }
