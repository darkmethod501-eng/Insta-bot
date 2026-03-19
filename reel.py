import yt_dlp
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = "8717568709:AAFuTOrie0E7v4QXX1BqE8F0d_bUnIn9upc"
ADMIN_ID = 7437002319

users = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    users[user.id] = user.username

    await update.message.reply_text("👋 Reel link bhejo 🎬")

def get_video(url):
    ydl_opts = {
        'quiet': True,
        'format': 'best'
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return info['url']

async def download_reel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    users[user.id] = user.username

    url = update.message.text

    if "instagram.com" not in url:
        await update.message.reply_text("❌ Sirf Instagram link bhejo")
        return

    try:
        await update.message.reply_text("⏳ Download ho raha hai...")

        video_url = get_video(url)

        await update.message.reply_video(video=video_url)

    except Exception as e:
        await update.message.reply_text(f"⚠️ Error: {str(e)}")

async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == ADMIN_ID:
        await update.message.reply_text(
            "👑 Admin Panel:\n\n"
            "/users - total users\n"
            "/broadcast <msg>\n"
            "@adminhelp - full report"
        )

async def users_count(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == ADMIN_ID:
        await update.message.reply_text(f"👥 Users: {len(users)}")

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == ADMIN_ID:
        msg = " ".join(context.args)

        for uid in users:
            try:
                await context.bot.send_message(chat_id=uid, text=msg)
            except:
                pass

        await update.message.reply_text("✅ Broadcast done")

async def admin_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    if "@adminhelp" in update.message.text:
        data = "\n".join([f"{uid} (@{uname})" for uid, uname in users.items()])

        msg = f"👑 REPORT\n\n👥 {len(users)} Users\n\n{data}"

        if len(msg) > 4000:
            for i in range(0, len(msg), 4000):
                await update.message.reply_text(msg[i:i+4000])
        else:
            await update.message.reply_text(msg)

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("admin", admin))
app.add_handler(CommandHandler("users", users_count))
app.add_handler(CommandHandler("broadcast", broadcast))
app.add_handler(MessageHandler(filters.TEXT & filters.Regex(r'@adminhelp'), admin_help))
app.add_handler(MessageHandler(filters.TEXT, download_reel))

print("🤖 Bot chal raha hai...")
app.run_polling()
