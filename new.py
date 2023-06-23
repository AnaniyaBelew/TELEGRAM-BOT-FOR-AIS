
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
logger = logging.getLogger(__name__)

# Set the credentials for authentication
valid_username = "admin"
valid_password = "password"

# Define the start command handler
def start(update: Update, context: CallbackContext):
    update.message.reply_text('Hi! Please enter your username and password to login.')

# Define the login command handler
def login(update: Update, context: CallbackContext):
    # Get the user's input
    user_input = update.message.text.split()

    if len(user_input) != 3:
        update.message.reply_text('Invalid input! Please enter your username and password separated by a space.')
        return

    username = user_input[1]
    password = user_input[2]

    if username == valid_username and password == valid_password:
        update.message.reply_text('Login successful!')
    else:
        update.message.reply_text('Invalid username or password!')

# Define the main function to start the bot
def main():
    # Create an instance of the Updater class and pass your bot's token
    updater = Updater('6276254374:AAGTBqXm5l_AWzVv7nvZht1JtJOLzndaYHI',True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add handlers for the supported commands
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('login', login))

    # Start the bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C
    updater.idle()

# Run the main function
if __name__ == '__main__':
    main()

