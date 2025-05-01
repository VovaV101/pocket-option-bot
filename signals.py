import yfinance as yf
from indicators import compute_rsi, compute_stochastic, compute_ema, compute_macd, compute_bollinger_bands

def get_signal(ticker):
    try:
        data = yf.download(tickers=ticker, period="2d", interval="5m")
        if data.empty:
            return None

        close = data["Close"]
        ema50 = compute_ema(close, 50)
        rsi = compute_rsi(close)
        stochastic = compute_stochastic(data)
        macd = compute_macd(close)
        bollinger = compute_bollinger_bands(close)

        latest_close = close.iloc[-1]
        latest_ema50 = ema50.iloc[-1]
        latest_rsi = rsi.iloc[-1]

        if (latest_rsi < 30 and
            latest_close > latest_ema50 and
            stochastic == "bullish" and
            macd == "bullish" and
            bollinger == "bullish"):
            return "UP", round(latest_rsi, 1)
        
        elif (latest_rsi > 70 and
              latest_close < latest_ema50 and
              stochastic == "bearish" and
              macd == "bearish" and
              bollinger == "bearish"):
            return "DOWN", round(latest_rsi, 1)
        
        return None

    except Exception as e:
        print(f"Error in get_signal: {e}")
        return None
