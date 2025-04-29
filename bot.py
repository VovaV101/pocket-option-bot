import telegram
import time

TOKEN = "ТВОЙ_ТОКЕН_ТУТ"
CHAT_ID = "ТВОЙ_CHAT_ID"

bot = telegram.Bot(token=TOKEN)

def send_message(text):
    bot.send_message(chat_id=CHAT_ID, text=text)

# Простий нескінченний цикл
while True:
    send_message("Бот працює!")
    time.sleep(3600)  # Надсилати повідомлення кожну годину
