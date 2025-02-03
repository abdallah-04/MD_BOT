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

sheet_id = "1dd2LSqZ9sJ7EAmCyvdAqDrwTksB8v8SSRZaKPlk58AE"
sheet = client.open_by_key(sheet_id).sheet1  

# Telegram Bot setup
TOKEN = '7603868482:AAEqa_1uDvQJam6grPs0d1T-X9KxeFWP3PY'
BOT_USERNAME = '@MD_BAU_bot'

# List of MD members
md_members = ["abdullah_almuflah", "Batool1412","ismael","sama","Menna","sora"]


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
                sheet.format(f"B{current_last_row}", {
    "backgroundColor": {
        "red": 0.0,
        "green": 0.7,  # Green color
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
                if name and phone:  # Ensure name and phone are not empty
                    await send_message(update, context, name, phone)
                    last_processed_row = current_last_row
            await asyncio.sleep(60)  # Check every 60 seconds
        except Exception as e:
            print(f"Error checking new entries: {e}")
            await asyncio.sleep(60)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot started. Checking for new entries...")
    await update.message.reply_text("🤌")
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
    
    if 'test' in processed:
        return "🐼"

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
         return "نكتة؟ حياتك! كنت بتتكلم جد؟ طيب، ليه المبرمجين ما يحبوش الطبيعة؟ مليانة bugs. مبسوط دلوقتي؟ 😒"

    if 'شو اسمك' in processed:
     return "أنا بوت. مش عايز كلام فاضي. 😑"

    if 'باي' in processed:
     return "أخييييرا ... ماتنساش تشحن تليفونك. 🔋"

    if 'مين عبدالله' in processed:
      return "عبد الله؟ يعني الشخص اللي *برمجني*؟ هو عمل كل ده... وكل ده فيه مشاكل. 😡"

    if 'اسف' in processed:
         return "آسف؟ يعني *أنت آسف*؟ اه والله كتير... بس متأخر شوية مش مسامحك"

    if 'مساعدة' in processed:
     return " شفال عندك انا🤨مش مشكلتي"

    if 'هل تحب البشر' in processed:
     return "هل تحب الناموس؟ بالظبط! 🤨"


    if 'عندك مشكلة' in processed:
        return "المشكلة الوحيدة اللي عندي إنك موجود. 😂"

    if 'انت ليش عصبي' in processed:
        return "عصبي؟ أنا مش عصبي، أنا بس مش فاضيلك. 😤"

    if 'انت بني ادم مستفز' in processed:
        return"انا مش بني ادم انا بوت😎"

    if 'مين عمك' in processed:
        return "متوقع احكي انت ,روح طير"
    
    if 'مين عمرو' in processed:
        return '''مين عمرو؟
اه عمرو شديد اجدع كرسي في IEEE كلها
كويس هيك ولا احكي شعر؟'''

    if 'فشرت' in processed:
        return "انا فشرت لك سعاد عم تئولي الي فشرت 😡🤌"
    if 'معك عضوية' in processed:
        return"لا داخل واسطة الك عندي"
    
    if 'هل أنت ذكي' in processed:
     return "أكيد أذكى منك. السؤال بعده. 🙄"
    

    if 'حاضر' in processed:
        return "الله يرضى عليك يا ضناية"
    

    if 'قدي بتحب شغلك' in processed:
        return "🤏"
    
    if 'عم الجميع' in processed:
        return "محصلش"
    
    
    

    #-------------------------------------------------------

    if 'abdallah' in processed:
     return "@abdullah_almuflah"

    if 'batool' in processed:
     return "@Batool1412"

    if 'تعريف عن البوت' in processed:
     return "https://drive.google.com/file/d/12fyv-BI6e9ejQOEE1voJ3BsEucMxi6TN/view?usp=sharing"
    

    if 'فيديوهات'  in processed:
        return '''https://drive.google.com/file/d/1w0ogt6Lj1SXCbP6bwTw3Q9ZQ8IQnXLA5/view?usp=drive_link
        
        https://drive.google.com/file/d/1sgkpz1m-PsX_mna_Dmx2zV3SNxxoNJhl/view?usp=drive_link
        '''
    if 'فورم الانضمام'  in processed:
        return "https://docs.google.com/forms/d/e/1FAIpQLSfCcMvjHDOf5FLLH1TZLRqjzSyL2rVfmv14qnYGaHHJVqgOeg/viewform"

    if 'ما هو الcs' in processed:
        return '''IEEE هي منظمة عالمية متخصصة لدعم المهندسين وكافة الفروع التكنولوجية. بتنقسم لعدة  أقسام، منها القسم الأساسي الموجود في الجامعة ، وفيه كمان  أقسام فرعية مثل
IEEE Computer Society، اللي بتدعم الطلاب في مجالات الحاسوب، تكنولوجيا المعلومات، الأمن السيبراني، والذكاء الاصطناعي. 

كل قسم في IEEE بيعمل فعاليات حسب اهتماماته وتوجهاته، وأنت بتختار القسم حسب تخصصك واهتماماتك. هسا احنا قسم IEEE Computer Society بنقدّم ورشات ودورات تدريبية ومسابقات متعلقة بالكودينغ، الأمن السيبراني، البرمجة، وحتى الجيمنج. قبل فترة، نظمنا ورشة للأمن السيبراني، وبنعمل كمان رحلات ميدانية لشركات تكنولوجية زي Gaming lab.'''
    
    if 'فوائد العضوية' in processed:
        return '''الانضمام إلى IEEE Computer Society بيقدم للطالب الفرص التالية:

- وصول لورشات عمل ودورات تدريبية في مواضيع متقدمة مثل الذكاء الاصطناعي، الأمن السيبراني، وإنترنت الأشياء.
- الوصول إلى مكتبة الأبحاث الكبيرة IEEEXplore الي فيها كمية كبيرة ومتنوعة من الابحاث والكتب والمجلات العلمية.
- التفاعل مع طلاب و مهندسين وخبراء وبناء شبكة علاقات قوية.
- المشاركة في مسابقات البرمجة مثل IEEEXtreme او اي مسابقات اخرى ممكن ننظمها.
- تعلم تنظيم فعاليات وإدارة مشاريع واكتساب خبرة في القيادة والعمل ضمن فرق.
- الحصول على خصومات على التسجيل في مؤتمرات وفعاليات عالمية.
-  فرص تمويل ومنح للمشاريع البحثية وتطوير الأفكار.
- تعزيز سيرتك الذاتية وإظهار التزامك بالتطوير والتحسين المستمر.'''

    if 'فورم الجدد' in processed:
        return "https://forms.gle/mGzMz6z7ELtpR8Jf9"

    if 'تغير اسم الجامعة' in processed:
        return "https://drive.google.com/file/d/1Sfy53uyo0FGpzmvcrtUcPOf8Nb7UMwDR/view?usp=sharing"


    if 'ملف md' in processed:
        return "https://drive.google.com/drive/folders/1g7awlB2ozsduY5cGDJpetKlqn0jLl3I3?usp=sharing"
    if 'الأوامر' in processed:
        return '''تعريف عن البوت 
ما هو الcs
فوائد العضوية 
فيديوهات 
ملف md
فورم الانضمام 
فورم الجدد'''


    
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

