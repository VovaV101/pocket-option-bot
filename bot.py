from flask import Flask
from telegram.ext import CommandHandler, Dispatcher, Updater
import threading

TOKEN = "7713898071:AAG9Xe23F_pqR4dGKeWFtJw-_h6Ke62wrLk"
app = Flask(__name__)

def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=(
            "Привіт! Я твій особистий бот для трейдингу.\n\n"
            "📈 Даю точні сигнали для Pocket Option\n"
            "⏱️ Аналізую старші таймфрейми\n"
            "⚙️ Працюю на основі індикаторів та патернів\n"
            "✅ Працюю 24/7 — очікуй сигнали!"
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
    return "Бот запущений!"

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=8000)
