from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext
from src.config import pairs_list, selected_pairs, analyzing
from src.signals import start_analysis, stop_analysis

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "Привіт! Я твій бот для сигналів.\n"
        "Команди:\n"
        "/pairs — обрати валютні пари\n"
        "/on — увімкнути аналіз\n"
        "/off — вимкнути аналіз\n"
        "/status — переглянути статус"
    )

async def pairs(update: Update, context: CallbackContext):
    keyboard = [[pair] for pair in pairs_list.keys()]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("Оберіть валютні пари для аналізу:", reply_markup=markup)

async def pair_selected(update: Update, context: CallbackContext):
    text = update.message.text
    if text in pairs_list:
        symbol = pairs_list[text]
        if symbol not in selected_pairs:
            selected_pairs.append(symbol)
            await update.message.reply_text(f"Додано пару: {text}")
        else:
            await update.message.reply_text(f"Пара {text} вже обрана.")
    else:
        await update.message.reply_text("Будь ласка, оберіть валютну пару зі списку через /pairs.")

async def turn_on(update: Update, context: CallbackContext):
    global analyzing
    if not analyzing:
        await start_analysis(context.bot)
        analyzing = True
        await update.message.reply_text("Аналіз увімкнено!")
    else:
        await update.message.reply_text("Аналіз вже активний.")

async def turn_off(update: Update, context: CallbackContext):
    global analyzing
    if analyzing:
        await stop_analysis()
        analyzing = False
        await update.message.reply_text("Аналіз вимкнено!")
    else:
        await update.message.reply_text("Аналіз вже вимкнений.")
