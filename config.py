# Обрані пари для аналізу
selected_pairs = []

# Список доступних валютних пар
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
    "USD/CHF": "USDCHF=X"
}

# Стан аналізу
analyzing = False

# Таймфрейм аналізу в хвилинах
TIMEFRAME_MINUTES = 5
