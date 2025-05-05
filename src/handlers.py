# src/handlers.py

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from src.config import pairs_list
from src.signals import start_analysis, stop_analysis, selected_pairs

analyzing = False

def start(update: Update, context: CallbackContext):
    """Команда /start — привітання та пропозиція обрати пари."""
    keyboard = [[InlineKeyboardButton(pair, callback_data=pair)] for pair in pairs_list.keys()]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Привіт! Оберіть валютні пари для аналізу:', reply_markup=reply_markup)

def pairs(update: Update, context: CallbackContext):
    """Команда /pairs — ще раз обрати валютні пари."""
    keyboard = [[InlineKeyboardButton(pair, callback_data=pair)] for pair in pairs_list.keys()]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Оберіть валютні пари для аналізу:', reply_markup=reply_markup)

def pair_selected(update: Update, context: CallbackContext):
    """Обробка вибору валютної пари."""
    query = update.callback_query
    query.answer()
    pair = query.data
    if pair in selected_pairs:
        query.edit_message_text(text=f"⚠️ Пара {pair} вже обрана.")
    else:
        selected_pairs.add(pair)
        query.edit_message_text(text=f"✅ Додано пару: {pair}")

def turn_on(update: Update, context: CallbackContext):
    """Команда /on — запуск аналізу."""
    global analyzing
    if not analyzing:
        start_analysis(context)
        analyzing = True
        update.message.reply_text('▶️ Аналіз увімкнено. Чекаємо сигнали...')
    else:
        update.message.reply_text('Аналіз уже увімкнений.')

def turn_off(update: Update, context: CallbackContext):
    """Команда /off — зупинка аналізу."""
    global analyzing
    if analyzing:
        stop_analysis(context)
        analyzing = False
        update.message.reply_text('⏹️ Аналіз вимкнено.')
    else:
        update.message.reply_text('Аналіз уже вимкнений.')
