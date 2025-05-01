from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext
from config import pairs_list
from signals import analyze_job

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Привіт! Я твій бот для торгових сигналів.\n"
        "Щоб вибрати валютні пари — напиши /pairs."
    )

def pairs(update: Update, context: CallbackContext):
    keyboard = [[pair] for pair in pairs_list.keys()]
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_text(
        "Вибери валютну пару для аналізу:",
        reply_markup=markup
    )

def pair_selected(update: Update, context: CallbackContext):
    text = update.message.text
    if text in pairs_list:
        selected = context.bot_data.get("selected_pairs", [])
        selected.append(pairs_list[text])
        context.bot_data["selected_pairs"] = selected

        update.message.reply_text(
            f"Пара {text} додана для аналізу.\n"
            "Щоб обрати ще одну пару — вибери зі списку.\n"
            "Щоб почати аналіз — напиши /on."
        )
    else:
        update.message.reply_text(
            "Будь ласка, обери валютну пару зі списку!"
        )

def turn_on(update: Update, context: CallbackContext):
    analyzing = context.bot_data.get("analyzing", False)
    if not analyzing:
        job = context.job_queue.run_repeating(
            analyze_job, interval=300, first=1, context=update.message.chat_id
        )
        context.bot_data["analyzing"] = True
        context.bot_data["job"] = job
        update.message.reply_text("Аналіз увімкнено!")
    else:
        update.message.reply_text("Аналіз уже запущений.")

def turn_off(update: Update, context: CallbackContext):
    analyzing = context.bot_data.get("analyzing", False)
    job = context.bot_data.get("job")
    if analyzing and job:
        job.schedule_removal()
        context.bot_data["analyzing"] = False
        context.bot_data["job"] = None
        update.message.reply_text("Аналіз вимкнено.")
    else:
        update.message.reply_text("Аналіз зараз не запущений.")
