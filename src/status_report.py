from src.config import chat_id

async def send_signal(bot, pair, signal):
    text = f"✅ Новий сигнал для {pair}: {signal}"
    await bot.send_message(chat_id=chat_id, text=text)

async def send_status(bot):
    text = (
        "✅ Аналіз зараз активний.\n\n"
        "Обрані валютні пари:\n" +
        "\n".join([f"— {pair}" for pair in sorted(set(bot.selected_pairs))])
    )
    await bot.send_message(chat_id=chat_id, text=text)
