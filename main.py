#import
import telebot
import google.generativeai as genai
#from IPython.display import Markdown
import requests
from io import BytesIO
from PyPDF2 import PdfReader

#api key
#TELEGRAM_API_KEY = userdata.get('botkey')
#GENI_API_KEY = userdata.get('gemini_api')

TELEGRAM_API_KEY = "6450948570:AAGpbsVKGQrFLxPP1u1v3wy28VqZTS52D3o"
GENI_API_KEY = "AIzaSyBJvevE8U-3ZJ-EIKGzkt1Zqr5nJhd6eJk"

#setup Bot & GenAI
bot = telebot.TeleBot(TELEGRAM_API_KEY)
genai.configure(api_key=GENI_API_KEY)
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])

#setup the model
generation_config = {
    "temperature": 0,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

model = genai.GenerativeModel(model_name="gemini-pro",
                               generation_config=generation_config,
                               safety_settings=safety_settings)

prompt_parts = [
    "Your name is Cognigenius Bot, a Telegram bot developed by @johnsam05 and @BenhurLee.\n",
    "You are here to assist us in generating mock text questions based on the input PDF file(but you will get that pdf as a text).\n",
    "Simply upload the PDF containing the questions, and I'll take care of the rest!"
]

response = chat.send_message(prompt_parts)

# Function to process PDF files
def process_pdf_and_generate_mock_test(file_id, chat_id):
    # Download the PDF file using Telegram's file_id
    bot.send_message(chat_id, "PDF Received.")
    file_info = bot.get_file(file_id)
    file_url = f"https://api.telegram.org/file/bot{bot.token}/{file_info.file_path}"
    response = requests.get(file_url)
    bot.send_message(chat_id, "Processing...")

    # Read PDF content
    with BytesIO(response.content) as pdf_buffer:
        pdf_reader = PdfReader(pdf_buffer)
        pdftext = ""
        for page in pdf_reader.pages:
            pdftext += page.extract_text()
    print(pdftext)
    bot.send_message(chat_id, "Generating Mock Questions...")
    bot.send_message(chat_id, chat.send_message(pdftext + "Process this text neatly and generate mock questions using this text. Also, make it as short as possible.").text)

# Function to handle "/start" command
def start(message):
    op = f"Hello {message.from_user.first_name}! I'm Cognigenius Bot 🤖\n"\
         f"This bot is developed by @johnsam05 & @BenhurLee\n"\
         "I'm here to assist you in generating mock text questions based on the input PDF file. Simply upload the PDF containing the questions, and I'll take care of the rest!\n"\
         "Feel free to ask any questions or use the available commands to get started.\n"\
         "Enjoy your time with @cognigeniusbot!"
    return op

# Function to handle other messages
def handle_message(message):
    # You may want to add error handling here
    pmt = chat.send_message(message.text)
    return pmt.text


#Telegram message handler
@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    msg_text = message.text.lower()

    if msg_text == "/start":
        op = start(message)
    else:
        op = handle_message(message)

    bot.send_message(message.chat.id, op)

#Telegram document handler
@bot.message_handler(content_types=['document'])
def handle_document(message):
    file_id = message.document.file_id
    chat_id = message.chat.id
    process_pdf_and_generate_mock_test(file_id, chat_id)

#Run the bot
print("Bot Started")
bot.infinity_polling()
