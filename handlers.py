# handlers.py

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext
from config import pairs_list, selected_pairs, analyzing
from signals import analyze

job_reference = None  # Посилання на активну задачу аналізу

def start(update: Update, context: CallbackContext):
    """Команда /start."""
    update.message.reply_text("Привіт! Я твій бот для сигналів. Використай /pairs щоб вибрати валютні пари.")

def pairs(update: Update, context: CallbackContext):
    """Команда /pairs для вибору валютних пар."""
    keyboard = [[pair] for pair in pairs_list.keys()]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    update.message.reply_text("Вибери валютну пару:", reply_markup=markup)

def pair_selected(update: Update, context: CallbackContext):
    """Коли користувач вибирає пару."""
    global selected_pairs
    text = update.message.text
    if text in pairs_list:
        selected_pairs.append(pairs_list[text])
        update.message.reply_text(f"Пара {text} додана для аналізу.\n\nЩоб обрати ще одну пару — вибери зі списку.\nЩоб почати аналіз — напиши /on.")
    else:
        update.message.reply_text("Натисни на валюту із списку!")

def turn_on(update: Update, context: CallbackContext):
    """Команда /on для запуску аналізу."""
    global analyzing, job_reference
    if not analyzing:
        analyzing = True
        job_reference = context.job_queue.run_repeating(analyze, interval=300, first=1, context=update.message.chat_id)
        context.bot_data["analyzing_ref"] = lambda: True
        update.message.reply_text("Аналіз увімкнено!")
    else:
        update.message.reply_text("Аналіз вже працює.")

def turn_off(update: Update, context: CallbackContext):
    """Команда /off для зупинки аналізу."""
    global analyzing, job_reference
    if analyzing and job_reference:
        job_reference.schedule_removal()
        analyzing = False
        context.bot_data["analyzing_ref"] = lambda: False
        update.message.reply_text("Аналіз вимкнено.")
    else:
        update.message.reply_text("Аналіз вже не активний.")
