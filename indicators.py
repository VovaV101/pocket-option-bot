import pandas as pd

def compute_rsi(df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
    """Обчислення індикатора RSI."""
    delta = df['Close'].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(window=period, min_periods=period).mean()
    avg_loss = loss.rolling(window=period, min_periods=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    df['RSI'] = rsi
    return df

def compute_stochastic(df: pd.DataFrame, k_period: int = 14, d_period: int = 3) -> pd.DataFrame:
    """Обчислення стохастичного осцилятора."""
    low_min = df['Low'].rolling(window=k_period).min()
    high_max = df['High'].rolling(window=k_period).max()

    df['%K'] = 100 * (df['Close'] - low_min) / (high_max - low_min)
    df['%D'] = df['%K'].rolling(window=d_period).mean()

    return df

def compute_ema(df: pd.DataFrame, span: int = 50) -> pd.DataFrame:
    """Обчислення EMA."""
    df[f'EMA_{span}'] = df['Close'].ewm(span=span, adjust=False).mean()
    return df
