import logging
import os
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# --- CẤU HÌNH LẤY TỪ MÔI TRƯỜNG RENDER ---
# Không dán trực tiếp key vào đây nữa nhé!
TELEGRAM_TOKEN = os.environ.get("8229062858:AAGeAmWU_hJHYSBdNeIzgreXh29MLt-ijXg")
GEMINI_API_KEY = os.environ.get("AIzaSyBIRUKodeBYsunFNx5qIoZHh5ZkAhCkAR8")

# Kiểm tra xem đã nạp Key chưa
if not TELEGRAM_TOKEN or not GEMINI_API_KEY:
    raise ValueError("Chưa cài đặt TELEGRAM_TOKEN hoặc GEMINI_API_KEY trong Environment Variables!")

# Cấu hình Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot đã online trên Render! Sẵn sàng phục vụ.")

async def chat_gemini(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    # await context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing') # Tạm tắt để tối ưu tốc độ

    try:
        response = model.generate_content(user_text)
        bot_reply = response.text
        
        # Cắt tin nhắn nếu quá dài (Telegram giới hạn 4096 ký tự)
        if len(bot_reply) > 4000:
            for x in range(0, len(bot_reply), 4000):
                await update.message.reply_text(bot_reply[x:x+4000])
        else:
            await update.message.reply_text(bot_reply)
            
    except Exception as e:
        await update.message.reply_text(f"Lỗi: {e}")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    start_handler = CommandHandler('start', start)
    msg_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), chat_gemini)
    
    application.add_handler(start_handler)
    application.add_handler(msg_handler)
    
    print("Bot is running...")
    application.run_polling()
