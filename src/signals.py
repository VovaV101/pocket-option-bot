import yfinance as yf
import pandas as pd
import ta
from datetime import datetime
import pytz
from src.config import M5_INTERVAL, H1_INTERVAL, SIGNAL_TIMEOUT_MINUTES

selected_pairs = []
_last_check_time = None

def set_selected_pairs(pair):
    if pair not in selected_pairs:
        selected_pairs.append(pair)

def get_last_check_time():
    if _last_check_time:
        return _last_check_time.strftime("%d.%m.%Y %H:%M:%S")
    else:
        return "Ще не було перевірок."

def fetch_data(pair, interval, period="2d"):
    try:
        data = yf.download(tickers=pair.replace("/", ""), interval=interval, period=period, progress=False)
        return data
    except Exception as e:
        print(f"Помилка завантаження даних для {pair}: {e}")
        return pd.DataFrame()

def analyze_pair(pair):
    global _last_check_time
    try:
        df_h1 = fetch_data(pair, H1_INTERVAL)
        df_m5 = fetch_data(pair, M5_INTERVAL)

        if df_h1.empty or df_m5.empty:
            return None

        # Аналіз тренду на H1
        df_h1["ema_50"] = ta.trend.EMAIndicator(df_h1["Close"], window=50).ema_indicator()
        df_h1["ema_200"] = ta.trend.EMAIndicator(df_h1["Close"], window=200).ema_indicator()
        last_h1 = df_h1.iloc[-1]

        up_trend = last_h1["ema_50"] > last_h1["ema_200"]
        down_trend = last_h1["ema_50"] < last_h1["ema_200"]

        # Аналіз сигналу на M5
        df_m5["rsi"] = ta.momentum.RSIIndicator(df_m5["Close"]).rsi()
        df_m5["ema_50"] = ta.trend.EMAIndicator(df_m5["Close"], window=50).ema_indicator()
        df_m5["ema_200"] = ta.trend.EMAIndicator(df_m5["Close"], window=200).ema_indicator()
        stoch = ta.momentum.StochasticOscillator(df_m5["High"], df_m5["Low"], df_m5["Close"])
        df_m5["stoch_k"] = stoch.stoch()

        last_m5 = df_m5.iloc[-1]

        buy_signal = (
            up_trend and
            last_m5["rsi"] < 30 and
            last_m5["ema_50"] > last_m5["ema_200"] and
            last_m5["stoch_k"] < 30
        )

        sell_signal = (
            down_trend and
            last_m5["rsi"] > 70 and
            last_m5["ema_50"] < last_m5["ema_200"] and
            last_m5["stoch_k"] > 70
        )

        # Оновлюємо час останньої перевірки
        kyiv_tz = pytz.timezone('Europe/Kyiv')
        _last_check_time = datetime.now(kyiv_tz)

        if buy_signal:
            return f"{pair} — Вхід UP на {SIGNAL_TIMEOUT_MINUTES} хвилин"
        elif sell_signal:
            return f"{pair} — Вхід DOWN на {SIGNAL_TIMEOUT_MINUTES} хвилин"
        else:
            return None
    except Exception as e:
        print(f"Помилка аналізу для {pair}: {e}")
        return None
