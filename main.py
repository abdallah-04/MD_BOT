import time
import math
import random
import asyncio
from google.oauth2.service_account import Credentials
import gspread
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv,dotenv_values
import os
load_dotenv()
# Google Sheets API setup
scopes = [os.getenv("SCOPES")]
creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
client = gspread.authorize(creds)

sheet_id = os.getenv("SHEET_ID")
sheet = client.open_by_key(sheet_id).sheet1  


# Telegram Bot setup
token = os.getenv("TOKEN")
bot_username = os.getenv("BOT_USERNAME")

# List of MD members
md_members = ["abdullah_almuflah", "Batool1412","samaweshah","Janabaha2","sura"]


def get_last_row():
    return len(sheet.col_values(2))

# Function to send message via Telegram bot
async def send_message(update: Update, context: ContextTypes.DEFAULT_TYPE, name: str, phone: str,current_last_row :int):
    try:
        first_name = name.split()[0]
        message1 = f"يعطيك العافيه {first_name} انا من IEEE computer society وانت مسجل بفورم الانضمام لسا حاب تسجل معنا ؟"
        message2 = f"the WhatsApp link: https://wa.me/962{phone}"
        message3 = "@" + random.choice(md_members)
        message4 = current_last_row


        await update.message.reply_text(message1)
        await update.message.reply_text(message2)
        await update.message.reply_text(message3)
        await update.message.reply_text(message4)

    except Exception as e:
        print(f"Error sending message: {e}")

# Function to check for new entries and send messages
async def check_new_entries(update: Update, context: ContextTypes.DEFAULT_TYPE):
    last_processed_row = get_last_row()
    while True:
        try:
            current_last_row = get_last_row()
            if current_last_row > last_processed_row:
                name = sheet.acell(f"B{current_last_row}").value
                phone = sheet.acell(f"D{current_last_row}").value
                sheet.format(f"I{current_last_row}", {
    "backgroundColor": {
        "red": 1.0,    
        "green": 0.7,  
        "blue": 0.0    
    },
    "horizontalAlignment": "CENTER",
    "textFormat": {
        "foregroundColor": {
            "red": 1.0,    
            "green": 1.0,  
            "blue": 1.0    
        },
        "fontSize": 10,
        "bold": False
    }
})
                if name and phone:  
                    await send_message(update, context, name, phone,current_last_row )
                    last_processed_row = current_last_row
            await asyncio.sleep(60)  
        except Exception as e:
            print(f"Error checking new entries: {e}")
            await asyncio.sleep(60)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot started. Checking for new entries...")
    await update.message.re
    asyncio.create_task(check_new_entries(update, context))  


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("My job is to help the MD members.")



# Function to update the sheet when one of the MD member conivt  him 
async def update_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    if not context.args:
        await update.message.reply_text("🙄 شكلك ناسي شغلة! جرب: /update <number>")
        return

    try:
        row_number = int(context.args[0])  

       
        sheet.format(f"I{row_number}", {
            "backgroundColor": {"red": 0.0, "green": 0.7, "blue": 0.0},
            "horizontalAlignment": "CENTER",
            "textFormat": {
                "foregroundColor": {"red": 1.0, "green": 1.0, "blue": 1.0},
                "fontSize": 10,
                "bold": False
            }
        })

        
        responses = [
            f"✅ Boom! Row {row_number} is now updated",
        ]

        await update.message.reply_text(random.choice(responses))

    except ValueError:
        await update.message.reply_text("😅 Oops! That’s not a valid row number")


   
