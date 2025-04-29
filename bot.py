from flask import Flask
import telegram
from telegram.ext import CommandHandler, Dispatcher, Updater
import threading

TOKEN = "7713898071:AAG9Xe23F_pqR4dGKeWFtJw-_h6Ke62wrLk"
bot = telegram.Bot(token=TOKEN)
app = Flask(__name__)

def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=(
            "Привіт! Я твій особистий бот для трейдингу.\n\n"
            "📈 Даю точні сигнали для входу на Pocket Option\n"
            "⏱️ Аналізую ринок на старших таймфреймах\n"
            "⚙️ Сигнали формуються на основі індикаторів та патернів\n"
            "🛠️ Працюю автоматично 24/7\n\n"
            "Чекай на сигнали — скоро буде перший!"
        )
    )

def run_bot():
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    updater.start_polling()
    updater.idle()

@app.route('/')
def home():
    return "Бот працює!"

if __name__ == "__main__":
    t = threading.Thread(target=run_bot)
    t.start()
    app.run(host='0.0.0.0', port=8000)
