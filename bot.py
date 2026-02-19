import os
import yt_dlp
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes

TOKEN = os.getenv("TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Send YouTube or Instagram Reel link.\nI will download it for you."
    )

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    if not any(x in url for x in ["youtube.com", "youtu.be", "instagram.com"]):
        await update.message.reply_text("❌ Send valid YouTube or Instagram link.")
        return

    await update.message.reply_text("⏳ Downloading...")

    ydl_opts = {
        "format": "mp4",
        "outtmpl": "video.%(ext)s",
        "quiet": True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        for file in os.listdir():
            if file.startswith("video"):
                with open(file, "rb") as f:
                    await update.message.reply_video(video=f)
                os.remove(file)
                break

    except Exception as e:
        await update.message.reply_text("⚠️ Download failed.")

if TOKEN:
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))
    print("Bot is running...")
    app.run_polling()
else:
    print("TOKEN not found. Please add it in Railway Variables.")