async def jop_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    spreadsheet = client.open_by_key(sheet_id)
    worksheet = spreadsheet.worksheet("jop_command")
    
    # Fetch data and filter valid numbers
    numbers_list = [num.strip() for num in worksheet.col_values(1) if num.strip().isdigit()]
    md_members2 = worksheet.col_values(4)
    md_members3 = worksheet.col_values(3)
    
    # Ensure members and metadata are aligned
    if len(md_members2) != len(md_members3):
        await update.message.reply_text("Mismatched member data!")
        return

    total_numbers = len(numbers_list)
    total_members = len(md_members2)
    
    num_per_member, remainder = divmod(total_numbers, total_members)
    
    updates = []
    count = 0
    count_row = 0
    
    for i in range(total_members):
        current_chunk = num_per_member + 1 if i < remainder else num_per_member
        member_numbers = numbers_list[count:count + current_chunk]
        count += current_chunk
        
        if not member_numbers:
            continue  # Skip members with no numbers
        
        message = f"Member: @{md_members2[i]}\n"
        for number in member_numbers:
            count_row += 1
            message += f"WhatsApp link: https://wa.me/962{number}\n"
            updates.append({'range': f'B{count_row}', 'values': [[md_members3[i]]]})
        
        # Send message in chunks if too long
        if len(message) > 4096:
            for chunk in [message[i:i+4096] for i in range(0, len(message), 4096)]:
                await update.message.reply_text(chunk)
        else:
            await update.message.reply_text(message)
    
    # Batch update Google Sheet
    if updates:
        worksheet.batch_update(updates)

# Function to mention all the number in the sheet 
async def mention_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    spreadsheet = client.open_by_key(sheet_id) 
    worksheet = spreadsheet.worksheet("mention_command")
    numbers_list = worksheet.col_values(1) 
    message_num = ""  
    for i in numbers_list:
        message_num += f"  @+962{i}"  
    if message_num.strip():  
        await update.message.reply_text(message_num)
    else:
        await update.message.reply_text("No data found")


# async def _command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     spreadsheet = client.open_by_key(sheet_id) 
#     worksheet = spreadsheet.worksheet("mention_command")
#     numbers_list = worksheet.col_values(1) 
#     message_num = ""  
#     for i in numbers_list:
#         message_num += f"  @{i}"  
#     if message_num.strip():  
#         await update.message.reply_text(message_num)
#     else:
#         await update.message.reply_text("No data found") 



async def handle_response(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str) -> None:
    spreadsheet = client.open_by_key(sheet_id) 
    worksheet = spreadsheet.worksheet("data fot the bot")
    processed: str = text.lower()

    if 'فورم الانضمام' in processed:
        await update.message.reply_text(worksheet.acell('B1').value)
    elif 'فورم الجدد' in processed:
        await update.message.reply_text(worksheet.acell('B2').value)
    elif 'ملف md' in processed:
        await update.message.reply_text(worksheet.acell('B3').value)
    elif 'تعريف عن البوت' in processed:
        await update.message.reply_text(worksheet.acell('B4').value)
    elif 'فيديوهات' in processed:
        await update.message.reply_text(worksheet.acell('B5').value)
    elif 'ما هو الcs' in processed:
        await update.message.reply_text(worksheet.acell('B6').value)
    elif 'فوائد العضوية' in processed:
        await update.message.reply_text(worksheet.acell('B7').value)
    elif 'الأوامر' in processed:
        await update.message.reply_text(worksheet.acell('B8').value)
    elif 'get CS certification' in processed:
        await update.message.reply_text(worksheet.acell('B9').value)
    elif 'IEEE membership information' in processed:
        await update.message.reply_text(worksheet.acell('B10').value)
    elif 'join CS for ieee member' in processed:
        await update.message.reply_text(worksheet.acell('B11').value)
    elif 'Renew' in processed:
        await update.message.reply_text(worksheet.acell('B12').value)
    elif 'تغير اسم الجامعة' in processed:
        await update.message.reply_text(worksheet.acell('B13').value)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == 'group':
        if bot_username in text:
            new_text: str = text.replace(bot_username, '').strip()
            await handle_response(update, context, new_text)
        else:
            return
    else:
        await handle_response(update, context, text)

    print('Bot: Response sent')



# Error handler
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

if __name__ == '__main__':
    print("Starting bot...")
    
    app = Application.builder().token(token).build()

    # Command handlers
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('update', update_command))
    app.add_handler(CommandHandler('mention', mention_command))
    app.add_handler(CommandHandler('jop', jop_command))

    # Message handler
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Error handler
    app.add_error_handler(error)

    print("Polling...")

    app.run_polling(poll_interval=3)  


