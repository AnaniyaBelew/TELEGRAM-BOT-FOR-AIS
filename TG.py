

from typing import Final

# pip install python-telegram-bot
from telegram import Update,ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

print('Starting up bot...')

TOKEN: Final = '6276254374:AAGTBqXm5l_AWzVv7nvZht1JtJOLzndaYHI'
BOT_USERNAME: Final = '@Aisais_bot'


# Lets us use the /start command
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_keyboard = [["Login", "FAQ"]]
    await update.message.reply_text(
        "Hi! This is AIS BOT "
        "Choose\n\n"
        "What you want to do",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Choose",resize_keyboard=True
        ),
    )


# Lets us use the /help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "1: Lorem Ipsum is simplywhen an unknown printer took a galley of type and scrambled it to make a type specimen book.\n\n" 
        "2: It has survived not only five centuries.\n\n"
        "3: Lorem Ipsum is simply dummy text of the printing and typesetting industry.\n\n"
        "4: Lorem Ipsum is simply dummy text of the printing and typesetting industry.",
        reply_markup=ReplyKeyboardRemove()
    )


# Lets us use the /custom command
async def login_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Wellcome To AIS Please Enter your username and password ",
        reply_markup=ReplyKeyboardRemove()
    )
    async def check():
        txt:str =update.message.text
        if(txt=="anew"):
            await update.message.reply_to_message("Success")
        else:
            await update.message.reply_to_message("Failed")
def handle_response(text: str) -> str:
    processed: str = text.lower()

    if 'hello' in processed:
        return 'Hey there!'

    if 'how are you' in processed:
        return 'I\'m good!'

    if 'i love python' in processed:
        return 'Remember to subscribe!'

    return 'I don\'t understand'



        

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Get basic info of the incoming message
    message_type: str = update.message.chat.type
    text: str = update.message.text

    # Print a log for debugging
    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    # React to group messages only if users mention the bot directly
    if message_type == 'group':
        # Replace with your bot username
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return  # We don't want the bot respond if it's not mentioned in the group
    else:
        response: str = handle_response(text)

    # Reply normal if the message is in private
    print('Bot:', response)
    await update.message.reply_text(response)


# Log errors
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


# Run the program
if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('login', login_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Log all errors
    app.add_error_handler(error)

    print('Polling...')
    # Run the bot
    app.run_polling(poll_interval=1)