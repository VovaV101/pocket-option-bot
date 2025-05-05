import os
import threading
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters
)
from src.config import TELEGRAM_TOKEN, WEBHOOK_URL
from src.handlers import start, pairs, pair_selected, turn_on, turn_off
from src.status_report import send_status

# Ініціалізація Flask
app = Flask(__name__)

# Ініціалізація Telegram бота
application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

# Додаємо обробники команд
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("pairs", pairs))
application.add_handler(CommandHandler("on", turn_on))
application.add_handler(CommandHandler("off", turn_off))
application.add_handler(CommandHandler("status", send_status))
application.add_handler(CallbackQueryHandler(pair_selected))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, pair_selected))

# Обробка Webhook від Telegram
@app.route(f'/{TELEGRAM_TOKEN}', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    asyncio.run(application.process_update(update))
    return "ok", 200

# Просто домашня сторінка
@app.route('/')
def index():
    return "Бот працює!"

def run_application():
    asyncio.run(application.initialize())
    asyncio.run(application.start())
    asyncio.run(application.updater.start_polling())

if __name__ == '__main__':
    application.bot.delete_webhook()
    application.bot.set_webhook(url=f"{WEBHOOK_URL}/{TELEGRAM_TOKEN}")
    print(f"Webhook встановлено: {WEBHOOK_URL}/{TELEGRAM_TOKEN}")

    # Запуск Flask у окремому потоці
    threading.Thread(target=lambda: app.run(host="0.0.0.0", port=8000)).start()
