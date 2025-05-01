import yfinance as yf
from config import TIMEFRAME_MINUTES

def get_signal(pair: str):
    try:
        data = yf.download(
            tickers=pair,
            interval=f"{TIMEFRAME_MINUTES}m",
            period="2d",
            progress=False,
            threads=False
        )

        if data.empty or len(data) < 10:
            return None  # Недостатньо даних

        # Старший таймфрейм (наприклад 15 хв)
        senior = data.iloc[-10:-5]
        # Молодший таймфрейм (останні 5 свічок)
        junior = data.iloc[-5:]

        # Простий приклад логіки:
        senior_trend_up = senior['Close'].mean() > senior['Open'].mean()
        senior_trend_down = senior['Close'].mean() < senior['Open'].mean()

        junior_breakout_up = junior.iloc[-1]['Close'] > junior['High'].max()
        junior_breakout_down = junior.iloc[-1]['Close'] < junior['Low'].min()

        if senior_trend_up and junior_breakout_up:
            return f"Сигнал для {pair}: Купувати на {TIMEFRAME_MINUTES * 3} хвилин ✅"
        elif senior_trend_down and junior_breakout_down:
            return f"Сигнал для {pair}: Продавати на {TIMEFRAME_MINUTES * 3} хвилин ❌"
        else:
            return None  # Немає чіткого сигналу
    except Exception as e:
        print(f"Помилка при отриманні сигналу для {pair}: {e}")
        return None
