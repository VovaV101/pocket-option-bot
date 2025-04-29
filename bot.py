from flask import Flask
from telegram.ext import CommandHandler, Dispatcher, Updater
import threading

TOKEN = "7781796905:AAG5qRJ4w2VTEyISAkmtE3bUILTAo9s-9xc"
app = Flask(__name__)

def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=(
            "Привіт! Я твій бот для трейдингу на Pocket Option.\n\n"
            "📈 Даю сигнали з точним входом\n"
            "⏱️ Аналізую старші таймфрейми\n"
            "⚙️ Працюю на індикаторах і свічкових патернах\n"
            "✅ Автоматичний режим — чекай сигналів!"
        )
    )

def run_bot():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    updater.start_polling()
    updater.idle()

@app.route('/')
def home():
    return "Бот активний!"

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=8000)
