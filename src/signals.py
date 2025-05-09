from src.twelvedata_api import (
    get_last_two_candles_m5,
    get_last_candles_for_indicators_m5,
    get_last_candles_for_ema_h1
)
import numpy as np

selected_pairs = []
debug_mode = False  # ← True для відлагодження вручну через /debug

def calculate_ema(values, period):
    weights = np.exp(np.linspace(-1., 0., period))
    weights /= weights.sum()
    a = np.convolve(values, weights, mode='full')[:len(values)]
    a[:period] = a[period]
    return a

def calculate_rsi(closes, period=14):
    deltas = np.diff(closes)
    seed = deltas[:period]
    up = seed[seed >= 0].sum() / period
    down = -seed[seed < 0].sum() / period
    rs = up / down if down != 0 else 0
    rsi = np.zeros_like(closes)
    rsi[:period] = 100. - 100. / (1. + rs)

    for i in range(period, len(closes)):
        delta = deltas[i - 1]
        upval = max(delta, 0)
        downval = -min(delta, 0)
        up = (up * (period - 1) + upval) / period
        down = (down * (period - 1) + downval) / period
        rs = up / down if down != 0 else 0
        rsi[i] = 100. - 100. / (1. + rs)

    return rsi

def calculate_stochastic(highs, lows, closes, period=14):
    stochastics = []
    for i in range(period - 1, len(closes)):
        highest_high = max(highs[i - period + 1:i + 1])
        lowest_low = min(lows[i - period + 1:i + 1])
        if highest_high == lowest_low:
            stochastics.append(0)
        else:
            stochastics.append((closes[i] - lowest_low) / (highest_high - lowest_low) * 100)
    return stochastics

def analyze_pair(symbol):
    try:
        # === Тренд на H1 через EMA ===
        candles_h1 = get_last_candles_for_ema_h1(symbol)
        closes_h1 = [float(candle['close']) for candle in reversed(candles_h1)]

        ema50 = calculate_ema(np.array(closes_h1), period=50)
        ema200 = calculate_ema(np.array(closes_h1), period=200)

        if ema50[-2] > ema200[-2]:
            trend = "up"
        elif ema50[-2] < ema200[-2]:
            trend = "down"
        else:
            if debug_mode:
                print(f"[DEBUG] {symbol}: Тренд не визначений")
            return None

        # === Індикатори на M5 ===
        candles_m5 = get_last_candles_for_indicators_m5(symbol)
        closes_m5 = [float(candle['close']) for candle in reversed(candles_m5)]
        highs_m5 = [float(candle['high']) for candle in reversed(candles_m5)]
        lows_m5 = [float(candle['low']) for candle in reversed(candles_m5)]

        rsi = calculate_rsi(np.array(closes_m5))[-1]
        stochastic = calculate_stochastic(highs_m5, lows_m5, closes_m5)[-1]

        # === Колір останньої свічки ===
        prev_candle, last_candle = get_last_two_candles_m5(symbol)
        open_prev = float(prev_candle["open"])
        close_prev = float(prev_candle["close"])
        open_last = float(last_candle["open"])
        close_last = float(last_candle["close"])

        is_green = close_last > open_last
        is_red = close_last < open_last

        # === DEBUG ВИВІД ===
        if debug_mode:
            print(f"\n[DEBUG] Аналіз: {symbol}")
            print(f"[DEBUG] Тренд: {trend}")
            print(f"[DEBUG] EMA50[-2]: {ema50[-2]:.5f}, EMA200[-2]: {ema200[-2]:.5f}")
            print(f"[DEBUG] RSI: {rsi:.2f}, Stochastic: {stochastic:.2f}")
            print(f"[DEBUG] Свічка: {'зелена' if is_green else 'червона'}")

        # === Сигнали ===
        if trend == "up" and rsi < 30 and stochastic < 20 and is_green:
            return "UP"
        elif trend == "down" and rsi > 70 and stochastic > 80 and is_red:
            return "DOWN"
        else:
            return None

    except Exception as e:
        print(f"[ERROR] {symbol}: {e}")
        return None
