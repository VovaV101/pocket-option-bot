from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext
from config import selected_pairs, pairs_list, analyzing
from signals import analyze

def start(update: Update, context: CallbackContext):
    """Стартова команда."""
    update.message.reply_text("Привіт! Я бот для торгових сигналів. Використай команду /pairs щоб обрати валютні пари.")

def pairs(update: Update, context: CallbackContext):
    """Відправка клавіатури для вибору пар."""
    keyboard = [[pair] for pair in pairs_list.keys()]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    update.message.reply_text("Вибери одну або кілька валютних пар:", reply_markup=reply_markup)

def pair_selected(update: Update, context: CallbackContext):
    """Обробка вибору пари або кількох пар."""
    global selected_pairs
    text = update.message.text

    if "," in text:
        selected = [pair.strip() for pair in text.split(",") if pair.strip() in pairs_list]
    else:
        selected = [text.strip()] if text.strip() in pairs_list else []

    if selected:
        selected_pairs.clear()
        for sel in selected:
            selected_pairs.append(pairs_list[sel])

        update.message.reply_text(f"Вибрані пари: {', '.join(selected)}")
    else:
        update.message.reply_text("Невірний вибір. Спробуй ще раз.")

def turn_on(update: Update, context: CallbackContext):
    """Увімкнення аналізу."""
    global analyzing

    if not analyzing:
        analyzing = True
        context.job_queue.run_repeating(run_analysis, interval=300, first=1, context=update.message.chat_id)
        update.message.reply_text("Аналіз увімкнено!")
    else:
        update.message.reply_text("Аналіз вже активний.")

def turn_off(update: Update, context: CallbackContext):
    """Вимкнення аналізу."""
    global analyzing

    if analyzing:
        analyzing = False
        context.job_queue.stop()
        update.message.reply_text("Аналіз вимкнено.")
    else:
        update.message.reply_text("Аналіз і так вимкнений.")

def run_analysis(context: CallbackContext):
    """Аналіз обраних пар і надсилання сигналів."""
    for pair in selected_pairs:
        signal = analyze(pair)
        if "Вхід" in signal:
            context.bot.send_message(chat_id=context.job.context, text=signal)
