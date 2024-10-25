import os
import speedtest
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Command handler for the /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Hello! I can check your internet speed. Type /speedtest to begin."
    )

# Command handler for the /speedtest command
async def speedtest_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        st = speedtest.Speedtest()
        st.download()  # Initiate download test
        st.upload()    # Initiate upload test
        download_speed = st.results.download / 1e6  # Convert to Mbps
        upload_speed = st.results.upload / 1e6      # Convert to Mbps
        ping = st.results.ping                      # Ping in ms

        await update.message.reply_text(
            f"Download speed: {download_speed:.2f} Mbps\n"
            f"Upload speed: {upload_speed:.2f} Mbps\n"
            f"Ping: {ping} ms"
        )
    except Exception as e:
        await update.message.reply_text(f"Failed to perform speed test: {e}")

# Main function to start the bot
def main():
    # Get the Telegram bot token from environment variables
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        print("Error: Telegram Bot Token not provided.")
        return

    # Initialize the bot application
    app = ApplicationBuilder().token(token).build()

    # Handlers for commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("speedtest", speedtest_command))

    print("Bot is polling...")
    app.run_polling()

if __name__ == '__main__':
    main()
