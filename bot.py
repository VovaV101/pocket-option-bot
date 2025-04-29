from flask import Flask
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CommandHandler, Updater, CallbackContext, MessageHandler, Filters
import yfinance as yf
import pandas as pd
import time

TOKEN = "7781796905:AAGbeuu5lcfWUAPgJzI6JAL5fQRyVHveowI"

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


def get_signal(ticker):
    try:
        data = yf.download(tickers=ticker, period="2d", interval="5m")
        if data.empty:
            return None

        close = data["Close"]
        ema50 = close.ewm(span=50).mean()
        ema200 = close.ewm(span=200).mean()
        rsi = compute_rsi(close)
        stochastic_signal = compute_stochastic(data)

        latest_close = close.iloc[-1]
        latest_ema50 = ema50.iloc[-1]
        latest_ema200 = ema200.iloc[-1]
        latest_rsi = rsi.iloc[-1]

        conditions_up = (
            latest_rsi < 30 and
            latest_close > latest_ema50 and
            stochastic_signal == "bullish"
        )

        conditions_down = (
            latest_rsi > 70 and
            latest_close < latest_ema50 and
            stochastic_signal == "bearish"
        )

        if conditions_up:
            return "UP", round(latest_rsi, 1)
        elif conditions_down:
            return "DOWN", round(latest_rsi, 1)
        else:
            return None
    except Exception as e:
        print(f"Error getting signal: {e}")
        return None


def compute_rsi(series, period=14):
    delta = series.diff()
    up = delta.clip(lower=0)
    down = -1 * delta.clip(upper=0)
    ema_up = up.ewm(com=period - 1, adjust=False).mean()
    ema_down = down.ewm(com=period - 1, adjust=False).mean()
    rs = ema_up / ema_down
    return 100 - (100 / (1 + rs))


def compute_stochastic(data, k_period=14, d_period=3):
    low_min = data["Low"].rolling(window=k_period).min()
    high_max = data["High"].rolling(window=k_period).max()
    stoch_k = 100 * (data["Close"] - low_min) / (high_max - low_min)
    stoch_d = stoch_k.rolling(window=d_period).mean()

    if stoch_k.iloc[-2] < stoch_d.iloc[-2] and stoch_k.iloc[-1] > stoch_d.iloc[-1]:
        return "bullish"
    elif stoch_k.iloc[-2] > stoch_d.iloc[-2] and stoch_k.iloc[-1] < stoch_d.iloc[-1]:
        return "bearish"
    else:
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
                    text=f"{pair_name} — ВХІД {direction} на 15 хв\n"
                         f"RSI: {rsi_value} | Підтвердження EMA | Stochastic OK\n"
                         f"Час: {time.strftime('%H:%M')}"
                )
                last_signal[pair] = direction


def start(update: Update, context: CallbackContext):
    update.message.reply_text("Привіт! Я твій бот для автоматичних сигналів. Вибери валютні пари командою /pairs")


def pairs(update: Update, context: CallbackContext):
    keyboard = [[pair] for pair in pairs_list.keys()]
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
        update.message.reply_text("Аналіз увімкнено! Сигнали почнуть надходити.")


def turn_off(update: Update, context: CallbackContext):
    global analyzing, job_reference
    if analyzing and job_reference:
        job_reference.schedule_removal()
        analyzing = False
        update.message.reply_text("Аналіз вимкнено.")
    else:
        update.message.reply_text("Аналіз вже вимкнений або ще не запускався.")


updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("pairs", pairs))
dispatcher.add_handler(CommandHandler("on", turn_on))
dispatcher.add_handler(CommandHandler("off", turn_off))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, pair_selected))

@app.route('/')
def home():
    return 'Бот активний!'

if __name__ == "__main__":
    updater.start_polling()
    app.run(host="0.0.0.0", port=8000)
