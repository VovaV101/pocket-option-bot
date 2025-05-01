# signals.py

import yfinance as yf
import time
from indicators import compute_rsi, compute_stochastic
from config import pairs_list, last_signal, last_signal_time

def get_signal(ticker):
    try:
        # Завантажуємо дані старшого таймфрейму для перевірки тренду (15 хвилин)
        data_higher = yf.download(tickers=ticker, period="2d", interval="15m")
        if data_higher.empty:
            return None

        close_higher = data_higher["Close"]
        ema50_higher = close_higher.ewm(span=50).mean()
        latest_close_higher = close_higher.iloc[-1]
        latest_ema50_higher = ema50_higher.iloc[-1]

        # Перевірка тренду на 15 хвилинному графіку
        trend_up = latest_close_higher > latest_ema50_higher
        trend_down = latest_close_higher < latest_ema50_higher

        # Завантажуємо дані молодшого таймфрейму для входу (5 хвилин)
        data = yf.download(tickers=ticker, period="2d", interval="5m")
        if data.empty:
            return None

        close = data["Close"]
        ema50 = close.ewm(span=50).mean()
        rsi = compute_rsi(close)
        stochastic_signal = compute_stochastic(data)

        latest_close = close.iloc[-1]
        latest_ema50 = ema50.iloc[-1]
        latest_rsi = rsi.iloc[-1]

        # Умови для входу на молодшому таймфреймі
        if trend_up and latest_rsi < 30 and latest_close > latest_ema50 and stochastic_signal == "bullish":
            return "UP", round(latest_rsi, 1)
        elif trend_down and latest_rsi > 70 and latest_close < latest_ema50 and stochastic_signal == "bearish":
            return "DOWN", round(latest_rsi, 1)
        else:
            return None

    except Exception as e:
        print(f"Error in get_signal: {e}")
        return None

def analyze(context):
    for pair in context.bot_data.get("selected_pairs", []):
        signal = get_signal(pair)
        if signal:
            direction, rsi_value = signal
            pair_name = [k for k, v in pairs_list.items() if v == pair][0]
            if last_signal.get(pair) != direction:
                context.bot.send_message(
                    chat_id=context.job.context,
                    text=f"{pair_name} — ВХІД {direction} на 15 хвилин\n"
                         f"RSI: {rsi_value} | EMA підтверджено | Stochastic OK\n"
                         f"Час: {time.strftime('%H:%M:%S')}"
                )
                last_signal[pair] = direction
                last_signal_time[pair] = time.strftime('%H:%M:%S')
