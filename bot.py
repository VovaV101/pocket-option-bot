import os
import time
import pandas as pd
import yfinance as yf
from flask import Flask, request
from telegram import Bot, Update, ReplyKeyboardMarkup
from telegram.ext import (
    Dispatcher, CommandHandler, MessageHandler, Filters, CallbackContext, JobQueue
)
from config import selected_pairs, analyzing, last_signal, last_signal_time, pairs_list
from status_report import status

# Отримуємо змінні середовища з Render
TOKEN = os.environ["TELEGRAM_TOKEN"]
WEBHOOK_URL = os.environ["WEBHOOK_URL"]

# Ініціалізація Flask
app = Flask(__name__)
bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot, None, workers=4, use_context=True)
job_queue = JobQueue()
job_queue.set_dispatcher(dispatcher)
job_queue.start()

# === Індикатори ===
def compute_rsi(series, period=14):
    delta = series.diff()
    up = delta.clip(lower=0)
    down = -1 * delta.clip(upper=0)
    ema_up = up.ewm(span=period, adjust=False).mean()
    ema_down = down.ewm(span=period, adjust=False).mean()
    rs = ema_up / ema_down
    return 100 - (100 / (1 + rs))

def compute_stochastic(data, k_period=14, d_period=3):
    low_min = data["Low"].rolling(window=k_period).min()
    high_max = data["High"].rolling(window=k_period).max()
    stoch_k = 100 * ((data["Close"] - low_min) / (high_max - low_min))
    stoch_d = stoch_k.rolling(window=d_period).mean()
    if stoch_k.iloc[-2] < stoch_d.iloc[-2] and stoch_k.iloc[-1] > stoch_d.iloc[-1]:
        return "bullish"
    elif stoch_k.iloc[-2] > stoch_d.iloc[-2] and stoch_k.iloc[-1] < stoch_d.iloc[-1]:
        return "bearish"
    return None

def get_signal(ticker):
    try:
        data = yf.download(tickers=ticker, period="2d", interval="5m")
        if data.empty:
            return None
        close = data["Close"]
        ema50 = close.ewm(span=50).mean()
        rsi = compute_rsi(close)
        stochastic = compute_stochastic(data)
        latest_close = close.iloc[-1]
        latest_ema50 = ema50.iloc[-1]
        latest_rsi = rsi.iloc[-1]

        if latest_rsi < 30 and latest_close > latest_ema50 and stochastic == "bullish":
            return "UP", round(latest_rsi, 1)
        elif latest_rsi > 70 and latest_close < latest_ema50 and stochastic == "bearish":
            return "DOWN", round(latest_rsi, 1)
        return None
    except Exception as e:
        print(f"Error in get_signal: {e}")
        return None

def analyze_job(context: CallbackContext):
    global last_signal
    for pair in selected_pairs:
        signal = get_signal(pair)
        if signal:
            direction, rsi_value = signal
            pair_name = [k for k, v in pairs_list.items() if v == pair][0]
            if last_signal.get(pair) != direction:
                bot.send_message(
                    chat_id=context.job.context,
                    text=f"{pair_name} ВХІД {direction} на 15 хв\n"
                         f"RSI: {rsi_value} | EMA підтверджено | Stochastic OK\n"
                         f"Час: {time.strftime('%H:%M:%S')}"
                )
                last_signal[pair] = direction
                last_signal_time[pair] = time.strftime('%H:%M:%S')

# === Команди ===
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Привіт! Я твій бот для сигналів. Використай /pairs щоб вибрати валюту.")

def pairs(update: Update, context: CallbackContext):
    available_pairs = ", ".join(pairs_list.keys())
    update.message.reply_text(
        f"Вибери валютні пари для аналізу, розділивши через кому (,):\n\n{available_pairs}"
    )

def pair_selected(update: Update, context: CallbackContext):
    global selected_pairs
    text = update.message.text
    selected = []

    for item in text.split(","):
        pair = item.strip().upper()
        if pair in pairs_list:
            selected.append(pairs_list[pair])

    if selected:
        selected_pairs = selected
        update.message.reply_text(f"Вибрані пари для аналізу: {', '.join([k for k, v in pairs_list.items() if v in selected_pairs])}")
    else:
        update.message.reply_text("Невірний вибір. Спробуйте ще раз за допомогою команди /pairs.")

def turn_on(update: Update, context: CallbackContext):
    global analyzing, job_reference
    if not analyzing:
        analyzing = True
        job_reference = job_queue.run_repeating(analyze_job, interval=300, first=1, context=update.message.chat_id)
        update.message.reply_text("Аналіз увімкнено!")
    else:
        update.message.reply_text("Аналіз уже працює.")

def turn_off(update: Update, context: CallbackContext):
    global analyzing, job_reference
    if analyzing and job_reference:
        job_reference.schedule_removal()
        analyzing = False
        update.message.reply_text("Аналіз вимкнено.")
    else:
        update.message.reply_text("Аналіз вже не активний.")

# === Реєстрація команд ===
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("pairs", pairs))
dispatcher.add_handler(CommandHandler("on", turn_on))
dispatcher.add_handler(CommandHandler("off", turn_off))
dispatcher.add_handler(CommandHandler("status", status))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, pair_selected))

# === Webhook для Telegram ===
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok", 200

@app.route("/")
def index():
    return "Бот активний!"

if __name__ == "__main__":
    bot.delete_webhook()
    bot.set_webhook(url=f"{WEBHOOK_URL}/{TOKEN}")
    app.run(host="0.0.0.0", port=8000)
