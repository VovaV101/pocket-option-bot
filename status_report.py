# status_report.py

from telegram import Update
from telegram.ext import CallbackContext

def status(update: Update, context: CallbackContext):
    """Команда /status для перевірки чи аналіз запущений."""
    analyzing_func = context.bot_data.get("analyzing_ref")
    if analyzing_func and analyzing_func():
        update.message.reply_text("Аналіз зараз *запущений*.", parse_mode="Markdown")
    else:
        update.message.reply_text("Аналіз зараз *не запущений*.", parse_mode="Markdown")
