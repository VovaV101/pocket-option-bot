from telegram import Update
from telegram.ext import CallbackContext
from signals import get_signal
from config import pairs_list, TIMEFRAME_MINUTES

# Глобальний прапор для контролю
is_running = False

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Привіт! Я твій бот для торгових сигналів.\n"
        "Щоб вибрати валютні пари — напиши /pairs."
    )

def pairs(update: Update, context: CallbackContext):
    available_pairs = ", ".join(pairs_list)
    update.message.reply_text(
        f"Вибери одну або кілька валютних пар через кому:\n\n{available_pairs}"
    )

def pair_selected(update: Update, context: CallbackContext):
    text = update.message.text.upper().replace(" ", "")
    selected = text.split(",")
    valid = [p for p in selected if p in pairs_list]
    if valid:
        context.user_data["selected_pairs"] = valid
        update.message.reply_text(f"Вибрані пари: {', '.join(valid)}")
    else:
        update.message.reply_text("Не знайдено валідних пар. Спробуй ще раз.")

def analyze_job(context: CallbackContext):
    job_data = context.job.context
    chat_id = job_data["chat_id"]
    selected_pairs = job_data["pairs"]

    for pair in selected_pairs:
        signal = get_signal(pair)
        if signal:
            context.bot.send_message(chat_id=chat_id, text=signal)

def turn_on(update: Update, context: CallbackContext):
    global is_running

    if is_running:
        update.message.reply_text("Аналіз уже запущено.")
        return

    if not context.user_data.get("selected_pairs"):
        update.message.reply_text("Будь ласка, спочатку вибери пари через /pairs.")
        return

    if not hasattr(context.application, 'job_queue') or context.application.job_queue is None:
        update.message.reply_text("Помилка: job_queue недоступний!")
        return

    context.application.job_queue.run_repeating(
        analyze_job,
        interval=300,  # 5 хвилин
        first=1,
        context={"chat_id": update.effective_chat.id, "pairs": context.user_data["selected_pairs"]}
    )

    is_running = True
    update.message.reply_text(f"Аналіз запущено! Перевірка кожні {TIMEFRAME_MINUTES} хвилин.")

def turn_off(update: Update, context: CallbackContext):
    global is_running

    if not is_running:
        update.message.reply_text("Аналіз вже вимкнений.")
        return

    context.application.job_queue.stop()
    is_running = False
    update.message.reply_text("Аналіз зупинено.")
