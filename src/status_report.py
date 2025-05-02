from telegram import Update
from telegram.ext import CallbackContext
import src.config as config  # Імпортуємо весь config

def status(update: Update, context: CallbackContext):
    message = ""

    if config.analyzing:
        message += "✅ Аналіз зараз *активний*.\n\n"
    else:
        message += "⛔ Аналіз зараз *неактивний*.\n\n"

    if config.selected_pairs:
        message += "*Обрані валютні пари:*\n"
        for ticker in config.selected_pairs:
            pair_name = next((k for k, v in config.pairs_list.items() if v == ticker), ticker)
            last_time = config.last_signal_time.get(ticker, "Ще немає сигналу")
            message += f"— {pair_name} (Останній сигнал: {last_time})\n"
    else:
        message += "Валютні пари ще не обрані."

    update.message.reply_text(message, parse_mode="Markdown")
