import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp

TOKEN = os.getenv("8717568709:AAFuTOrie0E7v4QXX1BqE8F0d_bUnIn9upc")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send Instagram reel link 📥")

async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    ydl_opts = {
        'outtmpl': 'video.mp4'
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        await update.message.reply_video(video=open('video.mp4', 'rb'))

    except Exception as e:
        await update.message.reply_text("Error downloading reel ❌")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download))

app.run_polling()
