# 📩 Message Forwarding from Discord to Telegram 🤖

This Python script automates the process of fetching messages from Discord threads and forwarding them to specified Telegram chats using the Discord and Telegram APIs. It is designed to ensure smooth operation by avoiding message flooding and handling errors gracefully.

## ✨ Key Features

- **Automatic Message Forwarding**: The script continuously monitors specific Discord threads for new messages and forwards them to the mapped Telegram chats.
- **Flood Control Handling**: Implements random intervals to avoid Telegram's rate-limiting mechanisms.
- **Message Formatting**: Cleans and formats Discord messages before forwarding them to ensure proper readability in Telegram.
- **Error Handling & Retrying**: Automatically retries failed message deliveries due to rate limits or other API-related errors.

## 🔧 Technologies and Libraries Used

- **[aiogram](https://docs.aiogram.dev/en/latest/)**: A Python framework for Telegram Bot API.
- **[discord.py](https://discordpy.readthedocs.io/en/stable/)**: A Python wrapper for Discord’s API.
- **[requests](https://requests.readthedocs.io/en/latest/)**: Used for making HTTP requests to Discord for fetching messages.
- **Logging**: Provides detailed logs of message fetching, forwarding, and error handling.

## 📦 Installation

### Prerequisites:
- Python 3.6+
- Discord Token (with appropriate permissions).
- Telegram Bot Token.

### Steps:
1. **Clone the repository**:
    ```bash
    git clone https://github.com/mrkorzun/message-forwarding.git
    cd message-forwarding
    ```

2. **Create and activate a virtual environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use: venv\Scripts\activate
    ```

3. **Install the required Python packages**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Add your Discord and Telegram tokens**:
    - Open the `config.py` file (or set environment variables) and insert your Discord token and Telegram bot token.
    - Specify the mappings for Discord threads and corresponding Telegram chats in the script.

## 🚀 Usage

1. **Run the Script**:
    ```bash
    python forwarding-script.py
    ```

2. **How It Works**:
   - The script checks for new messages in the specified Discord threads.
   - It forwards the messages to the corresponding Telegram channels while adhering to Telegram’s rate limits.
   - Only new messages are forwarded using the `last_message_id` feature to track the last sent message.

## 💡 Example Setup

1. **Discord Thread to Telegram Mapping**: In the script, you can map a specific Discord thread to a Telegram chat using:
    ```python
    FORUM_THREAD_MAPPING = {
        'discord_thread_id': ('telegram_chat_id', 'thread_message_id')
    }
    ```
    This will ensure that messages from the mapped Discord thread are forwarded to the specified Telegram chat.

2. **Log Example**:
    ```
    INFO: New message from Discord: "Hello, how are you?"
    INFO: Forwarding to Telegram chat: -100123456789
    INFO: Message successfully sent to Telegram.
    ```

## 📚 Future Enhancements

- **Media Forwarding**: Add support for forwarding media files (images, videos) from Discord to Telegram.
- **Multiple Discord Servers**: Expand the script to handle message forwarding across multiple Discord servers.
- **Improved Flood Control**: Implement more advanced rate-limiting strategies for handling higher volumes of messages.

## 🤔 Troubleshooting

1. **401 Unauthorized Error**: 
    - Ensure that your Discord token is correct and valid.
    - Verify that the bot has sufficient permissions to read messages in the threads.

2. **Flood Control Issues**:
    - Telegram may reject messages if the bot sends too many within a short time. The script automatically handles this by retrying after a delay. Ensure that the retry mechanism is functioning by checking the logs.

3. **Token Expiry**: 
    - If your tokens expire, you will need to refresh them and update the script accordingly.

## 🛠 Project Structure

- **`forwarding-script.py`**: The main Python script that handles fetching, formatting, and forwarding messages.
- **`config.py`**: A configuration file to store your API tokens and mapping information.
- **`requirements.txt`**: A list of the required Python libraries for the project.

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

### Example Badges:
![Python](https://img.shields.io/badge/python-3.12%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## 📝 Contact

Created by [mrkorzun](https://github.com/mrkorzun). Feel free to reach out if you have any questions or suggestions for improvement!
