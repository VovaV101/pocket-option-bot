import os
from flask import Flask, request
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, filters
)
from src.config import TELEGRAM_TOKEN, WEBHOOK_URL
from src.handlers import start, pairs, pair_selected, turn_on, turn_off
from src.status_report import send_signal

app = Flask(__name__)
application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

# Обов'язково: встановлюємо application у signals.py
import src.signals
src.signals.application = application

# Реєстрація обробників команд
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("pairs", pairs))
application.add_handler(CommandHandler("on", turn_on))
application.add_handler(CommandHandler("off", turn_off))
application.add_handler(CommandHandler("status", send_signal))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, pair_selected))

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
