import yfinance as yf
import ta
from config import TIMEFRAME_MINUTES

def get_signal(pair: str):
    try:
        # Завантажуємо дані
        data = yf.download(
            tickers=pair,
            interval="5m",
            period="2d",
            progress=False,
            threads=False
        )

        if data.empty or len(data) < 50:
            return None  # Недостатньо даних

        # Обчислення індикаторів
        data['EMA50'] = ta.trend.ema_indicator(data['Close'], window=50)
        data['EMA200'] = ta.trend.ema_indicator(data['Close'], window=200)
        data['RSI'] = ta.momentum.rsi(data['Close'], window=14)
        stoch = ta.momentum.StochasticOscillator(
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            window=14,
            smooth_window=3
        )
        data['Stoch_%K'] = stoch.stoch()

        # Визначення тренду на старшому таймфреймі
        last_ema50 = data['EMA50'].iloc[-20:-5].mean()
        last_ema200 = data['EMA200'].iloc[-20:-5].mean()

        if last_ema50 > last_ema200:
            trend = "up"
        elif last_ema50 < last_ema200:
            trend = "down"
        else:
            trend = None

        # Перевірка сигналу на молодшому таймфреймі (останній сигнал)
        last_rsi = data['RSI'].iloc[-1]
        last_stoch = data['Stoch_%K'].iloc[-1]

        if trend == "up" and last_rsi > 50 and last_stoch < 30:
            return f"Сигнал для {pair}: Купувати на {TIMEFRAME_MINUTES * 3} хвилин ✅"
        elif trend == "down" and last_rsi < 50 and last_stoch > 70:
            return f"Сигнал для {pair}: Продавати на {TIMEFRAME_MINUTES * 3} хвилин ❌"
        else:
            return None  # Немає чіткого сигналу

    except Exception as e:
        print(f"Помилка при отриманні сигналу для {pair}: {e}")
        return None
