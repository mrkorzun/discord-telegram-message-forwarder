import logging
import asyncio
import requests
from discord.ext import tasks
from aiogram import Bot as TelegramBot, Dispatcher
from aiogram.enums import ParseMode
from datetime import datetime
import pytz
import random
import re
import html

# Logging settings
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Constants (replace with your own tokens)
DISCORD_TOKEN = 'your_discord_token'  # Replace with your Discord token
TELEGRAM_TOKEN = 'your_telegram_token'  # Replace with your Telegram token
KIEV_TIMEZONE = pytz.timezone('Europe/Kiev')

# User-Agent and Cookies for HTTP requests (replace with your own values)
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Mobile Safari/537.36',
    'Authorization': DISCORD_TOKEN
}

COOKIES = {
    "__dcfduid": "your_dcfduid",  # Replace with your cookies
    "__sdcfduid": "your_sdcfduid",
    "OptanonConsent": "your_optanon_consent",
    "cf_clearance": "your_cf_clearance",
    "__cfruid": "your_cfruid",
    "_cfuvid": "your_cfuvid"
}

# Set the initial last_message_id manually (use the last known message ID here)
last_message_id = 'your_last_message_id'  # Set the last message ID from which you want to start

# Mapping of Discord threads to Telegram channels (replace with your IDs)
FORUM_THREAD_MAPPING = {
    'your_Discord,message_id': ('your_telegram_channel_id', 'telegram_id-thred')  # Example mapping: Discord thread -> Telegram channel
}

# Telegram bot setup
telegram_bot = TelegramBot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# Queue to store new messages from Discord threads
message_queue = []

# Clean text before sending to Telegram
def clean_text(text):
    # Remove mentions or any unnecessary elements
    text = re.sub(r'<@&\d+>', '', text)
    return html.escape(text)

# Send a message to Telegram
async def send_to_telegram(message, chat_id, reply_to_message_id=None):
    try:
        await telegram_bot.send_message(chat_id, message, parse_mode=ParseMode.HTML, reply_to_message_id=reply_to_message_id)
        logging.info(f"Message sent to Telegram chat_id: {chat_id}")
    except Exception as e:
        logging.error(f"Failed to send message to Telegram: {e}")

# Generate a random interval in minutes
def random_interval(min_minutes, max_minutes):
    return random.randint(min_minutes, max_minutes)

# Fetch messages from Discord via HTTP GET requests
def fetch_discord_messages(channel_id):
    url = f'https://discord.com/api/v9/channels/{channel_id}/messages'
    response = requests.get(url, headers=HEADERS, cookies=COOKIES)

    if response.status_code == 200:
        return response.json()
    else:
        logging.error(f"Error fetching messages from Discord: {response.status_code}, {response.text}")
        return []

# Timer to check for new messages in Discord threads
@tasks.loop(minutes=random_interval(1, 2))  # Loop to run frequently with a random interval
async def frequent_task():
    logging.info("Running frequent_task")
    global message_queue
    while message_queue:
        message, chat_id, reply_to_message_id = message_queue.pop(0)
        user_message = f"<b>{clean_text(message['author']['username'])}</b>: \n{clean_text(message['content'])}"
        await send_to_telegram(user_message, chat_id, reply_to_message_id)

# Check for new messages from Discord and add them to the queue
async def check_new_messages():
    global last_message_id  # To keep track of the last processed message ID
    for discord_channel_id, (telegram_chat_id, thread_id) in FORUM_THREAD_MAPPING.items():
        messages = fetch_discord_messages(discord_channel_id)
        if messages:
            for message in reversed(messages):  # Process messages from oldest to newest
                if int(message['id']) > int(last_message_id):  # Only process messages newer than the last_message_id
                    logging.info(f"New message from {message['author']['username']}: {message['content']}")
                    message_queue.append((message, telegram_chat_id, thread_id))
                    last_message_id = message['id']  # Update last_message_id to the latest processed message

# Main loop to keep checking for new messages
async def run():
    frequent_task.start()
    while True:
        await check_new_messages()
        await asyncio.sleep(120)  # Check every 2 minutes

# Starting main code
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())