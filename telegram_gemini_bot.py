import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import google.generativeai as genai

# Read env variables
TELEGRAM_TOKEN = os.getenv("8489357662:AAEvlfAGxkna6RlyNr8vcLXMzNGoqx4w3ks")
GEMINI_API_KEY = os.getenv("AIzaSyCqqMW193V4xBHL2zp-hOfv_umOZRsAVEY")
GEMINI_MODEL = "gemini-1.5-flash"  # hardcoded to keep it super simple

if not TELEGRAM_TOKEN or not GEMINI_API_KEY:
    raise SystemExit("Set TELEGRAM_TOKEN and GEMINI_API_KEY in Replit Secrets")

genai.configure(api_key=GEMINI_API_KEY)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def call_gemini(prompt: str) -> str:
    resp = genai.generate_text(model=GEMINI_MODEL, prompt=prompt, temperature=0.2, max_output_tokens=400)
    return getattr(resp, "text", None) or str(resp)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi — I’m your Gemini bot! Send me a message.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    await update.message.chat.send_action("typing")
    reply = call_gemini(f"You are a helpful assistant.\nUser: {user_text}\nAssistant:")
    await update.message.reply_text(reply[:4000])  # keep under Telegram limit

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
