
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext
from src.config import pairs_list
from src.signals import analyze_job

def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    context.bot_data.setdefault("selected_pairs", DEFAULT_PAIRS.copy())
    context.bot_data.setdefault("last_signal", {})
    context.bot_data.setdefault("last_signal_time", {})

    update.message.reply_text(
        "✅ Бот готовий до роботи!\n"
        "Щоб побачити статус аналізу, використайте команду /status."
    )

def pairs(update: Update, context: CallbackContext):
    keyboard = [[pair] for pair in pairs_list.keys()]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    update.message.reply_text("Оберіть валютні пари для аналізу:", reply_markup=markup)

def pair_selected(update: Update, context: CallbackContext):
    text = update.message.text
    selected_pairs = context.bot_data.setdefault("selected_pairs", [])

    if text in pairs_list:
        selected_pairs.append(pairs_list[text])
        update.message.reply_text(f"Додано пару: {text}")
    else:
        update.message.reply_text("Будь ласка, оберіть валютну пару зі списку через /pairs.")

def turn_on(update: Update, context: CallbackContext):
    if not context.bot_data.get("analyzing", False):
        context.bot_data["analyzing"] = True
        job_queue = context.bot_data["job_queue"]
        job_reference = job_queue.run_repeating(
            analyze_job,
            interval=300,
            first=1,
            context=update.message.chat_id
        )
        context.bot_data["job_reference"] = job_reference
        update.message.reply_text("Аналіз увімкнено!")
    else:
        update.message.reply_text("Аналіз вже працює.")

def turn_off(update: Update, context: CallbackContext):
    if context.bot_data.get("analyzing", False) and context.bot_data.get("job_reference"):
        context.bot_data["job_reference"].schedule_removal()
        context.bot_data["analyzing"] = False
        context.bot_data["job_reference"] = None
        update.message.reply_text("Аналіз вимкнено.")
    else:
        update.message.reply_text("Аналіз вже вимкнений або не запущений.")
