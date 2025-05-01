import os
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import (
    Dispatcher, CommandHandler, MessageHandler, filters, CallbackContext
)
from config import pairs_list
from handlers import start, pairs, pair_selected, turn_on, turn_off
from status_report import status

# Отримання токена та вебхука з середовища
TOKEN = os.environ["TELEGRAM_TOKEN"]
WEBHOOK_URL = os.environ["WEBHOOK_URL"]

# Ініціалізація Flask
app = Flask(__name__)
bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot, None, workers=4, use_context=True)

# === Реєстрація команд ===
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("pairs", pairs))
dispatcher.add_handler(CommandHandler("on", turn_on))
dispatcher.add_handler(CommandHandler("off", turn_off))
dispatcher.add_handler(CommandHandler("status", status))
dispatcher.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, pair_selected))

# === Webhook для Telegram ===
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    """Приймає оновлення від Telegram."""
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok", 200

@app.route("/")
def home():
    """Проста відповідь для перевірки що сервер працює."""
    return "Бот активний!"

if __name__ == "__main__":
    bot.delete_webhook()
    bot.set_webhook(url=f"{WEBHOOK_URL}/{TOKEN}")
    app.run(host="0.0.0.0", port=8000)
