from telegram import Update
from telegram.ext import CallbackContext
from src.config import pairs_list

def status(update: Update, context: CallbackContext):
    bot_data = context.bot_data
    analyzing = bot_data.get("analyzing", False)
    selected_pairs = bot_data.get("selected_pairs", [])
    last_signal_time = bot_data.get("last_signal_time", {})

    message = ""

    if analyzing:
        message += "✅ Аналіз зараз *активний*.\n\n"
    else:
        message += "⛔ Аналіз зараз *неактивний*.\n\n"

    if selected_pairs:
        message += "*Обрані валютні пари:*\n"
        for ticker in selected_pairs:
            pair_name = next((k for k, v in pairs_list.items() if v == ticker), ticker)
            last_time = last_signal_time.get(ticker, "Ще немає сигналу")
            message += f"— {pair_name} (Останній сигнал: {last_time})\n"
    else:
        message += "Валютні пари ще не обрані."

    update.message.reply_text(message, parse_mode="Markdown")
