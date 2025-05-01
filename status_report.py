from telegram import Update
from telegram.ext import CallbackContext
from handlers import is_running

def status(update: Update, context: CallbackContext):
    if is_running:
        update.message.reply_text("Аналіз зараз активний ✅", parse_mode="Markdown")
    else:
        update.message.reply_text("Аналіз зараз неактивний ❌", parse_mode="Markdown")
