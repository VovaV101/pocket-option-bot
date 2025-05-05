from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext
from src.config import pairs_list
from src.signals import analyze_job

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Привіт! Я твій бот для сигналів.\n"
        "Використай команду /pairs для вибору валютних пар."
    )

def pairs(update: Update, context: CallbackContext):
    keyboard = [[pair] for pair in pairs_list.keys()]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    update.message.reply_text("Оберіть валютні пари для аналізу:", reply_markup=markup)

def pair_selected(update: Update, context: CallbackContext):
    selected_pairs = context.bot_data.setdefault("selected_pairs", [])
    text = update.message.text
    if text in pairs_list:
        symbol = pairs_list[text]
        if symbol not in selected_pairs:
            selected_pairs.append(symbol)
            update.message.reply_text(f"✅ Додано пару: {text}")
        else:
            update.message.reply_text(f"⚠️ Пара {text} вже обрана.")
    else:
        update.message.reply_text("⚠️ Будь ласка, оберіть валютну пару зі списку через /pairs.")

def turn_on(update: Update, context: CallbackContext):
    analyzing = context.bot_data.get("analyzing", False)
    if not analyzing:
        job_queue = context.bot_data["job_queue"]
        job = job_queue.run_repeating(analyze_job, interval=300, first=1, context=update.message.chat_id)
        context.bot_data["analyzing"] = True
        context.bot_data["job_reference"] = job
        update.message.reply_text("✅ Аналіз увімкнено!")
    else:
        update.message.reply_text("⚠️ Аналіз вже активний.")

def turn_off(update: Update, context: CallbackContext):
    job = context.bot_data.get("job_reference")
    if job:
        job.schedule_removal()
        context.bot_data["analyzing"] = False
        context.bot_data["job_reference"] = None
        update.message.reply_text("⛔ Аналіз вимкнено.")
    else:
        update.message.reply_text("⚠️ Аналіз вже вимкнений або не запущений.")
