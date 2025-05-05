from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from src.config import pairs_list
from src.signals import start_analysis, stop_analysis

selected_pairs = set()
analyzing = False

def start(update: Update, context: CallbackContext):
    keyboard = [[InlineKeyboardButton(pair, callback_data=pair)] for pair in pairs_list.keys()]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Оберіть валютні пари для аналізу:', reply_markup=reply_markup)

def pairs(update: Update, context: CallbackContext):
    keyboard = [[InlineKeyboardButton(pair, callback_data=pair)] for pair in pairs_list.keys()]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Оберіть валютні пари для аналізу:', reply_markup=reply_markup)

def pair_selected(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    pair = query.data
    if pair in selected_pairs:
        query.edit_message_text(text=f"⚠️ Пара {pair} вже обрана.")
    else:
        selected_pairs.add(pair)
        query.edit_message_text(text=f"✅ Додано пару: {pair}")

def turn_on(update: Update, context: CallbackContext):
    global analyzing
    if not analyzing:
        update.message.reply_text('▶️ Аналіз увімкнено.')
        # Передаємо список вибраних пар
        context.bot_data["selected_pairs"] = [pairs_list[pair] for pair in selected_pairs]
        start_analysis(context)
        analyzing = True
    else:
        update.message.reply_text('Аналіз уже увімкнений.')

def turn_off(update: Update, context: CallbackContext):
    global analyzing
    if analyzing:
        update.message.reply_text('⏹️ Аналіз вимкнено.')
        stop_analysis()
        analyzing = False
    else:
        update.message.reply_text('Аналіз уже вимкнений.')
