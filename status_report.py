from telegram import Update
from telegram.ext import CallbackContext
from handlers import is_running

def status(update: Update, context: CallbackContext):
    if is_running:
        update.message.reply_text("Аналіз зараз активний ✅")
    else:
        update.message.reply_text("Аналіз зараз неактивний ❌")
