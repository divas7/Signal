import yfinance as yf
import traceback

def test_nifty():
    symbol = "^NSEI"
    print(f"Testing YFinance for {symbol}...")
    try:
        ticker = yf.Ticker(symbol)
        
        print("Fetching fast_info...")
        try:
             price = ticker.fast_info.last_price
             print(f"Price: {price}")
        except Exception as e:
             print(f"Fast Info Failed: {e}")
             traceback.print_exc()

        print("Fetching history...")
        try:
            df = ticker.history(period="1d", interval="5m")
            print(f"History Shape: {df.shape}")
            if not df.empty:
                print(df.tail(1))
        except Exception as e:
            print(f"History Failed: {e}")
            traceback.print_exc()
            
    except Exception as e:
        print(f"General Error: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    test_nifty()
