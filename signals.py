import pandas as pd
import yfinance as yf
from indicators import compute_rsi, compute_stochastic, compute_trend
from config import TIMEFRAME_MINUTES

def analyze(pair: str) -> str:
    """Повертає сигнал для входу в угоду по валютній парі."""
    try:
        # Завантажуємо дані
        df = yf.download(pair, interval="5m", period="1d", progress=False)

        if df.empty or len(df) < 50:
            return f"Недостатньо даних для {pair}."

        # Обчислення індикаторів
        df = compute_rsi(df)
        df = compute_stochastic(df)
        df = compute_trend(df)

        # Отримуємо значення останніх двох свічок
        latest = df.iloc[-1]
        previous = df.iloc[-2]

        # Логіка сигналу
        signal = None

        if latest['Trend'] == 'uptrend' and latest['RSI'] > 50 and latest['Stochastic'] > 50:
            signal = "BUY"
        elif latest['Trend'] == 'downtrend' and latest['RSI'] < 50 and latest['Stochastic'] < 50:
            signal = "SELL"

        if signal:
            return f"{pair}: {signal} на {TIMEFRAME_MINUTES * 3} хвилин."
        else:
            return f"{pair}: Сигналу немає."

    except Exception as e:
        return f"Помилка при аналізі {pair}: {e}"
