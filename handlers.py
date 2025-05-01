from telegram import Update
from telegram.ext import CallbackContext
from config import pairs_list, pair_selected_list, TIMEFRAME_MINUTES
from signals import get_signal

selected_pairs = []

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Привіт! Я твій бот для торгових сигналів.\nЩоб вибрати валютні пари — напиши /pairs."
    )

def pairs(update: Update, context: CallbackContext):
    pairs_str = ", ".join(pairs_list)
    update.message.reply_text(f"Вибери одну або кілька валютних пар:\n\n{pairs_str}")

def pair_selected(update: Update, context: CallbackContext):
    global selected_pairs
    text = update.message.text.upper()
    selected = [pair.strip() for pair in text.split(",") if pair.strip() in pairs_list]

    if selected:
        selected_pairs = selected
        update.message.reply_text(f"Вибрані пари: {', '.join(selected_pairs)}")
    else:
        update.message.reply_text("Невірний формат. Спробуй ще раз.")

def run_analysis(context: CallbackContext):
    for pair in selected_pairs:
        signal = get_signal(pair)
        if signal:
            context.bot.send_message(chat_id=context.job.chat_id, text=signal)

def turn_on(update: Update, context: CallbackContext):
    if not selected_pairs:
        update.message.reply_text("Спочатку вибери валютні пари командою /pairs.")
        return

    context.job_queue.run_repeating(run_analysis, interval=TIMEFRAME_MINUTES * 60, first=1, chat_id=update.effective_chat.id)
    update.message.reply_text("Аналіз запущено.")

def turn_off(update: Update, context: CallbackContext):
    context.job_queue.stop()
    update.message.reply_text("Аналіз зупинено.")
