# handlers.py

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext
from config import pairs_list
from signals import analyze

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Привіт! Я бот для автоматичних сигналів.\n"
        "Використай команду /pairs щоб вибрати валютні пари."
    )

def pairs(update: Update, context: CallbackContext):
    keyboard = [[pair] for pair in pairs_list.keys()]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    update.message.reply_text(
        "Вибери валютні пари для аналізу:\n"
        "(Можна вибрати кілька пар через кому)",
        reply_markup=markup
    )

def pair_selected(update: Update, context: CallbackContext):
    text = update.message.text
    pairs = [pair.strip() for pair in text.split(",")]
    selected = []
    for pair in pairs:
        if pair in pairs_list:
            selected.append(pairs_list[pair])

    if selected:
        context.bot_data["selected_pairs"] = selected
        update.message.reply_text(f"Пари вибрані для аналізу: {', '.join(pairs)}")
    else:
        update.message.reply_text("Некоректний вибір. Використай /pairs ще раз.")

def turn_on(update: Update, context: CallbackContext):
    if not context.bot_data.get("analyzing", False):
        context.bot_data["analyzing"] = True
        context.bot_data["job"] = context.job_queue.run_repeating(analyze, interval=300, first=1, context=update.message.chat_id)
        update.message.reply_text("Аналіз увімкнено!")
    else:
        update.message.reply_text("Аналіз вже працює.")

def turn_off(update: Update, context: CallbackContext):
    if context.bot_data.get("analyzing", False):
        job = context.bot_data.get("job")
        if job:
            job.schedule_removal()
        context.bot_data["analyzing"] = False
        update.message.reply_text("Аналіз вимкнено.")
    else:
        update.message.reply_text("Аналіз вже вимкнений.")
