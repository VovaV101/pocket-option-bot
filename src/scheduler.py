import asyncio
from src.signals import selected_pairs, analyze_pair
from telegram import Bot

task = None

async def check_signals(bot: Bot):
    while True:
        for pair in selected_pairs:
            signal = analyze_pair(pair)
            if signal:
                await bot.send_message(chat_id=bot.chat_id, text=signal)
                await asyncio.sleep(0.5)  # невелика пауза між повідомленнями, щоб не банив Telegram

        # Після перевірки всіх пар
        await bot.send_message(chat_id=bot.chat_id, text="Бот активний: всі вибрані пари проаналізовано.")
        await asyncio.sleep(300)  # чекати 5 хвилин

def start_scheduler(app):
    global task
    if not task:
        # Зберігаємо chat_id користувача в Bot
        for update in app.update_queue.queue:
            if update.message:
                app.bot.chat_id = update.message.chat_id
                break
        task = asyncio.create_task(check_signals(app.bot))

def stop_scheduler(app):
    global task
    if task:
        task.cancel()
        task = None
