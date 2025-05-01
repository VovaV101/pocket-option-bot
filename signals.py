import yfinance as yf
from indicators import compute_rsi, compute_stochastic, compute_ema
from config import TIMEFRAME_MINUTES

def analyze(pair: str) -> str:
    """Аналізує валютну пару та повертає торговий сигнал."""

    # Завантаження даних
    data = yf.download(pair, interval='5m', period='1d')

    if data.empty:
        return f"Не вдалося отримати дані для {pair}."

    # Обчислення індикаторів
    data = compute_rsi(data)
    data = compute_stochastic(data)
    data = compute_ema(data)

    # Логіка прийняття рішення
    last = data.iloc[-1]
    previous = data.iloc[-2]

    # Умови для покупки (UP)
    if (
        last['RSI'] > 50
        and last['%K'] > last['%D']
        and last['Close'] > last['EMA_50']
    ):
        return f"{pair}: Вхід UP на {TIMEFRAME_MINUTES} хвилин."

    # Умови для продажу (DOWN)
    if (
        last['RSI'] < 50
        and last['%K'] < last['%D']
        and last['Close'] < last['EMA_50']
    ):
        return f"{pair}: Вхід DOWN на {TIMEFRAME_MINUTES} хвилин."

    # Якщо немає явного сигналу
    return f"{pair}: Сигналів немає."
