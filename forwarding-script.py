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

# Constants
DISCORD_TOKEN = 'your_discord_token'  # Replace with your Discord token
TELEGRAM_TOKEN = 'your_telegram_token'  # Replace with your Telegram token
KIEV_TIMEZONE = pytz.timezone('Europe/Kiev')

# User-Agent and Cookies for HTTP requests
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

# Mapping of Discord threads to Telegram channels
FORUM_THREAD_MAPPING = {
    1060168170318606446: ('-1002082789826', 6693)  # Example: "Garry" thread on Discord
}

# Telegram bot setup
telegram_bot = TelegramBot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# Queue to store new messages from Discord threads
message_queue = []

# Get current time in Kiev
def get_current_time_in_kiev():
    return datetime.now(KIEV_TIMEZONE)

# Clean text before sending to Telegram
def clean_text(text):
    text = re.sub(r'<@&\d+>', '', text)  # Remove mentions or any unnecessary elements
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
    for discord_channel_id, (telegram_chat_id, thread_id) in FORUM_THREAD_MAPPING.items():
        messages = fetch_discord_messages(discord_channel_id)
        if messages:
            for message in messages:
                logging.info(f"New message from {message['author']['username']}: {message['content']}")
                message_queue.append((message, telegram_chat_id, thread_id))

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