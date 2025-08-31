import os
import yt_dlp
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

TOKEN = os.getenv("BOT_TOKEN")

def start(update, context):
    update.message.reply_text("👋 Hello! Send me a YouTube link and I will download it for you.")

def download_video(update, context):
    url = update.message.text
    update.message.reply_text("📥 Downloading... Please wait.")

    try:
        ydl_opts = {
            'format': 'best',
            'outtmpl': 'video.mp4'
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        update.message.reply_video(open("video.mp4", "rb"))
        os.remove("video.mp4")
    except Exception as e:
        update.message.reply_text(f"❌ Error: {str(e)}")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, download_video))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()