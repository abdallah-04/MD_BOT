from typing import final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from TEST import message1,message2,message3
# Bot token and username
TOKEN: final = '7932025838:AAGswbpqMbPnQnsYLlY8lR_i6ZOoVmydTN0'
BOT_USERNAME = '@MD_BAU_bot'

# Define the start command
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(message1)
    await update.message.reply_text(message2)
    await update.message.reply_text(message3)

# Define the help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("My job is to help the MD members.")

# Function to handle text responses
def handle_response(text: str) -> str:
    processed: str = text.lower()  # Lowercase everything for easy matching

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

# Function to handle messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type  # Fixed assignment
    text: str = update.message.text  # Fixed assignment

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == 'group':  # Fixed condition
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return  # Ignore messages not directed at the bot
    else:
        response: str = handle_response(text)

    print('Bot:', response)
    await update.message.reply_text(response)  # Fixed: Added `await`

async def error (update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'update{update} caused error {context.error}')

if __name__=='__main__':
    print("strting bot....") 
    app=Application.builder().token(TOKEN).build()
       
    #command
    app.add_handler(CommandHandler('start',start_command))
    app.add_handler(CommandHandler('help',help_command))
    
    #message
    app.add_handler(MessageHandler(filters.TEXT,handle_message))

    #error

    app.add_error_handler(error)

    print("polling....") 
    app.run_polling(poll_interval=3)




