# src/signals.py

import time
import pandas as pd
import yfinance as yf
import ta
from telegram import Bot
from telegram.ext import CallbackContext, JobQueue
from src.config import pairs_list, TELEGRAM_TOKEN, CHAT_ID, TIMEFRAME_MINUTES

selected_pairs = set()
job = None

def fetch_data(pair: str, interval: str, period: str):
    try:
        data = yf.download(
            tickers=pair,
            interval=interval,
            period=period,
            progress=False,
            threads=False
        )
        return data
    except Exception as e:
        print(f"Помилка при завантаженні даних для {pair}: {e}")
        return pd.DataFrame()

def calculate_indicators(df: pd.DataFrame):
    if df.empty:
        return df

    df["EMA_14"] = ta.trend.ema_indicator(df["Close"], window=14)
    df["RSI_14"] = ta.momentum.rsi(df["Close"], window=14)
    stoch = ta.momentum.StochasticOscillator(df["High"], df["Low"], df["Close"], window=14, smooth_window=3)
    df["Stoch_K"] = stoch.stoch()
    df["Stoch_D"] = stoch.stoch_signal()

    return df

def get_signal(pair: str):
    senior = fetch_data(pair, interval="60m", period="2d")
    senior = calculate_indicators(senior)

    if senior.empty or len(senior) < 10:
        print(f"Недостатньо даних для H1 таймфрейму: {pair}")
        return None

    trend_up = senior["EMA_14"].iloc[-1] > senior["EMA_14"].iloc[-5]
    trend_down = senior["EMA_14"].iloc[-1] < senior["EMA_14"].iloc[-5]

    junior = fetch_data(pair, interval="5m", period="2d")
    junior = calculate_indicators(junior)

    if junior.empty or len(junior) < 10:
        print(f"Недостатньо даних для M5 таймфрейму: {pair}")
        return None

    last = junior.iloc[-1]
    rsi = last["RSI_14"]
    stoch_k = last["Stoch_K"]
    stoch_d = last["Stoch_D"]

    if trend_up and rsi > 50 and stoch_k > stoch_d and stoch_k > 20:
        return "UP"
    elif trend_down and rsi < 50 and stoch_k < stoch_d and stoch_k < 80:
        return "DOWN"
    else:
        return None

def analyze(context: CallbackContext):
    bot = context.bot
    for pair in selected_pairs:
        ticker = pairs_list.get(pair)
        if not ticker:
            continue

        signal = get_signal(ticker)
        if signal:
            bot.send_message(
                chat_id=CHAT_ID,
                text=f"📈 {pair}: Сигнал {signal} на {TIMEFRAME_MINUTES * 3} хвилин!\nЧас: {time.strftime('%H:%M:%S')}"
            )
            print(f"Сигнал для {pair}: {signal}")
        else:
            print(f"Немає сигналу для {pair}")

def start_analysis(context: CallbackContext):
    global job
    if job is None:
        job_queue: JobQueue = context.job_queue
        job = job_queue.run_repeating(analyze, interval=TIMEFRAME_MINUTES * 60, first=5)
        print("Аналіз запущено.")

def stop_analysis(context: CallbackContext):
    global job
    if job is not None:
        job.schedule_removal()
        job = None
        print("Аналіз зупинено.")
