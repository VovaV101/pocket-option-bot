from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    CommandHandler, CallbackQueryHandler, ContextTypes
)
from src.signals import analyze_pair
from src.scheduler import start_scheduler, stop_scheduler
from src.config import PAIRS
import asyncio

selected_pairs = []
monitoring = False  # Чи йде моніторинг

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global monitoring
    monitoring = False  # Обнуляємо при новому старті
    buttons = [
        [InlineKeyboardButton(pair, callback_data=pair)] for pair in PAIRS
    ]
    markup = InlineKeyboardMarkup(buttons)
    await update.message.reply_text(
        "Привіт! Я бот для пошуку сигналів на Pocket Option.\n\n"
        "Оберіть валютні пари для аналізу (натискаючи кнопки нижче).\n"
        "Коли оберете пари — введіть команду /run для запуску моніторингу.\n"
        "Перевірити статус бота: /status.\n"
        "Переглянути обрані пари: /pairs.",
        reply_markup=markup
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    pair = query.data
    if pair not in selected_pairs:
        selected_pairs.append(pair)
    selected_text = ', '.join(selected_pairs)
    await query.edit_message_text(text=f"Ви обрали: {selected_text}\nТепер напишіть /run для старту!")

async def run(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global monitoring
    if not selected_pairs:
        await update.message.reply_text("Спочатку оберіть валютні пари через /start!")
        return
    monitoring = True
    await update.message.reply_text("Аналіз розпочато! Чекайте сигнали кожні 5 хвилин.")
    context.job_queue.run_repeating(check_signals, interval=300, first=0, chat_id=update.effective_chat.id)

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if monitoring:
        selected_text = ', '.join(selected_pairs) if selected_pairs else "жодної пари не обрано"
        await update.message.reply_text(f"Бот активний. Слідкую за парами: {selected_text} кожні 5 хвилин!")
    else:
        await update.message.reply_text("Бот не моніторить. Введіть /start і оберіть пари.")

async def pairs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if selected_pairs:
        selected_text = ', '.join(selected_pairs)
        await update.message.reply_text(f"Обрані пари: {selected_text}")
    else:
        await update.message.reply_text("Ще не обрано жодної пари. Введіть /start!")

async def check_signals(context: ContextTypes.DEFAULT_TYPE):
    for pair in selected_pairs:
        signal = analyze_pair(pair)
        if signal:
            await context.bot.send_message(
                chat_id=context.job.chat_id,
                text=f"Сигнал для {pair}: {signal} на 15 хвилин"
            )

def setup_handlers(app):
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(CommandHandler("run", run))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("pairs", pairs))
