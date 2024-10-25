# Use a lightweight Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy project files to the container
COPY . /app

# Install the dependencies
RUN pip install -r requirements.txt

# Define environment variable for Telegram bot token
ENV TELEGRAM_BOT_TOKEN=7174836071:AAHlXf65S2Ot-klse-LZflvVn_WCqgbLwOI

# Start the bot
CMD ["python", "bot.py"]
