import os
from queue import Queue
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import (
    Application, ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext
)
from src.config import TELEGRAM_TOKEN, WEBHOOK_URL
from src.handlers import start, pairs, pair_selected, turn_on, turn_off
from src.status_report import send_signal

# Flask сервер
app = Flask(__name__)

# Ініціалізація Telegram бота через ApplicationBuilder
application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

# Реєстрація обробників команд
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("pairs", pairs))
application.add_handler(CommandHandler("on", turn_on))
application.add_handler(CommandHandler("off", turn_off))
application.add_handler(CommandHandler("status", status))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, pair_selected))

# Flask маршрут для Webhook
@app.route(f"/{TELEGRAM_TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put(update)
    return "ok", 200

@app.route("/")
def home():
    return "Бот працює!"

if __name__ == "__main__":
    application.bot.delete_webhook()
    application.bot.set_webhook(url=f"{WEBHOOK_URL}/{TELEGRAM_TOKEN}")
    print(f"Webhook встановлено: {WEBHOOK_URL}/{TELEGRAM_TOKEN}")
    app.run(host="0.0.0.0", port=8000)
