from telegram.ext import ApplicationBuilder
from src.handlers import setup_handlers
from src.config import BOT_TOKEN

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    setup_handlers(app)

    print("Bot started and polling...")
    app.run_polling()  # нічого міняти більше не треба

if __name__ == "__main__":
    main()
