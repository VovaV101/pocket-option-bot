import os
import time
import yfinance as yf
import pandas as pd
from telegram import Bot
from telegram.ext import CallbackContext
from src.config import pairs_list, TIMEFRAME_MINUTES

# Отримання змінних середовища
CHAT_ID = os.environ.get("CHAT_ID")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")

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

        if senior.empty or junior.empty:
            return None

        senior_trend_up = senior["Close"].mean() > senior["Open"].mean()
        senior_trend_down = senior["Close"].mean() < senior["Open"].mean()

        last_candle = junior.iloc[-1]
        junior_high_max = junior["High"].max()
        junior_low_min = junior["Low"].min()

        if pd.isna(last_candle["Close"]) or pd.isna(junior_high_max) or pd.isna(junior_low_min):
            return None

        junior_breakout_up = float(last_candle["Close"]) > float(junior_high_max)
        junior_breakout_down = float(last_candle["Close"]) < float(junior_low_min)

        if senior_trend_up and junior_breakout_up:
            return "UP"
        elif senior_trend_down and junior_breakout_down:
            return "DOWN"
        else:
            return None
    except Exception as e:
        print(f"Помилка при отриманні сигналу для {pair}: {e}")
        return None

def analyze_job(context: CallbackContext = None, chat_id: str = None):
    if context:
        # Якщо аналіз викликається через JobQueue
        bot_data = context.bot_data
        selected_pairs = bot_data.get("selected_pairs", [])
        last_signal = bot_data.setdefault("last_signal", {})
        last_signal_time = bot_data.setdefault("last_signal_time", {})
        chat_id = chat_id or context.job.context
        bot = context.bot
    else:
        # Якщо аналіз викликається вручну через /analyze
        selected_pairs = list(pairs_list.values())
        last_signal = {}
        last_signal_time = {}
        bot = Bot(token=TELEGRAM_TOKEN)

    if not selected_pairs:
        print("Немає обраних валютних пар для аналізу.")
        return

    for pair in selected_pairs:
        signal = get_signal(pair)
        if signal:
            try:
                pair_name = next((k for k, v in pairs_list.items() if v == pair), pair)
            except StopIteration:
                pair_name = pair

            if last_signal.get(pair) != signal:
                bot.send_message(
                    chat_id=chat_id,
                    text=f"{pair_name} — Вхід {signal} на {TIMEFRAME_MINUTES * 3} хвилин!\n"
                         f"Час: {time.strftime('%H:%M:%S')}"
                )
                last_signal[pair] = signal
                last_signal_time[pair] = time.strftime('%H:%M:%S')
