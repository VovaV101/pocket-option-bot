from telegram.ext import ApplicationBuilder
from src.handlers import setup_handlers
from src.config import BOT_TOKEN

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # ВАЖЛИВО: ініціалізувати job_queue
    app.job_queue

    setup_handlers(app)

    print("Bot started and polling...")
    app.run_polling()

if __name__ == "__main__":
    main()
