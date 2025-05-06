import os

BOT_TOKEN = os.getenv('BOT_TOKEN')  # або вставити свій токен прямо сюди в лапках

PAIRS = [
    "EUR/USD", "GBP/USD", "USD/JPY", "USD/CAD",
    "AUD/USD", "NZD/USD", "GBP/JPY", "EUR/JPY",
    "GBP/CHF", "EUR/GBP"
]

M5_INTERVAL = "5m"
H1_INTERVAL = "1h"

SIGNAL_TIMEOUT_MINUTES = 15  # На скільки хвилин орієнтуємо вхід
