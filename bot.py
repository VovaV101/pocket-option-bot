import telegram
import time

TOKEN = "7713898071:AAG9Xe23F_pqR4dGKeWFtJw-_h6Ke62wrLk"
CHAT_ID = "7653693089"

bot = telegram.Bot(token=TOKEN)

def send_message(text):
    bot.send_message(chat_id=CHAT_ID, text=text)

# Простий нескінченний цикл
while True:
    send_message("Бот працює!")
    time.sleep(3600)  # Надсилати повідомлення кожну годину
