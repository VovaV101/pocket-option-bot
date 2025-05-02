import os
import time
import yfinance as yf
from telegram import Bot
from telegram.ext import CallbackContext
from src.config import pairs_list, TIMEFRAME_MINUTES

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

        # Старший таймфрейм (5 свічок тому)
        senior = data.iloc[-10:-5]
        # Молодший таймфрейм (останні 5 свічок)
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

    bot = Bot(token=os.environ["TELEGRAM_TOKEN"])  # Створюємо окремого бота

    for pair in selected_pairs:
        signal = get_signal(pair)
        if signal:
            pair_name = [k for k, v in pairs_list.items() if v == pair][0]
            if last_signal.get(pair) != signal:
                bot.send_message(
                    chat_id=context.job.context,
                    text=f"{pair_name} — Вхід {signal} на {TIMEFRAME_MINUTES * 3} хвилин!\n"
                         f"Час: {time.strftime('%H:%M:%S')}"
                )
                last_signal[pair] = signal
                last_signal_time[pair] = time.strftime('%H:%M:%S')
