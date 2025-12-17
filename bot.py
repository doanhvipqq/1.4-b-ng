import logging
import os
import threading
from flask import Flask
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# --- CẤU HÌNH ---
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# --- PHẦN 1: TẠO WEB ẢO (ĐỂ RENDER KHÔNG TẮT BOT) ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_web_server():
    # Lấy cổng từ Render, nếu không có thì mặc định 8080
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# --- PHẦN 2: CODE BOT GEMINI ---
if not TELEGRAM_TOKEN or not GEMINI_API_KEY:
    raise ValueError("Thiếu biến môi trường!")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot đã sống lại và bất tử trên Render!")

async def chat_gemini(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    try:
        response = model.generate_content(user_text)
        bot_reply = response.text
        if len(bot_reply) > 4000:
            for x in range(0, len(bot_reply), 4000):
                await update.message.reply_text(bot_reply[x:x+4000])
        else:
            await update.message.reply_text(bot_reply)
    except Exception as e:
        await update.message.reply_text(f"Lỗi: {e}")

# --- PHẦN 3: CHẠY SONG SONG CẢ 2 ---
if __name__ == '__main__':
    # Chạy web server trong 1 luồng riêng
    t = threading.Thread(target=run_web_server)
    t.start()
    
    # Chạy bot Telegram
    print("Bot starting...")
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), chat_gemini))
    application.run_polling()
