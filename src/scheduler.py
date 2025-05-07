import asyncio
from src.signals import selected_pairs, analyze_pair
from telegram import Bot

task = None

async def check_signals(bot: Bot):
    while True:
        if selected_pairs:
            for pair in selected_pairs:
                signal = analyze_pair(pair)
                if signal:
                    await bot.send_message(
                        chat_id=bot.chat_id,
                        text=f"Сигнал для {pair}: {signal} на 15 хвилин"
                    )
                await asyncio.sleep(0.5)  # невелика пауза між повідомленнями
            await bot.send_message(
                chat_id=bot.chat_id,
                text="Бот активний: всі вибрані пари проаналізовано. Чекаємо наступну перевірку через 5 хвилин."
            )
        else:
            await bot.send_message(
                chat_id=bot.chat_id,
                text="Увага! Поки що немає обраних пар для моніторингу."
            )

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

def stop_scheduler():
    global task
    if task:
        task.cancel()
        task = None
