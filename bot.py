import os
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import (
    Application, ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters
)
from src.config import TELEGRAM_TOKEN, WEBHOOK_URL
from src.handlers import start, pairs, pair_selected, turn_on, turn_off
from src.status_report import send_status

# Flask додаток
app = Flask(__name__)

# Ініціалізація бота
application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

# Реєстрація команд
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("pairs", pairs))
application.add_handler(CommandHandler("on", turn_on))
application.add_handler(CommandHandler("off", turn_off))
application.add_handler(CommandHandler("status", send_status))
application.add_handler(CallbackQueryHandler(pair_selected))

# Маршрути Flask
@app.route(f"/{TELEGRAM_TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put(update)
    return "ok", 200

@app.route("/", methods=["GET"])
def home():
    return "Бот працює!"

# Старт програми
if __name__ == "__main__":
    bot = Bot(token=TELEGRAM_TOKEN)
    bot.delete_webhook()
    bot.set_webhook(url=f"{WEBHOOK_URL}/{TELEGRAM_TOKEN}")
    print(f"Webhook встановлено на {WEBHOOK_URL}/{TELEGRAM_TOKEN}")
    app.run(host="0.0.0.0", port=8000)
