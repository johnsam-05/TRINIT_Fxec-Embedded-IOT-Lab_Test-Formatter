
# Cognigenius Bot

Cognigenius Bot is a Telegram bot developed to assist users in generating mock text questions based on input PDF files. This bot extracts text from uploaded PDF files and generates mock questions based on that text.

## Table of Contents
1. [Features](#features)
2. [Setup](#setup)
3. [Usage](#usage)
4. [Commands](#commands)
5. [Dependencies](#dependencies)
6. [Demo](#demo)

## Features<a name="features"></a>
- Extracts text from PDF files.
- Generates mock questions based on extracted text.
- Handles `/start` and `/help` commands.

## Setup<a name="setup"></a>
To set up the Cognigenius Bot, follow these steps:

1. Clone this repository:
    ```
    git clone <repository_url>
    cd <repository_directory>
    ```

2. Install dependencies:
    ```
    pip install -r requirements.txt
    ```

3. Obtain Telegram API token and Google API key:
    - **Telegram API Token**: You need to obtain a Telegram API token from [BotFather](https://core.telegram.org/bots#6-botfather).
    - **Google API Key**: You need to obtain a Google API key with access to the GenerativeAI service.

4. Configure API keys:
    - Replace `TELEGRAM_API_KEY` with your Telegram API token.
    - Replace `GENI_API_KEY` with your Google API key.

5. Run the bot:
    ```
    python bot.py
    ```

## Usage<a name="usage"></a>
Once the bot is up and running, you can interact with it through Telegram. Follow these steps to use the bot:

1. Start a conversation with the bot by sending a `/start` command.
2. Upload a PDF file containing questions that you want to generate mock questions from.
3. The bot will process the PDF file, extract text, and generate mock questions based on the extracted text.
4. Receive the generated mock questions from the bot.

## Commands<a name="commands"></a>
The following commands are available:

- `/start`: Start the bot and initiate a conversation.
- `/help`: Display a help message with available commands.

## Dependencies<a name="dependencies"></a>
- `telebot`: Python wrapper for the Telegram Bot API.
- `google.generativeai`: Python client library for Google GenerativeAI service.
- `requests`: Library for making HTTP requests.
- `PyPDF2`: Library for reading PDF files.
- `io`: Core Python module for handling I/O operations.
- `logging`: Python module for logging.

## Demo Video<a name="demo"></a>
[Video Recording Of Our Project](https://drive.google.com/file/d/1enX4p9vmQPf_5Q6qjGPE53bn_WHBs3rk/view?usp=sharing)
