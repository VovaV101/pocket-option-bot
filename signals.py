import time
from telegram import Bot
from indicators import get_signal
from config import selected_pairs, last_signal, last_signal_time

def analyze_job(context):
    bot: Bot = context.bot
    for pair in selected_pairs:
        signal = get_signal(pair)
        if signal:
            direction, rsi_value = signal
            pair_name = pair.replace('/', '')
            if last_signal.get(pair) != direction:
                bot.send_message(
                    chat_id=context.job.context,
                    text=f"{pair} ВХІД {direction} на 15 хвилин\n"
                         f"RSI: {rsi_value} | EMA підтверджено | "
                         f"Stochastic, MACD, Bollinger Bands підтверджено\n"
                         f"Час: {time.strftime('%H:%M:%S')}"
                )
                last_signal[pair] = direction
                last_signal_time[pair] = time.strftime('%H:%M:%S')
