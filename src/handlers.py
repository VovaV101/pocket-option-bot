from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContex
from src.config import pairs_list, job_reference
from src.signals import analyze_job

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Привіт! Я твій бот для сигналів. Використай команду /pairs для вибору валютних пар.")

def pairs(update: Update, context: CallbackContext):
    keyboard = [[pair] for pair in pairs_list.keys()]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    update.message.reply_text("Оберіть валютні пари для аналізу:", reply_markup=markup)

def pair_selected(update: Update, context: CallbackContext):
    global selected_pairs
    text = update.message.text
    if text in pairs_list:
        selected_pairs.append(pairs_list[text])
        context.bot_data["selected_pairs"] = selected_pairs  # оновлюємо в bot_data
        update.message.reply_text(f"Додано пару: {text}")
    else:
        update.message.reply_text("Будь ласка, оберіть валютну пару зі списку через /pairs.")

def turn_on(update: Update, context: CallbackContext):
    global analyzing, job_reference
    if not analyzing:
        analyzing = True
        job_queue = context.bot_data.get("job_queue")
        if job_queue:
            job_reference = job_queue.run_repeating(
                analyze_job,
                interval=300,  # кожні 5 хвилин
                first=1,
                context=update.message.chat_id
            )
            update.message.reply_text("Аналіз увімкнено!")
        else:
            update.message.reply_text("Помилка: JobQueue не знайдено!")
    else:
        update.message.reply_text("Аналіз вже працює.")

def turn_off(update: Update, context: CallbackContext):
    global analyzing, job_reference
    if analyzing and job_reference:
        job_reference.schedule_removal()
        analyzing = False
        update.message.reply_text("Аналіз вимкнено.")
    else:
        update.message.reply_text("Аналіз вже вимкнений або не запущений.")
