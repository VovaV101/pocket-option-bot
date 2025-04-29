from flask import Flask
import threading
import telegram
import time

TOKEN = "7713898071:AAG9Xe23F_pqR4dGKeWFtJw-_h6Ke62wrLk"
CHAT_ID = "7653693089"

bot = telegram.Bot(token=TOKEN)
app = Flask(__name__)

def send_loop():
    while True:
        try:
            bot.send_message(chat_id=CHAT_ID, text="Бот працює!")
            time.sleep(3600)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(10)

@app.route("/")
def home():
    return "Bot is running!"

if __name__ == "__main__":
    t = threading.Thread(target=send_loop)
    t.start()
    app.run(host="0.0.0.0", port=8000)
