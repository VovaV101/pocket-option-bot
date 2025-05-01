# config.py

from telegram import Bot
import os

# Витягуємо токен із змінних середовища Render
TOKEN = os.getenv("BOT_TOKEN")

# Створюємо об'єкт бота
bot = Bot(token=TOKEN)

# Таймфрейм для аналізу (в хвилинах)
TIMEFRAME_MINUTES = 5

# Список доступних валютних пар
AVAILABLE_PAIRS = [
    "EUR/USD", "GBP/USD", "USD/JPY", "USD/CAD",
    "AUD/USD", "NZD/USD", "EUR/JPY", "GBP/JPY"
]
