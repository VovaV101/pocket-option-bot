import os
from queue import Queue
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import (
    Dispatcher, CommandHandler, MessageHandler, Filters, CallbackContext, JobQueue
)
from src.config import pairs_list
from src.handlers import start, pairs, pair_selected, turn_on, turn_off
from src.status_report import status
# Отримання токена та вебхука з середовища
TOKEN = os.environ["TELEGRAM_TOKEN"]
WEBHOOK_URL = os.environ["WEBHOOK_URL"]

# Ініціалізація Flask
app = Flask(__name__)
bot = Bot(token=TOKEN)

# Ініціалізація Dispatcher із чергою
update_queue = Queue()
dispatcher = Dispatcher(bot, update_queue, workers=4, use_context=True)

# Створення і запуск JobQueue
job_queue = JobQueue()
job_queue.set_dispatcher(dispatcher)
job_queue.start()

# Передача job_queue у dispatcher
dispatcher.bot_data["job_queue"] = job_queue

# Реєстрація команд
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("pairs", pairs))
dispatcher.add_handler(CommandHandler("on", turn_on))
dispatcher.add_handler(CommandHandler("off", turn_off))
dispatcher.add_handler(CommandHandler("status", status))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, pair_selected))

# Webhook для Telegram
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok", 200

@app.route("/")
def home():
    return "Бот активний!"

@app.route("/analyze", methods=["GET"])
def analyze_now():
    from src.signals import analyze_job
    chat_id = os.environ.get("CHAT_ID")
    if chat_id:
        analyze_job(None, chat_id=chat_id)
        return "Аналіз виконано!", 200
    else:
        return "CHAT_ID не встановлено.", 400


if __name__ == "__main__":
    bot.delete_webhook()
    bot.set_webhook(url=f"{WEBHOOK_URL}/{TOKEN}")
    print(f"Webhook встановлено: {WEBHOOK_URL}/{TOKEN}")
    app.run(host="0.0.0.0", port=8000)
