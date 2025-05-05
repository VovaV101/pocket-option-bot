import time
import pandas as pd
import yfinance as yf
import ta
from telegram import Bot
from src.config import pairs_list, TIMEFRAME_MINUTES, TELEGRAM_TOKEN, CHAT_ID

# Змінна для збереження роботи задачі
job_instance = None

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
    senior = fetch_data(pair, interval="60m", period="2d")
    senior = calculate_indicators(senior)

    if senior.empty or len(senior) < 10:
        print(f"Недостатньо даних для старшого таймфрейму для {pair}")
        return None

    senior_trend_up = senior["EMA_14"].iloc[-1] > senior["EMA_14"].iloc[-5]
    senior_trend_down = senior["EMA_14"].iloc[-1] < senior["EMA_14"].iloc[-5]

    junior = fetch_data(pair, interval="5m", period="2d")
    junior = calculate_indicators(junior)

    if junior.empty or len(junior) < 10:
        print(f"Недостатньо даних для молодшого таймфрейму для {pair}")
        return None

    last = junior.iloc[-1]

    rsi = last["RSI_14"]
    stoch_k = last["Stoch_K"]
    stoch_d = last["Stoch_D"]

    if senior_trend_up and rsi > 50 and stoch_k > stoch_d and stoch_k > 20:
        return "UP"
    elif senior_trend_down and rsi < 50 and stoch_k < stoch_d and stoch_k < 80:
        return "DOWN"
    else:
        return None

def analyze_job(context):
    selected_pairs = context.job.data.get("selected_pairs", [])
    bot = context.bot
    chat_id = context.job.data.get("chat_id", CHAT_ID)

    if not selected_pairs:
        print("Немає обраних валютних пар для аналізу.")
        return

    for pair in selected_pairs:
        signal = get_signal(pairs_list[pair])

        if signal:
            text = f"{pair} — Вхід {signal} на {TIMEFRAME_MINUTES * 3} хвилин!\nЧас: {time.strftime('%H:%M:%S')}"
            bot.send_message(chat_id=chat_id, text=text)
            print(f"Надіслано сигнал: {text}")
        else:
            print(f"Немає сигналу для {pair}")

def start_analysis(selected_pairs):
    global job_instance
    from src.bot import application

    if job_instance:
        print("Аналіз уже запущено.")
        return

    job_instance = application.job_queue.run_repeating(
        analyze_job,
        interval=TIMEFRAME_MINUTES * 60,
        first=0,
        data={"selected_pairs": list(selected_pairs), "chat_id": CHAT_ID}
    )
    print("Аналіз стартував.")

def stop_analysis():
    global job_instance

    if job_instance:
        job_instance.schedule_removal()
        job_instance = None
        print("Аналіз зупинено.")
    else:
        print("Аналіз не був запущений.")
