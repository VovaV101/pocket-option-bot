from telegram import Update
from telegram.ext import ContextTypes

from src.config import pairs_list, selected_pairs, analyzing, job_reference

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[pair] for pair in pairs_list]
    reply_markup = {"keyboard": keyboard, "resize_keyboard": True}
    await update.message.reply_text(
        "Оберіть валютні пари для аналізу:", reply_markup=reply_markup
    )

async def pairs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text in selected_pairs:
        await update.message.reply_text(f"⚠️ Пара {text} вже обрана.")
    elif text in pairs_list:
        selected_pairs.append(text)
        await update.message.reply_text(f"✅ Додано пару: {text}")

async def pair_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    selected_text = "\n".join(f"— {pair}" for pair in selected_pairs) if selected_pairs else "Немає обраних пар."
    await update.message.reply_text(f"Обрані пари:\n{selected_text}")

async def turn_on(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not analyzing.is_set():
        analyzing.set()
        await update.message.reply_text("✅ Аналіз увімкнено.")
    else:
        await update.message.reply_text("Аналіз вже увімкнено.")

async def turn_off(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if analyzing.is_set():
        analyzing.clear()
        if job_reference:
            job_reference.schedule_removal()
        await update.message.reply_text("⛔️ Аналіз вимкнено.")
    else:
        await update.message.reply_text("Аналіз вже вимкнено.")
