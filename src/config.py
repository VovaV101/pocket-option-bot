
# Валютні пари
pairs_list = {
    "EUR/USD": "EURUSD=X",
    "GBP/USD": "GBPUSD=X",
    "USD/JPY": "USDJPY=X",
    "AUD/USD": "AUDUSD=X",
    "USD/CAD": "USDCAD=X",
    "EUR/JPY": "EURJPY=X",
    "GBP/JPY": "GBPJPY=X",
    "EUR/GBP": "EURGBP=X",
    "NZD/USD": "NZDUSD=X",
    "USD/CHF": "USDCHF=X",
}

# Параметри аналізу
TIMEFRAME_MINUTES = 5  # Аналіз кожні 5 хвилин

# Змінні середовища
import os
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
CHAT_ID = os.getenv("CHAT_ID")

# Інші налаштування
DEFAULT_INTERVAL_SENIOR = "60m"  # H1
DEFAULT_INTERVAL_JUNIOR = "5m"   # M5
DEFAULT_PERIOD = "2d"            # Дві доби даних
