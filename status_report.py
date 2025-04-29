from config import pairs_list, selected_pairs, analyzing, last_signal_time

def status(update, context):
    msg = "Статус бота:\n"
    msg += f"Обрані пари: {', '.join([k for k, v in pairs_list.items() if v in selected_pairs])}\n"
    msg += f"Аналіз: {'увімкнено' if analyzing else 'вимкнено'}\n"

    if last_signal_time:
        for pair in selected_pairs:
            name = [k for k, v in pairs_list.items() if v == pair][0]
            last_time = last_signal_time.get(pair, "немає")
            msg += f"Останній сигнал по {name}: {last_time}\n"
    else:
        msg += "Сигнали ще не надходили."

    update.message.reply_text(msg)
