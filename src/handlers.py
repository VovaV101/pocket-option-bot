from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
)
from src.scheduler import start_scheduler, stop_scheduler
from src.signals import selected_pairs, set_selected_pairs, get_last_check_time

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [
        [InlineKeyboardButton(pair, callback_data=pair)] for pair in selected_pairs
    ]
    markup = InlineKeyboardMarkup(buttons)
    await update.message.reply_text(
        "Привіт! Я бот для пошуку сигналів на Pocket Option.\n\n"
        "Ось що ви можете зробити:\n"
        "- Оберіть валютні пари для аналізу (натискаючи кнопки нижче).\n"
        "- Коли оберете пари — введіть команду /run для запуску моніторингу.\n"
        "- Перевірити статус бота можна командою /status.\n\n"
        "Успішної торгівлі!",
        reply_markup=markup
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    pair = query.data
    set_selected_pairs(pair)
    await query.edit_message_text(text=f"Ви обрали: {', '.join(selected_pairs)}\nКоли будете готові, напишіть /run")

async def run(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Аналіз обраних пар розпочато!")
    start_scheduler(context.application)

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    last_time = get_last_check_time()
    status_msg = f"Бот активний.\nОстання перевірка: {last_time}"
    await update.message.reply_text(status_msg)

def setup_handlers(app):
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(CommandHandler("run", run))
    app.add_handler(CommandHandler("status", status))
