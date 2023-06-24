import requests
import json
from typing import Final
from prettytable import PrettyTable
# pip install python-telegram-bot
from telegram import Update,ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes,CallbackContext,ConversationHandler
print('Starting up bot...')
TOKEN: Final = '6214753896:AAEyoypGyT84yxz3e3hWqsYGQdW8SZvylPA'
BOT_USERNAME: Final = '@AISASTU_bot'
data={'username':'','password':''}
logged_in=False
USERNAME=1 
PASSWORD =2
# Lets us use the /start command
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello this is the AIS customer support BOT Please Enter your username")
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "1: Lorem Ipsum is simplywhen an unknown printer took a galley of type and scrambled it to make a type specimen book.\n\n" 
        "2: It has survived not only five centuries.\n\n"
        "3: Lorem Ipsum is simply dummy text of the printing and typesetting industry.\n\n"
        "4: Lorem Ipsum is simply dummy text of the printing and typesetting industry.",
        reply_markup=ReplyKeyboardRemove()
    )
def get_bearer(username,password):
    api_url = "http://ais.blackneb.com/api/token/"
    payload = {
        "username": username,
        "password": password
    }
    try:
        response = requests.post(api_url, data=payload)
        response.raise_for_status()  # Raise an exception if the request was not successful
        return response.text  # Return the response from the API
    except requests.exceptions.RequestException as e:
        # Handle any errors that occurred during the request
        print(f"An error occurred: {e}")
        return None
def login_access(username,password,tok):
    api_url = "http://ais.blackneb.com/api/ais/login"
    headers= {
     "Authorization": f"Bearer {tok}",
}
    payload = {
        "username": username,
        "password": password
    }
    try:
        response = requests.post(api_url, headers=headers,data=payload)
        response.raise_for_status()  # Raise an exception if the request was not successful
        return response.text  # Return the response from the API
    except requests.exceptions.RequestException as e:
        # Handle any errors that occurred during the request
        print(f"An error occurred: {e}")
        return None
def get_claims(id):
    api_url = "http://ais.blackneb.com/api/ais/getclaimsbot"
    payload = {
        "proposerID": id,
    }
    try:
        response = requests.post(api_url,data=payload)
        response.raise_for_status()  # Raise an exception if the request was not successful
        return response.text  # Return the response from the API
    except requests.exceptions.RequestException as e:
        # Handle any errors that occurred during the request
        print(f"An error occurred: {e}")
        return None
def print_dict_as_table(dictionary):
    table = PrettyTable(dictionary.keys())
    table.add_row(dictionary.values())
    return table
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
    resp_auth=get_bearer(data['username'],data['password'])
    newresp=json.loads(resp_auth)
    ref=newresp['refresh']
    acc=newresp['access']
    resp_acc=login_access(data['username'],data['password'],str(acc))
    newresp_acc=json.loads(resp_acc)
    stat=newresp_acc[0]
    if(stat['status']=='pass'):
        getresp=json.loads(get_claims(stat['proposerID']))
        claim=getresp[0]
        claim_displayed=print_dict_as_table(claim)
        await update.message.reply_text("login success\n"+str(claim_displayed))
        print("login Success")
    else:
        await update.message.reply_text("login failed. Please login again")
        print("login Failed")
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
# Log errors
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')
# Run the program
if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    # Messages
    # app.add_handler(MessageHandler(filters.TEXT, handle_message))
    app.add_handler( my_conversation_handler)
    # Log all errors
    app.add_error_handler(error)

    print('Polling...')
    # Run the bot
    app.run_polling(poll_interval=5)