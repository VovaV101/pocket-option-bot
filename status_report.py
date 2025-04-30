# status_report.py

from telegram import Update
from telegram.ext import CallbackContext
from config import analyzing, selected_pairs, last_signal_time

def status(update: Update, context: CallbackContext):
    if not analyzing:
        update.message.reply_text("Аналіз зараз не запущений.")
        return

    if not selected_pairs:
        update.message.reply_text("Жодна валютна пара не вибрана для аналізу.")
        return

    report = "Статус аналізу:\n"
    for pair in selected_pairs:
        pair_name = [k for k, v in context.bot_data["pairs_list"].items() if v == pair][0]
        last_time = last_signal_time.get(pair, "немає сигналів")
        report += f"{pair_name}: останній сигнал о {last_time}\n"

    update.message.reply_text(report)
