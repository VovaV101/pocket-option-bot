def analyze_job(context: CallbackContext = None, chat_id: str = None):
    if context:
        # Аналіз через JobQueue
        bot_data = context.bot_data
        selected_pairs = bot_data.get("selected_pairs", [])
        last_signal = bot_data.setdefault("last_signal", {})
        last_signal_time = bot_data.setdefault("last_signal_time", {})
        actual_chat_id = chat_id or context.job.context or CHAT_ID
        bot = context.bot
    else:
        # Ручний аналіз через /analyze
        selected_pairs = list(pairs_list.values())
        last_signal = {}
        last_signal_time = {}
        actual_chat_id = chat_id or CHAT_ID
        bot = Bot(token=TELEGRAM_TOKEN)

    if not selected_pairs:
        print("Немає обраних валютних пар для аналізу.")
        return

    for pair in selected_pairs:
        signal = get_signal(pair)

        if signal:
            try:
                pair_name = next((k for k, v in pairs_list.items() if v == pair), pair)
            except StopIteration:
                pair_name = pair

            previous_signal = last_signal.get(pair)
            print(f"Перевірка {pair}: минулий сигнал = {previous_signal}, новий сигнал = {signal}")

            if previous_signal != signal:
                # Надсилаємо сигнал
                bot.send_message(
                    chat_id=actual_chat_id,
                    text=f"{pair_name} — Вхід {signal} на {TIMEFRAME_MINUTES * 3} хвилин!\n"
                         f"Час: {time.strftime('%H:%M:%S')}"
                )
                # Зберігаємо новий сигнал
                last_signal[pair] = signal
                last_signal_time[pair] = time.strftime('%H:%M:%S')
            else:
                print(f"Сигнал для {pair} не змінився ({signal}), повідомлення не надсилаємо.")
        else:
            print(f"Немає сигналу для {pair}")
