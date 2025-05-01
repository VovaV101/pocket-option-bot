import yfinance as yf
from indicators import compute_rsi, compute_stochastic, compute_ema

def analyze_pair(pair, timeframe, candles, bot):
    """
    Аналізує валютну пару за допомогою трьох індикаторів:
    RSI, Stochastic і EMA.
    Якщо умови співпадають — надсилає сигнал в Telegram.
    """

    try:
        data = yf.download(pair, interval=f"{timeframe}m", period=f"{candles}d")

        if data.empty or len(data) < 50:
            print(f"Недостатньо даних для {pair}")
            return

        rsi_signal = compute_rsi(data)
        stochastic_signal = compute_stochastic(data)
        ema_signal = compute_ema(data)

        if rsi_signal == stochastic_signal == ema_signal and rsi_signal is not None:
            direction = "BUY" if rsi_signal == "buy" else "SELL"
            message = f"{pair}: Вхід {direction} на 15 хвилин"
            bot.send_message(chat_id=os.environ["CHAT_ID"], text=message)
            print(f"Сигнал на {pair}: {direction}")

    except Exception as e:
        print(f"Помилка аналізу {pair}: {e}")
