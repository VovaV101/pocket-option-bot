import os
import time
import yfinance as yf
from telegram.ext import CallbackContext
from src.config import pairs_list, TIMEFRAME_MINUTES

# Беремо змінну чат айді один раз на початку
CHAT_ID = os.environ["CHAT_ID"]

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
            return None

        senior = data.iloc[-10:-5]
        junior = data.iloc[-5:]

        senior_trend_up = senior['Close'].mean() > senior['Open'].mean()
        senior_trend_down = senior['Close'].mean() < senior['Open'].mean()

        junior_breakout_up = junior.iloc[-1]['Close'] > junior['High'].max()
        junior_breakout_down = junior.iloc[-1]['Close'] < junior['Low'].min()

        if senior_trend_up and junior_breakout_up:
            return "UP"
        elif senior_trend_down and junior_breakout_down:
            return "DOWN"
        else:
            return None
    except Exception as e:
        print(f"Помилка при отриманні сигналу для {pair}: {e}")
        return None

def analyze_job(context: CallbackContext):
    selected_pairs = context.bot_data.get("selected_pairs", [])
    last_signal = context.bot_data.setdefault("last_signal", {})
    last_signal_time = context.bot_data.setdefault("last_signal_time", {})

    if not selected_pairs:
        print("Немає обраних пар для аналізу.")
        return

    for pair in selected_pairs:
        signal = get_signal(pair)
        if signal:
            pair_name = [k for k, v in pairs_list.items() if v == pair][0]
            if last_signal.get(pair) != signal:
                context.bot.send_message(
                    chat_id=CHAT_ID,
                    text=f"{pair_name} — Вхід {signal} на {TIMEFRAME_MINUTES * 3} хвилин!\n"
                         f"Час: {time.strftime('%H:%M:%S')}"
                )
                last_signal[pair] = signal
                last_signal_time[pair] = time.strftime('%H:%M:%S')
