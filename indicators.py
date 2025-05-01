import pandas as pd

def compute_rsi(data: pd.DataFrame, period: int = 14) -> pd.Series:
    delta = data["Close"].diff()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)

    avg_gain = gain.rolling(window=period, min_periods=period).mean()
    avg_loss = loss.rolling(window=period, min_periods=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.fillna(50)  # Якщо даних мало — ставимо RSI=50 для безпеки

def compute_stochastic(data: pd.DataFrame, k_period: int = 14) -> pd.Series:
    low_min = data["Low"].rolling(window=k_period).min()
    high_max = data["High"].rolling(window=k_period).max()
    stochastic = 100 * (data["Close"] - low_min) / (high_max - low_min)
    return stochastic.fillna(50)  # Якщо даних мало — ставимо 50

def compute_ema(data: pd.DataFrame, period: int = 50) -> pd.Series:
    ema = data["Close"].ewm(span=period, adjust=False).mean()
    return ema
