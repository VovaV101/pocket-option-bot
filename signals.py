# signals.py

import time
import yfinance as yf
from indicators import compute_rsi, compute_stochastic, compute_macd, compute_bollinger_bands
from config import pairs_list, last_signal, last_signal_time

def get_signal(pair_code):
    """Основна логіка перевірки всіх індикаторів для однієї пари."""
    try:
        data = yf.download(tickers=pair_code, period="2d", interval="5m")
        if data.empty:
            return None

        close = data["Close"]
        ema50 = close.ewm(span=50).mean()
        latest_close = close.iloc[-2]  # Беремо ЗАВЕРШЕНУ попередню свічку
        latest_ema50 = ema50.iloc[-2]
        latest_rsi = compute_rsi(close).iloc[-2]
        stochastic_signal = compute_stochastic(data)
        macd_signal = compute_macd(data)
        bollinger_position = compute_bollinger_bands(data)

        # Умови для входу
        conditions_up = (
            latest_rsi < 30 and
            latest_close > latest_ema50 and
            stochastic_signal == "bullish" and
            macd_signal == "bullish" and
            bollinger_position == "below"
        )

        conditions_down = (
            latest_rsi > 70 and
            latest_close < latest_ema50 and
            stochastic_signal == "bearish" and
            macd_signal == "bearish" and
            bollinger_position == "above"
        )

        if conditions_up:
            return "UP", round(latest_rsi, 1)
        elif conditions_down:
            return "DOWN", round(latest_rsi, 1)
        else:
            return None

    except Exception as e:
        print(f"Error getting signal for {pair_code}: {e}")
        return None

def analyze(context):
    """Проходить по всім вибраним парам і надсилає сигнал при виконанні умов."""
    from config import selected_pairs
    for pair in selected_pairs:
        signal = get_signal(pair)
        if signal:
            direction, rsi_value = signal
            pair_name = [k for k, v in pairs_list.items() if v == pair][0]
            if last_signal.get(pair) != direction:
                context.bot.send_message(
                    chat_id=context.job.context,
                    text=f"{pair_name} — ВХІД {direction} на 15 хв\n"
                         f"RSI: {rsi_value} | Підтвердження EMA | Stochastic OK | MACD OK | Bollinger OK\n"
                         f"Час: {time.strftime('%H:%M:%S')}"
                )
                last_signal[pair] = direction
                last_signal_time[pair] = time.strftime('%H:%M:%S')
