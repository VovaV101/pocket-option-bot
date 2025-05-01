from indicators import get_signal
from config import pairs_list
import time

def analyze_job(context):
    bot = context.bot
    chat_id = context.job.context
    selected_pairs = context.bot_data.get("selected_pairs", [])

    for pair in selected_pairs:
        signal = get_signal(pair)
        if signal:
            direction, rsi_value = signal
            for name, symbol in pairs_list.items():
                if symbol == pair:
                    pair_name = name
                    break
            else:
                pair_name = pair

            bot.send_message(
                chat_id=chat_id,
                text=f"{pair_name} ВХІД {direction} на 15 хвилин\n"
                     f"RSI: {rsi_value} | EMA підтверджено | Stochastic OK\n"
                     f"Час: {time.strftime('%H:%M:%S')}"
            )
