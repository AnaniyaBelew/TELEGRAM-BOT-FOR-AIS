from typing import Final
# pip install python-telegram-bot
from telegram import Update,ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes,CallbackContext,ConversationHandler
print('Starting up bot...')
TOKEN: Final = '6214753896:AAEyoypGyT84yxz3e3hWqsYGQdW8SZvylPA'
BOT_USERNAME: Final = '@AISASTU_bot'
data={'username':'','password':''}
USERNAME=1 
PASSWORD =2
# Lets us use the /start command
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello this is the AIS customer support BOT Please Enter your username")
    context.user_data['username']
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "1: Lorem Ipsum is simplywhen an unknown printer took a galley of type and scrambled it to make a type specimen book.\n\n" 
        "2: It has survived not only five centuries.\n\n"
        "3: Lorem Ipsum is simply dummy text of the printing and typesetting industry.\n\n"
        "4: Lorem Ipsum is simply dummy text of the printing and typesetting industry.",
        reply_markup=ReplyKeyboardRemove()
    )
async def login(update:Update,context:ContextTypes.DEFAULT_TYPE):
    global data
    data={'username':'','password':''}
    await update.message.reply_text("add username and password in separated messages\n\nnow write Username")
    return USERNAME
async def get_username(update:Update,context:ContextTypes.DEFAULT_TYPE):
    data['username']=update.message.text
    await update.message.reply_text(f"username: {update.message.text}\n\nnow write password")
    return PASSWORD
async def get_password(update:Update,context:ContextTypes.DEFAULT_TYPE):
    data['password']=update.message.text
    await update.message.reply_text(f"Password: {update.message.text}")
    msg = """I got all data

title: {}
text: {}
comments: {}""".format(data['username'], data['password'])
    await update.message.reply_text(msg)
    return ConversationHandler.END
async def cancel(update:Update,context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('canceled')
    # end of conversation
    return ConversationHandler.END
my_conversation_handler = ConversationHandler(
   entry_points=[CommandHandler('login', login)],
   states={
       USERNAME: [
           CommandHandler('cancel', cancel),  # has to be before MessageHandler to catch `/cancel` as command, not as `title`
           MessageHandler(filters.TEXT, get_username)
       ],
       PASSWORD: [
           CommandHandler('cancel', cancel),  # has to be before MessageHandler to catch `/cancel` as command, not as `text`
           MessageHandler(filters.TEXT, get_password)
       ],
   },
   fallbacks=[CommandHandler('cancel', cancel)],
   conversation_timeout=None
) 

""" def handle_response(text: str) -> str:
    # Create your own response logic
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
    await update.message.reply_text(response) """
# Log errors
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')
# Run the program
if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('login', login))
    # Messages
    # app.add_handler(MessageHandler(filters.TEXT, handle_message))
    app.add_handler( my_conversation_handler)
    # Log all errors
    app.add_error_handler(error)

    print('Polling...')
    # Run the bot
    app.run_polling(poll_interval=5)