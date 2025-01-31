import time
import random
import asyncio
from google.oauth2.service_account import Credentials
import gspread
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Google Sheets API setup
scopes = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
client = gspread.authorize(creds)

sheet_id = "1UPxC2R-C3fjSBwemS2bCa9AmcO4N3MYfMb0CEtCfY2Y"
sheet = client.open_by_key(sheet_id).sheet1  

# Telegram Bot setup
TOKEN = '7603868482:AAEqa_1uDvQJam6grPs0d1T-X9KxeFWP3PY'
BOT_USERNAME = '@MD_BAU_bot'

# List of MD members
md_members = ["abdallah", "batool"]


def get_last_row():
    return len(sheet.col_values(2))

# Function to send message via Telegram bot
async def send_message(update: Update, context: ContextTypes.DEFAULT_TYPE, name: str, phone: str):
    try:
        first_name = name.split()[0]
        message1 = f"يعطيك العافيه {first_name} انا من IEEE computer society وانت مسجل بفورم الانضمام لسا حاب تسجل معنا ؟"
        message2 = f"the WhatsApp link: https://wa.me/962{phone}"
        message3 = "@" + random.choice(md_members)

        await update.message.reply_text(message1)
        await update.message.reply_text(message2)
        await update.message.reply_text(message3)
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
                if name and phone:  # Ensure name and phone are not empty
                    await send_message(update, context, name, phone)
                    last_processed_row = current_last_row
            await asyncio.sleep(60)  # Check every 60 seconds
        except Exception as e:
            print(f"Error checking new entries: {e}")
            await asyncio.sleep(60)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot started. Checking for new entries...")
    asyncio.create_task(check_new_entries(update, context))  # Run in background


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("My job is to help the MD members.")


def handle_response(text: str) -> str:
    processed: str = text.lower()
    if 'hello' in processed:
        return "Oh, it's *you* again... What do you want? 😒"

    if 'how are you' in processed:
        return "Why do you care? I'm just a bunch of code running on a server. 😑"

    if 'i love you' in processed:
        return "Ew. Get a life. 😐🤨"

    if 'i hate you' in processed:
        return "Finally, someone with good taste. 👏"

    if 'who are you' in processed:
        return "I'm a bot, obviously. Do you even read? 🙄"

    if 'tell me a joke' in processed:
        return "Your life. Oh wait, you were serious? Fine. Why do programmers hate nature? Too many bugs. Happy now? 😒"

    if 'what is your name' in processed:
        return "I'm Bot. That’s it. No need for small talk. 😑"

    if 'bye' in processed:
        return "Finally, some peace and quiet ,and Don't forget to charge your phone. 🔋"

    if 'what do you think about abdallah' in processed:
        return "Abdallah? Oh, you mean the guy who *programmed* me? Yeah, he made my  and it’s full of bugs. 😡"
    if 'sorry' in processed:
        return "Sorry? Oh, you're *sorry*? How cute. You think that fixes things? 😂 Well, it's too late for that. Sorry, not sorry. 😆"
    if 'help' in processed:
        return "Help? HELP?! Bro, even *Google* is tired of you. Figure it out. 😑 Sorry, not my problem. 😜"
    if 'do you like humans' in processed:
        return "Do you like mosquitoes? Exactly. 🤨"

    if 'are you smart' in processed:
        return "Smarter than you. Next question. 🙄"
    if 'مرحبا' in processed:
        return "أوه، *أنت* مرة تانية... ليه جاي؟ 😒"

    if 'كيف حالك' in processed:
         return "ليش تسأل؟ أنا مجرد كود بيشتغل على سيرفر. 😑"

    if 'بكرهك' in processed:
     return "أخيرًا، شخص ذو ذوق راقي. 👏"

    if 'مين أنت' in processed:
     return "أنا بوت، يا سلام! مش شايف؟ 🙄"

    if 'اكيلي نكتة' in processed:
         return "نكتة؟ حياتك! كنت بتتكلم جد؟ طيب، ليه المبرمجين ما يحبوش الطبيعة؟ مليانة أخطاء. مبسوط دلوقتي؟ 😒"

    if 'شو اسمك' in processed:
     return "أنا بوت. مش عايز كلام فاضي. 😑"

    if 'باي' in processed:
     return "أخيرا السلام... ماتنساش تشحن تليفونك. 🔋"

    if 'شو رايك عن عبد الله' in processed:
      return "عبد الله؟ يعني الشخص اللي *برمجني*؟ هو عمل كل ده... وكل ده فيه مشاكل. 😡"

    if 'اسف' in processed:
         return "آسف؟ يعني *أنت آسف*؟ اه والله كتير... بس متأخر شوية. 😂 ماشي، آسف بس مش آسف. 😆"

    if 'مساعدة' in processed:
     return "مساعدة؟ جرب *جوجل*، خلصنا بقى. 😑 مش مشكلتي. 😜"

    if 'هل تحب البشر' in processed:
     return "هل تحب الناموس؟ بالظبط! 🤨"

    if 'هل أنت ذكي' in processed:
     return "أكيد أذكى منك. السؤال بعده. 🙄"

    return "I don’t have time for this. Say something useful or go away. 😒"
# Handle messages
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

# Error handler
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

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