from telegram import Update
from telegram.ext import CallbackContext
from config import analyzing

def status(update: Update, context: CallbackContext):
    """Відправляє статус аналізу."""
    if analyzing:
        update.message.reply_text("Аналіз *активний* ✅", parse_mode="Markdown")
    else:
        update.message.reply_text("Аналіз *неактивний* ❌", parse_mode="Markdown")
