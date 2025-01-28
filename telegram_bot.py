import time
import random
from google.oauth2.service_account import Credentials
import gspread
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Google Sheets API setup
scopes = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
client = gspread.authorize(creds)

sheet_id = "1UPxC2R-C3fjSBwemS2bCa9AmcO4N3MYfMb0CEtCfY2Y"
sheet = client.open_by_key(sheet_id).sheet1  # Open the first sheet

# Telegram Bot setup
TOKEN = '7932025838:AAGswbpqMbPnQnsYLlY8lR_i6ZOoVmydTN0'
BOT_USERNAME = '@MD_BAU_bot'

# List of MD members
md_members = ["abdallah", "batool"]

# Function to get the last row
def get_last_row():
    return len(sheet.col_values(2)) 

# Function to send message via Telegram bot
async def send_message(update: Update, context: ContextTypes.DEFAULT_TYPE, name: str, phone: str):
    message1 = f"يعطيك العافيه {name} انا من IEEE computer society وانت مسجل بفورم الانضمام لسا حاب تسجل معنا ؟"
    message2 = f"the WhatsApp link: https://wa.me/962{phone}"
    message3 = "@" + random.choice(md_members)
    
    await update.message.reply_text(message1)
    await update.message.reply_text(message2)
    await update.message.reply_text(message3)

# Function to check for new entries and send messages
async def check_new_entries(update: Update, context: ContextTypes.DEFAULT_TYPE):
    last_processed_row = get_last_row()
    while True:
        current_last_row = get_last_row()
        if current_last_row > last_processed_row:
            name = sheet.acell(f"B{current_last_row}").value
            phone = sheet.acell(f"D{current_last_row}").value
            await send_message(update, context, name, phone)
            last_processed_row = current_last_row
        time.sleep(60)  # Check every 60 seconds

# start command
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot started. Checking for new entries...")
    await check_new_entries(update, context)

# help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("My job is to help the MD members.")

# handle text responses
def handle_response(text: str) -> str:
    processed: str = text.lower()
    
    return "I don’t have time for this. Say something useful or go away. 😒"

# handle messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)

    print('Bot:', response)
    await update.message.reply_text(response)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'update {update} caused error {context.error}')

if __name__ == '__main__':
    print("Starting bot....")
    app = Application.builder().token(TOKEN).build()

    # Command handlers
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))

    # Message handler
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Error handler
    app.add_error_handler(error)

    print("Polling....")
    app.run_polling(poll_interval=3)