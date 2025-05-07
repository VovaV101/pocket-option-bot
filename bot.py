# bot.py (у корені)

from telegram.ext import ApplicationBuilder
from src.handlers import setup_handlers
from src.config import BOT_TOKEN
import os
import requests

def check_api_connection():
    api_key = os.getenv("TWELVE_DATA_API_KEY")
    url = "https://api.twelvedata.com/time_series"
    params = {
        "symbol": "EUR/USD",
        "interval": "5min",
        "outputsize": 1,
        "apikey": api_key
    }
    try:
        response = requests.get(url, params=params)
        data = response.json()
        if "values" in data:
            print("✅ API доступ працює.")
        else:
            print(f"❌ API проблема: {data.get('message', 'Невідома помилка')}")
    except Exception as e:
        print(f"❌ Помилка підключення до API: {e}")

def main():
    # Перевірка API перед стартом бота
    check_api_connection()

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    setup_handlers(app)

    print("Bot started and polling...")
    app.run_polling(stop_signals=None)

if __name__ == "__main__":
    main()
