from telegram import Update
from telegram.ext import CallbackContext
from signals import analyze
from config import pairs_list

# Глобальні змінні для статусу
is_analysis_running = False
selected_pairs = []

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Привіт! Я твій бот для торгових сигналів.\nЩоб вибрати валютні пари — напиши /pairs.")

def pairs(update: Update, context: CallbackContext):
    text = "Вибери одну або кілька валютних пар:\n\n"
    text += ", ".join(pairs_list)
    update.message.reply_text(text)

def pair_selected(update: Update, context: CallbackContext):
    global selected_pairs
    text = update.message.text.upper()
    pairs = [pair.strip() for pair in text.split(",")]

    valid_pairs = [pair for pair in pairs if pair in pairs_list]

    if valid_pairs:
        selected_pairs = valid_pairs
        update.message.reply_text(f"Вибрані пари: {', '.join(selected_pairs)}")
    else:
        update.message.reply_text("Не знайдено правильних пар. Спробуй ще раз.")

def run_analysis(context: CallbackContext):
    for pair in selected_pairs:
        analyze(pair, context.bot, context.job.context)

def turn_on(update: Update, context: CallbackContext):
    global is_analysis_running

    if is_analysis_running:
        update.message.reply_text("Аналіз вже активний.")
        return

    # Перевірка чи job_queue існує
    if context.job_queue:
        chat_id = update.message.chat_id
        context.job_queue.run_repeating(run_analysis, interval=300, first=1, context=chat_id)
        is_analysis_running = True
        update.message.reply_text("Аналіз увімкнено ✅")
    else:
        update.message.reply_text("Помилка: job_queue недоступний!")

def turn_off(update: Update, context: CallbackContext):
    global is_analysis_running

    if is_analysis_running:
        context.job_queue.stop()
        is_analysis_running = False
        update.message.reply_text("Аналіз вимкнено ❌")
    else:
        update.message.reply_text("Аналіз і так не запущений.")
