from twelvedata_api import get_last_two_candles

def analyze_pair(symbol):
    try:
        prev_candle, last_candle = get_last_two_candles(symbol)
        
        open_prev = float(prev_candle["open"])
        close_prev = float(prev_candle["close"])
        open_last = float(last_candle["open"])
        close_last = float(last_candle["close"])
        
        # Сигнал на підвищення
        if close_prev > open_prev and close_last > open_last:
            return "UP"
        # Сигнал на зниження
        elif close_prev < open_prev and close_last < open_last:
            return "DOWN"
        else:
            return None
    except Exception as e:
        print(f"Помилка при аналізі {symbol}: {e}")
        return None
