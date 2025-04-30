# config.py

selected_pairs = []  # сюди додаються вибрані пари користувачем
analyzing = False    # чи активний аналіз
job_reference = None # посилання на задачу

# Для контролю повторних сигналів
last_signal = {}
last_signal_time = {}

# Валютні пари та тікери yfinance
pairs_list = {
    "EUR/USD": "EURUSD=X",
    "GBP/USD": "GBPUSD=X",
    "USD/JPY": "JPY=X",
    "USD/CAD": "CAD=X",
    "AUD/USD": "AUDUSD=X",
    "NZD/USD": "NZDUSD=X",
    "EUR/JPY": "EURJPY=X",
    "GBP/JPY": "GBPJPY=X",
}
