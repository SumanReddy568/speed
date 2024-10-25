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
        # Initialize the Speedtest instance and get the closest server
        st = speedtest.Speedtest()
        st.get_best_server()

        # Conduct download and upload tests multiple times for accuracy
        download_speeds = [st.download() / 1e6 for _ in range(3)]  # Convert to Mbps
        upload_speeds = [st.upload() / 1e6 for _ in range(3)]      # Convert to Mbps

        # Average the results
        avg_download_speed = sum(download_speeds) / len(download_speeds)
        avg_upload_speed = sum(upload_speeds) / len(upload_speeds)
        ping = st.results.ping  # Ping in ms

        # Format and send the message with averaged speeds
        await update.message.reply_text(
            f"Download speed: {avg_download_speed:.2f} Mbps\n"
            f"Upload speed: {avg_upload_speed:.2f} Mbps\n"
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
