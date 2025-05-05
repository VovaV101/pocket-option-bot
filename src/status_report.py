from telegram import Update
from telegram.ext import CallbackContext

def send_status(update: Update, context: CallbackContext):
    selected_pairs = context.bot_data.get("selected_pairs", [])
    if not selected_pairs:
        update.message.reply_text("Немає вибраних пар для аналізу.")
    else:
        text = "Активні пари для аналізу:\n"
        for pair in selected_pairs:
            text += f"✅ {pair}\n"
        update.message.reply_text(text)
