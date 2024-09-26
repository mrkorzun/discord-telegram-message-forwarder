# Message Forwarding from Discord to Telegram

This Python script fetches messages from Discord threads and forwards them to Telegram chats using the Discord and Telegram APIs.

# Usage

The script will continuously monitor the specified Discord threads for new messages and forward them to the mapped Telegram chats at random intervals. It is designed to avoid Telegram’s flood control by spacing out messages and retrying failed deliveries.

## Project Structure

- forwarding-script.py: The main Python script that handles fetching, formatting, and forwarding messages.
- requirements.txt: List of Python libraries required for the project.

## Features

- Uses GET requests to retrieve messages from Discord.
- Forwards messages to specific Telegram chats.
- Cleans and formats the text before sending.
- Operates with intervals to avoid rate limiting.

## Troubleshooting

- 401 Unauthorized Error: Ensure that your Discord token and cookies are correctly set and haven’t expired.
- Flood control errors: If you see rate limit errors from Telegram, the script will automatically retry after the required delay.

## Requirements

- Python 3.x
- aiogram
- requests
- discord.py

## How to Run

1. Clone the repository.
2. Install the required libraries.
3. Add the tokens for Discord and Telegram.
4. Run the script using the command python3 script_name.py.

## License

This project is licensed under the MIT License.

---------------------------------------------------------------------

### Updates (more info in CHANGELOG.md):
- The script now tracks the last sent message and forwards only new messages using the `last_message_id` functionality.


---------------------------------------------------------------------


# Перенос сообщений из Discord в Telegram

Этот Python-скрипт получает сообщения из веток Discord и пересылает их в чаты Telegram, используя API Discord и Telegram.

## Возможности

- Использует GET-запросы для получения сообщений из Discord.
- Переносит сообщения в определённые чаты Telegram.
- Очищает и форматирует текст перед отправкой.
- Работает с интервалами для избежания блокировок.

## Требования

- Python 3.x
- aiogram
- requests
- discord.py

## Как запустить

1. Клонируйте репозиторий.
2. Установите необходимые библиотеки.
3. Добавьте токены для Discord и Telegram.
4. Запустите скрипт с помощью команды `python3 script_name.py`.

## Лицензия

Этот проект лицензирован на условиях MIT License.