import os
import threading
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from src.config import TELEGRAM_TOKEN, WEBHOOK_URL
from src.handlers import start, pairs, pair_selected, turn_on, turn_off
from src.status_report import send_status

app = Flask(__name__)

# Створюємо Application
application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

# Додаємо обробники
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("pairs", pairs))
application.add_handler(CommandHandler("on", turn_on))
application.add_handler(CommandHandler("off", turn_off))
application.add_handler(CommandHandler("status", send_status))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, pair_selected))

# Flask маршрут для Webhook
@app.route(f"/{TELEGRAM_TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.create_task(application.process_update(update))
    return "ok", 200

@app.route("/")
def home():
    return "Бот працює!"

def run_application():
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    # Видаляємо старий Webhook і ставимо новий
    application.bot.delete_webhook()
    application.bot.set_webhook(url=f"{WEBHOOK_URL}/{TELEGRAM_TOKEN}")
    print(f"Webhook встановлено: {WEBHOOK_URL}/{TELEGRAM_TOKEN}")

    # Запускаємо обробник Telegram у фоні
    threading.Thread(target=run_application).start()

    # Запускаємо Flask сервер
    app.run(host="0.0.0.0", port=8000)
