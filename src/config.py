import os

# Змінні середовища
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

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
TIMEFRAME_MINUTES = 5  # Аналіз на 5-хвилинному таймфреймі

# Змінні для роботи бота
selected_pairs = []
analyzing = False
job_reference = None
