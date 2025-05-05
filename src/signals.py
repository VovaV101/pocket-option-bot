import os
import time
import pandas as pd
import yfinance as yf
import ta
from telegram import Bot
from telegram.ext import CallbackContext
from src.config import pairs_list, TIMEFRAME_MINUTES, TELEGRAM_TOKEN, CHAT_ID

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

    # EMA
    df["EMA_14"] = ta.trend.ema_indicator(df["Close"], window=14)

    # RSI
    df["RSI_14"] = ta.momentum.rsi(df["Close"], window=14)

    # Stochastic
    stoch = ta.momentum.StochasticOscillator(df["High"], df["Low"], df["Close"], window=14, smooth_window=3)
    df["Stoch_K"] = stoch.stoch()
    df["Stoch_D"] = stoch.stoch_signal()

    return df

def get_signal(pair: str):
    # Завантаження старшого таймфрейму (H1)
    senior = fetch_data(pair, interval="60m", period="2d")
    senior = calculate_indicators(senior)

    if senior.empty or len(senior) < 10:
        print(f"Недостатньо даних для старшого таймфрейму для {pair}")
        return None

    senior_trend_up = senior["EMA_14"].iloc[-1] > senior["EMA_14"].iloc[-5]
    senior_trend_down = senior["EMA_14"].iloc[-1] < senior["EMA_14"].iloc[-5]

    # Завантаження молодшого таймфрейму (5m)
    junior = fetch_data(pair, interval="5m", period="2d")
    junior = calculate_indicators(junior)

    if junior.empty or len(junior) < 10:
        print(f"Недостатньо даних для молодшого таймфрейму для {pair}")
        return None

    last = junior.iloc[-1]

    rsi = last["RSI_14"]
    stoch_k = last["Stoch_K"]
    stoch_d = last["Stoch_D"]

    # Умови сигналу
    if senior_trend_up and rsi > 50 and stoch_k > stoch_d and stoch_k > 20:
        return "UP"
    elif senior_trend_down and rsi < 50 and stoch_k < stoch_d and stoch_k < 80:
        return "DOWN"
    else:
        return None

def analyze_job(context: CallbackContext = None, chat_id: str = None):
    if context:
        bot_data = context.bot_data
        selected_pairs = bot_data.get("selected_pairs", [])
        last_signal = bot_data.setdefault("last_signal", {})
        last_signal_time = bot_data.setdefault("last_signal_time", {})
        actual_chat_id = chat_id or context.job.context
        bot = context.bot
    else:
        selected_pairs = list(pairs_list.values())
        last_signal = {}
        last_signal_time = {}
        actual_chat_id = chat_id or CHAT_ID
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

            previous_signal = last_signal.get(pair)
            print(f"Перевірка {pair}: минулий сигнал = {previous_signal}, новий сигнал = {signal}")

            if previous_signal != signal:
                bot.send_message(
                    chat_id=actual_chat_id,
                    text=f"{pair_name} — Вхід {signal} на {TIMEFRAME_MINUTES * 3} хвилин!\n"
                         f"Час: {time.strftime('%H:%M:%S')}"
                )
                last_signal[pair] = signal
                last_signal_time[pair] = time.strftime('%H:%M:%S')
            else:
                print(f"Сигнал для {pair} не змінився ({signal}), повідомлення не надсилаємо.")
        else:
            print(f"Немає сигналу для {pair}")
