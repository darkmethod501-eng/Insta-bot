import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp
TOKEN = "8717568709:AAHW7TlUz9MSYO4CdVtzBB2CV3oxxYz8Byk"
# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Send Instagram Reel link to download!")

# Reel download function
async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    ydl_opts = {
        'outtmpl': 'video.mp4',
        'quiet': True
    }

    try:
        await update.message.reply_text("⏳ Downloading...")

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        await update.message.reply_video(video=open('video.mp4', 'rb'))

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

# App setup
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download))

print("🤖 Bot is running...")
app.run_polling()
