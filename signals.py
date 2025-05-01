import yfinance as yf
from indicators import compute_rsi, compute_stochastic, compute_ema

# Таймфрейми для аналізу
HIGHER_TIMEFRAME = "1h"   # старший таймфрейм
LOWER_TIMEFRAME = "5m"    # молодший таймфрейм

# Угода на 3 свічки (тобто 15 хвилин на 5-хвилинному таймфреймі)
TRADE_DURATION_MINUTES = 15

def analyze(pair: str, bot, chat_id: int):
    try:
        # Завантажуємо дані для старшого таймфрейму
        higher_data = yf.download(tickers=pair, interval=HIGHER_TIMEFRAME, period="2d", progress=False)

        if higher_data.empty:
            bot.send_message(chat_id=chat_id, text=f"Не вдалося отримати дані для {pair} на {HIGHER_TIMEFRAME}.")
            return

        # Розрахунок індикаторів для старшого таймфрейму
        higher_rsi = compute_rsi(higher_data)
        higher_stochastic = compute_stochastic(higher_data)
        higher_ema = compute_ema(higher_data)

        # Визначаємо загальний тренд на старшому таймфреймі
        trend = None
        if higher_rsi[-1] > 50 and higher_data["Close"].iloc[-1] > higher_ema[-1]:
            trend = "up"
        elif higher_rsi[-1] < 50 and higher_data["Close"].iloc[-1] < higher_ema[-1]:
            trend = "down"

        if not trend:
            # Якщо тренд невизначений — не надсилаємо сигнал
            return

        # Завантажуємо дані для молодшого таймфрейму
        lower_data = yf.download(tickers=pair, interval=LOWER_TIMEFRAME, period="1d", progress=False)

        if lower_data.empty:
            bot.send_message(chat_id=chat_id, text=f"Не вдалося отримати дані для {pair} на {LOWER_TIMEFRAME}.")
            return

        # Розрахунок індикаторів для молодшого таймфрейму
        lower_rsi = compute_rsi(lower_data)
        lower_stochastic = compute_stochastic(lower_data)

        # Шукаємо точку входу на молодшому таймфреймі відповідно до тренду
        signal = None
        if trend == "up":
            if lower_rsi[-1] > 50 and lower_stochastic[-1] < 80:
                signal = "UP"
        elif trend == "down":
            if lower_rsi[-1] < 50 and lower_stochastic[-1] > 20:
                signal = "DOWN"

        if signal:
            message = (
                f"📈 Сигнал для {pair}:\n"
                f"➡️ Вхід: {signal}\n"
                f"➡️ Час угоди: {TRADE_DURATION_MINUTES} хвилин\n"
                f"➡️ За трендом: {trend.upper()} таймфрейм {HIGHER_TIMEFRAME}\n"
                f"➡️ Перевірено по {LOWER_TIMEFRAME}"
            )
            bot.send_message(chat_id=chat_id, text=message)

    except Exception as e:
        bot.send_message(chat_id=chat_id, text=f"Помилка аналізу для {pair}: {str(e)}")
