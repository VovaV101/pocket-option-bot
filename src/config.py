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

# Глобальні змінні
selected_pairs = []
analyzing = False
last_signal = {}
last_signal_time = {}
job_reference = None
