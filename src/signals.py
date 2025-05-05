import threading
import time
import yfinance as yf
from src.status_report import send_signal
from src.config import pairs_list, TIMEFRAME_MINUTES
from src.handlers import selected_pairs

analyzing = False
analysis_thread = None

def analyze_market():
    while analyzing:
        for pair in selected_pairs:
            ticker = pairs_list[pair]
            data = yf.download(tickers=ticker, period="2d", interval=f"{TIMEFRAME_MINUTES}m")
            if not data.empty:
                last_candle = data.iloc[-1]
                if last_candle['Close'] > last_candle['Open']:
                    signal = f"✅ Вгору ({pair})"
                elif last_candle['Close'] < last_candle['Open']:
                    signal = f"⬇️ Вниз ({pair})"
                else:
                    signal = f"⏸️ Немає руху ({pair})"
                send_signal(signal)
        time.sleep(TIMEFRAME_MINUTES * 60)

def start_analysis():
    global analyzing, analysis_thread
    if not analyzing:
        analyzing = True
        analysis_thread = threading.Thread(target=analyze_market)
        analysis_thread.start()

def stop_analysis():
    global analyzing
    if analyzing:
        analyzing = False
