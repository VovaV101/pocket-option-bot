from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    CommandHandler, CallbackQueryHandler, ContextTypes
)
from src.signals import analyze_pair, selected_pairs
from src.config import PAIRS
from src import signals  # ← для доступу до debug_mode і last_debug_output

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [[InlineKeyboardButton(pair, callback_data=pair)] for pair in PAIRS]
    markup = InlineKeyboardMarkup(buttons)
    await update.message.reply_text(
        "Привіт! Я бот для пошуку сигналів на Pocket Option.\n\n"
        "Оберіть валютні пари для аналізу (натискаючи кнопки нижче).\n"
        "Коли оберете пари — введіть команду /run для запуску моніторингу.\n"
        "Перевірити статус бота: /status.",
        reply_markup=markup
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    pair = query.data
    if pair not in selected_pairs:
        selected_pairs.append(pair)
    selected_text = ', '.join(selected_pairs)
    await query.message.reply_text(f"Ви обрали: {selected_text}\nТепер напишіть /run для старту!")

async def run(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not selected_pairs:
        await update.message.reply_text("Спочатку оберіть валютні пари через /start!")
        return
    if context.application.job_queue:
        context.application.job_queue.run_repeating(
            callback=check_signals,
            interval=300,
            first=0,
            chat_id=update.effective_chat.id
        )
    await update.message.reply_text("Аналіз розпочато! Чекайте сигнали кожні 5 хвилин.")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if selected_pairs:
        selected = ', '.join(selected_pairs)
        await update.message.reply_text(f"Бот активний. Обрані пари: {selected}. Перевірка кожні 5 хвилин!")
    else:
        await update.message.reply_text("Бот активний, але валютні пари ще не обрано. Використайте /start.")

async def pairs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if selected_pairs:
        selected = ', '.join(selected_pairs)
        await update.message.reply_text(f"Обрані пари: {selected}")
    else:
        await update.message.reply_text("Ви ще не обрали валютні пари. Використайте /start.")

async def check_signals(context: ContextTypes.DEFAULT_TYPE):
    for pair in selected_pairs:
        signal = analyze_pair(pair)
        if signal:
            await context.bot.send_message(
                chat_id=context.job.chat_id,
                text=f"Сигнал для {pair}: {signal} на 15 хвилин"
            )

async def test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ТЕСТОВИЙ СИГНАЛ: EUR/USD UP на 15 хвилин")

async def debug(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logs = []

    if not selected_pairs:
        await update.message.reply_text("Немає обраних пар для аналізу.")
        return

    signals.debug_mode = True  # Увімкнути режим дебагу

    for pair in selected_pairs:
        try:
            signal = analyze_pair(pair)
            if signal:
                logs.append(f"{pair}: Сигнал {signal}")
            else:
                logs.append(f"{pair}: Немає чіткого сигналу.")
            logs.extend(signals.last_debug_output)
        except Exception as e:
            logs.append(f"{pair}: Помилка при аналізі: {e}")

    signals.debug_mode = False  # Вимкнути після аналізу

    # Telegram обмежує повідомлення до 4096 символів
    for i in range(0, len(logs), 40):
        await update.message.reply_text("\n".join(logs[i:i+40]))

def setup_handlers(app):
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(CommandHandler("run", run))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("pairs", pairs))
    app.add_handler(CommandHandler("test", test))
    app.add_handler(CommandHandler("debug", debug))
