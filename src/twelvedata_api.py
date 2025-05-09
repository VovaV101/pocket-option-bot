import os
import requests

API_KEY = os.getenv("TWELVE_DATA_API_KEY")
BASE_URL = "https://api.twelvedata.com/"

def fetch_candles(symbol, interval="5min", outputsize=50):
    params = {
        "symbol": symbol,
        "interval": interval,
        "outputsize": outputsize,
        "apikey": API_KEY
    }
    response = requests.get(BASE_URL + "time_series", params=params)
    data = response.json()
    
    if "values" not in data:
        raise Exception(f"Помилка при отриманні даних для {symbol} ({interval}): {data.get('message', 'Невідома помилка')}")
    
    return data["values"]

def get_last_two_candles_m5(symbol):
    candles = fetch_candles(symbol, interval="5min", outputsize=2)
    if len(candles) < 2:
        raise Exception(f"Недостатньо свічок для {symbol} на M5")
    return candles[1], candles[0]  # попередня, остання

def get_last_candles_for_indicators_m5(symbol):
    candles = fetch_candles(symbol, interval="5min", outputsize=20)
    if len(candles) < 14:
        raise Exception(f"Недостатньо даних для розрахунку RSI/Stochastic для {symbol} на M5")
    return candles

def get_last_candles_for_ema_h1(symbol):
    candles = fetch_candles(symbol, interval="1h", outputsize=300)  # забезпечуємо достатньо даних для EMA200
    if len(candles) < 200:
        raise Exception(f"Недостатньо даних для розрахунку EMA для {symbol} на H1")
    return candles
