from telegram import Update
from telegram.ext import CallbackContext
from signals import analyze_job

# Стан бота: чи запущений аналіз
analysis_active = False

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "Привіт! Я твій бот для торгових сигналів.\nЩоб вибрати валютні пари — напиши /pairs."
    )

def pairs(update: Update, context: CallbackContext) -> None:
    pairs_list = [
        "EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD", "USD/CAD",
        "EUR/JPY", "GBP/JPY", "EUR/GBP", "NZD/USD", "USD/CHF"
    ]
    pairs_text = ", ".join(pairs_list)
    update.message.reply_text(
        f"Вибери одну або кілька валютних пар через кому:\n\n{pairs_text}"
    )

def pair_selected(update: Update, context: CallbackContext) -> None:
    text = update.message.text.upper().replace(" ", "")
    selected_pairs = text.split(",")
    context.chat_data["selected_pairs"] = selected_pairs
    update.message.reply_text(f"Вибрані пари: {', '.join(selected_pairs)}")

def turn_on(update: Update, context: CallbackContext) -> None:
    global analysis_active
    if analysis_active:
        update.message.reply_text("Аналіз вже активний.")
    else:
        if context.job_queue is not None:
            context.job_queue.run_repeating(analyze_job, interval=300, first=1, context=update.message.chat_id)
            analysis_active = True
            update.message.reply_text("Аналіз запущено!")
        else:
            update.message.reply_text("Помилка: job_queue недоступний!")

def turn_off(update: Update, context: CallbackContext) -> None:
    global analysis_active
    if analysis_active:
        context.job_queue.stop()
        analysis_active = False
        update.message.reply_text("Аналіз зупинено!")
    else:
        update.message.reply_text("Аналіз і так неактивний.")
