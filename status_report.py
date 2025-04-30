from telegram import Update
from telegram.ext import CallbackContext
from config import last_signal, last_signal_time

def status(update: Update, context: CallbackContext):
    if not last_signal:
        update.message.reply_text("Сигналів ще не було.")
        return

    message = "Останні сигнали:\n"
    for pair, signal in last_signal.items():
        time_str = last_signal_time.get(pair, "—")
        message += f"{pair}: {signal} о {time_str}\n"

    update.message.reply_text(message)
