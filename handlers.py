from telegram import Update
from telegram.ext import CallbackContext
from signals import analyze
from config import pairs_list

# Глобальний прапор для контролю статусу аналізу
is_running = False

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Привіт! Я твій бот для торгових сигналів.\n"
        "Щоб вибрати валютні пари — напиши /pairs."
    )

def pairs(update: Update, context: CallbackContext):
    available_pairs = ", ".join(pairs_list)
    update.message.reply_text(
        f"Вибери одну або кілька валютних пар:\n\n{available_pairs}"
    )

def pair_selected(update: Update, context: CallbackContext):
    text = update.message.text.upper().replace(" ", "")
    selected = text.split(",")
    valid = [p for p in selected if p in pairs_list]
    if valid:
        context.user_data["selected_pairs"] = valid
        update.message.reply_text(f"Вибрані пари: {', '.join(valid)}")
    else:
        update.message.reply_text("Не знайдено жодної валідної пари. Спробуй ще раз.")

def turn_on(update: Update, context: CallbackContext):
    global is_running

    if is_running:
        update.message.reply_text("Аналіз уже активний.")
        return

    if not context.user_data.get("selected_pairs"):
        update.message.reply_text("Будь ласка, спочатку вибери пари за допомогою /pairs.")
        return

    if not hasattr(context.application, 'job_queue') or context.application.job_queue is None:
        update.message.reply_text("Помилка: job_queue недоступний!")
        return

    context.application.job_queue.run_repeating(
        analyze,
        interval=300,  # 5 хвилин
        first=1,
        context={"chat_id": update.effective_chat.id, "pairs": context.user_data["selected_pairs"]}
    )

    is_running = True
    update.message.reply_text("Аналіз запущено!")

def turn_off(update: Update, context: CallbackContext):
    global is_running

    if not is_running:
        update.message.reply_text("Аналіз і так неактивний.")
        return

    context.application.job_queue.stop()
    is_running = False
    update.message.reply_text("Аналіз зупинено.")
