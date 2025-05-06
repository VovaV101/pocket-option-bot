import asyncio
from telegram.ext import ApplicationBuilder
from src.handlers import setup_handlers
from src.config import BOT_TOKEN

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    setup_handlers(app)

    print("Bot started and polling...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
