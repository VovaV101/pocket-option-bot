# signals.py

import asyncio
import logging
from config import bot, TIMEFRAME_MINUTES
from indicators import compute_rsi, compute_stochastic, compute_ema, compute_macd, compute_bollinger_bands

async def analyze_job(context):
    chat_id = context.job.chat_id
    pairs_to_analyze = context.bot_data.get('pairs', [])

    if not pairs_to_analyze:
        logging.info("Немає обраних валютних пар для аналізу.")
        return

    for pair in pairs_to_analyze:
        logging.info(f"Аналіз пари {pair}...")

        # Порахувати індикатори
        rsi = compute_rsi(pair)
        stochastic = compute_stochastic(pair)
        ema = compute_ema(pair)
        macd = compute_macd(pair)
        bollinger = compute_bollinger_bands(pair)

        # Умови для покупки
        buy_conditions = (
            rsi < 30 and
            stochastic < 20 and
            ema == 'buy' and
            macd == 'buy' and
            bollinger == 'buy'
        )

        # Умови для продажу
        sell_conditions = (
            rsi > 70 and
            stochastic > 80 and
            ema == 'sell' and
            macd == 'sell' and
            bollinger == 'sell'
        )

        # Надсилання сигналу
        if buy_conditions:
            await bot.send_message(
                chat_id=chat_id,
                text=f"📈 Купувати {pair}!\nВідкрити угоду на {TIMEFRAME_MINUTES} хвилин."
            )
        elif sell_conditions:
            await bot.send_message(
                chat_id=chat_id,
                text=f"📉 Продавати {pair}!\nВідкрити угоду на {TIMEFRAME_MINUTES} хвилин."
            )
        else:
            logging.info(f"Немає сигналу для {pair}.")
