# twelvedata_api.py

import os
import requests

API_KEY = os.getenv("TWELVE_DATA_API_KEY")
BASE_URL = "https://api.twelvedata.com/"

def fetch_candles(symbol, interval="5min", outputsize=2):
    params = {
        "symbol": symbol,
        "interval": interval,
        "outputsize": outputsize,
        "apikey": API_KEY
    }
    response = requests.get(BASE_URL + "time_series", params=params)
    data = response.json()
    
    if "values" not in data:
        raise Exception(f"Помилка при отриманні даних для {symbol}: {data.get('message', 'Невідома помилка')}")
    
    return data["values"]

def get_last_two_candles(symbol):
    candles = fetch_candles(symbol)
    if len(candles) < 2:
        raise Exception(f"Недостатньо свічок для {symbol}")
    return candles[1], candles[0]  # попередня, остання
