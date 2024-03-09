import logging
import telebot
import google.generativeai as genai
import requests
from io import BytesIO
from PyPDF2 import PdfReader

# Set up logging
logging.basicConfig(filename='bot.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set up Telebot and GenAI
TELEGRAM_API_KEY = "6450948570:AAGpbsVKGQrFLxPP1u1v3wy28VqZTS52D3o"
GENI_API_KEY = "AIzaSyBJvevE8U-3ZJ-EIKGzkt1Zqr5nJhd6eJk"

bot = telebot.TeleBot(TELEGRAM_API_KEY)
genai.configure(api_key=GENI_API_KEY)
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])

# Model configurations
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

# Initial prompt message
prompt_parts = [
    "Your name is Cognigenius Bot, a Telegram bot developed by @johnsam05 and @BenhurLee.\n",
    "You are here to assist us in generating mock text questions based on the input PDF file(but you will get that pdf as a text).\n",
    "Simply upload the PDF containing the questions, and I'll take care of the rest!,you need to use uppercase insterd of *"
]

response = chat.send_message(prompt_parts)

def processtxt(str):
    processedtxt = ""
    for x in str:
        if x not in ["*","`","```"]:
            processedtxt+=x
    return processedtxt

# Function to process PDF files
def process_pdf_and_generate_mock_test(file_id, chat_id):
    # Download the PDF file using Telegram's file_id
    bot.send_message(chat_id, "📥 PDF Received. Now processing...")
    file_info = bot.get_file(file_id)
    file_url = f"https://api.telegram.org/file/bot{bot.token}/{file_info.file_path}"
    response = requests.get(file_url)
        
        # Read PDF content
    with BytesIO(response.content) as pdf_buffer:
        pdf_reader = PdfReader(pdf_buffer)
        pdftext = ""
        for page in pdf_reader.pages:
            pdftext += page.extract_text()
        
    logging.info("PDF content extracted successfully.")
    bot.send_message(chat_id, "✅ PDF processed successfully. Generating Mock Questions...")
    bot.send_message(chat_id, processtxt(chat.send_message(pdftext + "Process this text neatly and generate mock questions using this text. Also, make it as short as possible and don't.").text))
    bot.send_message(chat_id, "🎉 Mock Questions generated successfully!")
    

# Function to handle "/start" command
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "👋")
    op = f"Hello {message.from_user.first_name}! I'm Cognigenius Bot 🤖\nThis bot was crafted by @johnsam05 & @BenhurLee to assist you in crafting mock text questions. \n📚 How it works:\nSimply upload a PDF containing your questions, and I'll handle the rest! I'll extract the text and generate mock questions based on it.\nFeel free to ask any questions or use the following commands to get started:\n🤔 Need help? Just type /help\nEnjoy your time with @cognigeniusbot!"
    bot.send_message(message.chat.id, op)


# Function to handle "/help" command
@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, "ℹ️ Here are the available commands:\n"
                                      "/start - Start the bot\n"
                                      "/help - Display this help message")
    

# Function to handle other messages
@bot.message_handler(func=lambda msg: True)
def handle_message(message):
    # You may want to add error handling here
    pmt = chat.send_message(message.text)
    bot.send_message(message.chat.id,processtxt(pmt.text))

# Telegram document handler
@bot.message_handler(content_types=['document'])
def handle_document(message):
    file_id = message.document.file_id
    chat_id = message.chat.id
    process_pdf_and_generate_mock_test(file_id, chat_id)

# Run the bot
print("Bot Started")
logging.info("Bot Started")
bot.infinity_polling()