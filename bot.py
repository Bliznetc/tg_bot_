import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton 
import constants as const

# Initialize the bot using the bot token
bot = telebot.TeleBot(f"{const.API_KEY}")

# Define a function to handle the /start command
@bot.message_handler(commands=['start'])
def start_handler(message):
    menu_keyboard = ReplyKeyboardMarkup(row_width=1)
    menu_keyboard.add(KeyboardButton('/help'), KeyboardButton('/info'))
    bot.reply_to(message, 'Welcome to my bot!', reply_markup=menu_keyboard)


# Define a function to handle the /help command
@bot.message_handler(commands=['help'])
def help_handler(message):
    bot.reply_to(message, 'This is the help message.')

# Define a function to handle the /echo command
@bot.message_handler(commands=['echo'])
def echo_handler(message):
    message_text = message.text.split(maxsplit=1)[1] # Get the text after the command
    bot.reply_to(message, message_text)

@bot.message_handler(commands=['info'])
def info_handler(message):
    bot.reply_to(message, 'Rostislav Budarin - Lepshy')


# Start the bot
bot.polling()

#сделал фигню
#сделал фигню №2