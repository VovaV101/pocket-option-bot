from telegram import Update
from telegram.ext import CallbackContext

def status(update: Update, context: CallbackContext):
    analyzing = context.bot_data.get("analyzing_ref", lambda: False)()
    if analyzing:
        update.message.reply_text("Аналіз зараз *запущений*.", parse_mode="Markdown")
    else:
        update.message.reply_text("Аналіз зараз *не запущений*.", parse_mode="Markdown")
