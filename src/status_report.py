

from telegram import Update
from telegram.ext import CallbackContext
from src.handlers import selected_pairs, analyzing

def send_signal(update: Update, context: CallbackContext):
    if not selected_pairs:
        update.message.reply_text("⚠️ Валютні пари не обрані.")
    else:
        pairs_text = "\n".join([f"✅ {pair}" for pair in selected_pairs])
        status_text = "🟢 Аналіз активний" if analyzing else "🔴 Аналіз не активний"
        update.message.reply_text(f"Поточний стан:\n{status_text}\n\nОбрані пари:\n{pairs_text}")
