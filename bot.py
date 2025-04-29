from flask import Flask, request
from telegram import Update, Bot, ReplyKeyboardMarkup
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters, CallbackContext
import yfinance as yf
import pandas as pd
import time
import threading
import os

TOKEN = "7781796905:AAGbeuu5lcfWUAPgJzI6JAL5fQRyVHveowI"
bot = Bot(token=TOKEN)
app = Flask(__name__)

# Глобальні змінні
selected_pairs = ["EURUSD=X"]
analyzing = False
last_signal = {}
job_reference = None

pairs_list = {
    "EUR/USD": "EURUSD=X",
    "GBP/USD": "GBPUSD=X",
    "USD/JPY": "USDJPY=X",
    "AUD/USD": "AUDUSD=X",
    "USD/CAD": "USDCAD=X",
    "EUR/JPY": "EURJPY=X",
    "GBP/JPY": "GBPJPY=X",
    "EUR/GBP": "EURGBP=X",
    "NZD/USD": "NZDUSD=X",
    "USD/CHF": "USDCHF=X"
}

dispatcher = Dispatcher(bot=bot, update_queue=None, use_context=True)

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
        print("Error getting signal:", e)
        return None

def compute_rsi(series, period=14):
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -1 * delta.clip(upper=0)
    avg_gain = gain.ewm(com=period - 1, min_periods=period).mean()
    avg_loss = loss.ewm(com=period - 1, min_periods=period).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def compute_stochastic(data, k_period=14, d_period=3):
    low_min = data["Low"].rolling(window=k_period).min()
    high_max = data["High"].rolling(window=k_period).max()
    k = 100 * ((data["Close"] - low_min) / (high_max - low_min))
    d = k.rolling(window=d_period).mean()

    if k.iloc[-2] < d.iloc[-2] and k.iloc[-1] > d.iloc[-1]:
        return "bullish"
    elif k.iloc[-2] > d.iloc[-2] and k.iloc[-1] < d.iloc[-1]:
        return "bearish"
    return None

def analyze_job(context: CallbackContext):
    global last_signal
    for pair in selected_pairs:
        signal = get_signal(pair)
        if signal:
            direction, rsi_value = signal
            pair_name = [k for k, v in pairs_list.items() if v == pair][0]
            if last_signal.get(pair) != direction:
                context.bot.send_message(
                    chat_id=context.job.context,
                    text=f"{pair_name} — ВХІД {direction} на 15 хв\nRSI: {rsi_value} | EMA підтверджено | Stochastic OK\nЧас: {time.strftime('%H:%M')}"
                )
                last_signal[pair] = direction

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Привіт! Я твій бот для автоматичних сигналів. Вибери валютні пари командою /pairs")

def pairs(update: Update, context: CallbackContext):
    keyboard = [[pair] for pair in pairs_list]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    update.message.reply_text("Вибери валютні пари для аналізу:", reply_markup=markup)

def pair_selected(update: Update, context: CallbackContext):
    global selected_pairs
    text = update.message.text
    if text in pairs_list:
        selected_pairs = [pairs_list[text]]
        update.message.reply_text(f"Пара {text} вибрана для аналізу!")

def turn_on(update: Update, context: CallbackContext):
    global analyzing, job_reference
    if not analyzing:
        analyzing = True
        job_reference = context.job_queue.run_repeating(analyze_job, interval=300, first=1, context=update.message.chat_id)
        update.message.reply_text("Аналіз увімкнено!")

def turn_off(update: Update, context: CallbackContext):
    global analyzing, job_reference
    if analyzing and job_reference:
        job_reference.schedule_removal()
        analyzing = False
        update.message.reply_text("Аналіз вимкнено.")
    else:
        update.message.reply_text("Аналіз вже вимкнений.")

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("pairs", pairs))
dispatcher.add_handler(CommandHandler("on", turn_on))
dispatcher.add_handler(CommandHandler("off", turn_off))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, pair_selected))

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "OK", 200

@app.route("/")
def index():
    return "Бот активний!"

def set_webhook():
    url = f"https://{os.environ['RENDER_EXTERNAL_HOSTNAME']}/{TOKEN}"
    bot.set_webhook(url)

if __name__ == "__main__":
    set_webhook()
    app.run(host="0.0.0.0", port=8000)
