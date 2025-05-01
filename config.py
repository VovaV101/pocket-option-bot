# config.py

# Список вибраних пар для аналізу
selected_pairs = []

# Статус аналізу
analyzing = False

# Останні сигнали для кожної пари
last_signal = {}

# Час останнього сигналу для кожної пари
last_signal_time = {}

# Доступні валютні пари для вибору
pairs_list = {
    "EUR/USD": "EURUSD=X",
    "GBP/USD": "GBPUSD=X",
    "USD/JPY": "JPY=X",
    "USD/CAD": "CAD=X",
    "AUD/USD": "AUDUSD=X",
    "NZD/USD": "NZDUSD=X",
    "EUR/JPY": "EURJPY=X",
    "GBP/JPY": "GBPJPY=X"
}
