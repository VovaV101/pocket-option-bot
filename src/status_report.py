from telegram import Update
from telegram.ext import CallbackContext
from src.config import analyzing, selected_pairs, last_signal_time, pairs_list

def status(update: Update, context: CallbackContext):
    message = ""

    if analyzing:
        message += "✅ Аналіз зараз *активний*.\n\n"
    else:
        message += "⛔ Аналіз зараз *неактивний*.\n\n"

    if selected_pairs:
        message += "*Обрані валютні пари:*\n"
        for ticker in selected_pairs:
            pair_name = [k for k, v in pairs_list.items() if v == ticker][0]
            last_time = last_signal_time.get(ticker, "Ще немає сигналу")
            message += f"— {pair_name} (Останній сигнал: {last_time})\n"
    else:
        message += "Валютні пари ще не обрані."

    update.message.reply_text(message, parse_mode="Markdown")
