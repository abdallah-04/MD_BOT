from typing import Dict
import random
import asyncio
from google.oauth2.service_account import Credentials
import gspread
from gspread_formatting import get_effective_format
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
md_members = ["abdullah_almuflah", "Batool1412","samaweshah","Janabaha2","saja_alkhateeb97"]



def get_last_row():
    return len(sheet.col_values(2))

# Function to send message via Telegram bot
async def send_message(update: Update, context: ContextTypes.DEFAULT_TYPE, name: str, phone: str,current_last_row :int,message_name):
    try:
        first_name = name.split()[0]
        message1 = f"يعطيك العافيه {first_name} انا من IEEE computer society وانت مسجل بفورم الانضمام لسا حاب تسجل معنا ؟"
        message2 = f"the WhatsApp link: https://wa.me/962{phone}"
        message3 = "@" + message_name
        message4 = current_last_row


        await update.message.reply_text(message1)
        #await context.bot.send_message(message1)

        await update.message.reply_text(message2)
        #await context.bot.send_message(message2)

        await update.message.reply_text(message3)
        #await context.bot.send_message(message3)

        await update.message.reply_text(message4)
        # await context.bot.send_message(message4)


    except Exception as e:
        print(f"Error sending message: {e}")

# Function to check for new entries and send messages
async def check_new_entries(update: Update, context: ContextTypes.DEFAULT_TYPE):
    last_processed_row = get_last_row()
    while True:
        try:
            current_last_row = get_last_row()
            if current_last_row > last_processed_row:
                message_name =str(random.choice(md_members))
                name = sheet.acell(f"B{current_last_row}").value
                phone = sheet.acell(f"D{current_last_row}").value
                sheet.update(f"K{current_last_row}", [[message_name]])  
                sheet.update(f"L{current_last_row}", [["B"]])     
                sheet.format(f"K{current_last_row}", {
    "backgroundColor": {
        "red": 1.0,
        "green": 1.0,
        "blue": 1.0
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
                sheet.format(f"I{current_last_row}", {
    "backgroundColor": {
        "red": 1.0,
        "green": 1.0,
        "blue": 0.0
    },
    "horizontalAlignment": "CENTER",
    "textFormat": {
        "foregroundColor": {
            "red": 0.0,
            "green": 0.0,
            "blue": 0.0
        },
        "fontSize": 10,
        "bold": False
    }
})
                if name and phone:  
                    await send_message(update, context, name, phone, current_last_row, message_name)
                    last_processed_row = current_last_row
            await asyncio.sleep(60)  
        except Exception as e:
            print(f"Error checking new entries: {e}")
            await asyncio.sleep(60)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot started. Checking for new entries...")
    await update.message.reply_text("🤌")
    asyncio.create_task(check_new_entries(update, context))
    asyncio.create_task(check_for_delay_command(update, context))

    
# async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     chat_id = update.effective_chat.id
#     await context.bot.send_message(chat_id=chat_id, text="Bot started. Checking for new entries...")
#     await context.bot.send_message(chat_id=chat_id, text="🤌")
#     asyncio.create_task(check_new_entries(update, context))

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("My job is to help the MD members.")
    

async def check_for_delay_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await asyncio.sleep(2 * 24 * 60 * 60)  
    while True:
        try:
            response_status_name = sheet.col_values(11)
            response_status = sheet.col_values(12)
            pending_responses = {}

            for i in range(len(response_status)):
                if response_status[i] == "B":
                    MD_name = response_status_name[i]
                    pending_responses[MD_name] = i + 1

            for name, row_id in pending_responses.items():
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=f"احم احم 😶‍🌫\n@{name}\nCheck for ID {row_id}"
                )

            await asyncio.sleep(2 * 24 * 60 * 60)  

        except Exception as e:
            print(f"Error checking delay command: {e}")
            await asyncio.sleep(60)  


# Function to update the sheet when one of the MD member send the message 
async def update_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("🙄 شكلك ناسي شغلة! جرب:\n /update <number>")
        return

    try:
        row_number = int(context.args[0])

        sheet.update(f"L{row_number}", [["D"]])
        sheet.format(f"L{row_number}", {
            "backgroundColor": {"red": 1.0, "green": 1.0, "blue": 1.0},
            "horizontalAlignment": "CENTER",
            "textFormat": {
                "foregroundColor": {"red": 1.0, "green": 1.0, "blue": 1.0},
                "fontSize": 10,
                "bold": False
            }
        })
        sheet.format(f"I{row_number}", {
            "backgroundColor": {"red": 0.0, "green": 0.7, "blue": 0.0},
            "horizontalAlignment": "CENTER",
            "textFormat": {
                "foregroundColor": {"red": 0.0, "green": 0.0, "blue": 0.0},
                "fontSize": 10,
                "bold": False
            }
        })


        responses = [
            f"Magic happened! ID {row_number} is now green!",
            f"Poof! ID {row_number} just turned green!",
            f"Boomshakalaka! ID {row_number} is now fresh and fancy!",
            f"ID {row_number} is now fresh and green—mission complete!",
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

# async def handle_response(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str) -> None:
#     spreadsheet = client.open_by_key(sheet_id) 
#     worksheet = spreadsheet.worksheet("data fot the bot")
#     processed: str = text.lower()

#     # Fetch all the necessary values from the sheet at once
#     data_dict: Dict[str, str] = {
#         'فورم الانضمام': worksheet.acell('B1').value,
#         'فورم الجدد': worksheet.acell('B2').value,
#         'ملف md': worksheet.acell('B3').value,
#         'تعريف عن البوت': worksheet.acell('B4').value,
#         'فيديوهات': worksheet.acell('B5').value,
#         'ما هو الcs': worksheet.acell('B6').value,
#         'فوائد العضوية': worksheet.acell('B7').value,
#         'الأوامر': worksheet.acell('B8').value,
#         'get CS certification': worksheet.acell('B9').value,
#         'IEEE membership information': worksheet.acell('B10').value,
#         'join CS for ieee member': worksheet.acell('B11').value,
#         'Renew': worksheet.acell('B12').value,
#         'تغير اسم الجامعة': worksheet.acell('B13').value
#     }

#     # Iterate over the dictionary keys to check for matching text
#     for keyword, response in data_dict.items():
#         if keyword in processed:
#             await update.message.reply_text(response)
#             return  # Exit once the correct response is sent


# async def handle_response(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str) -> None:
#     spreadsheet = client.open_by_key(sheet_id)
#     worksheet = spreadsheet.worksheet("data fot the bot")

   
#     keywords = worksheet.col_values(1) 
#     responses = worksheet.col_values(2)  

   
#     for i, keyword in enumerate(keywords):
#         if keyword in text:
#             await update.message.reply_text(responses[i])
#             return  




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


