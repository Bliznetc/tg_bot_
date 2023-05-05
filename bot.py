#!D:\python\python.exe
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import constants as const
import random
import dictionary as dt
from telebot import types

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
    bot.reply_to(message, 'Type\n"/quiz" - to get a quiz\n "/add_word" - to add a new word\n "/whole_dict" - to check '
                          'all the words')


# Define a function to handle the /echo command
@bot.message_handler(commands=['echo'])
def echo_handler(message):
    message_text = message.text.split(maxsplit=1)[1]  # Get the text after the command
    bot.reply_to(message, message_text)


@bot.message_handler(commands=['info'])
def info_handler(message):
    bot.reply_to(message, 'Rostislav Budarin - Lepshy')


@bot.message_handler(commands=['add_word'])
def add_word(message):
    bot.reply_to(message, 'Введите новое слово и перевод в формате "слово-перевод"')
    bot.register_next_step_handler(message, add_word_to_dict)


def add_word_to_dict(message):
    new_key = message.text.split('-')[0]
    new_meaning = message.text.split('-')[1]
    dt.quiz_list.append({'word': new_key, 'translation': new_meaning})  # здесь было неправильно
    bot.send_message(message.chat.id, f"ваше слово: {new_key}, перевод: {new_meaning}")
    print(len(dt.quiz_list))
    printAllWords(message.from_user.id)


def printAllWords(message_id):
    for word in dt.quiz_list:
        bot.send_message(message_id, f"{word['word']} - {word['translation']}") #зачем????


# generates quiz when user types "/quiz"
def generate_quiz():
    word = random.choice(dt.quiz_list)
    answer_options = random.sample(dt.quiz_list, 3)
    f = 1
    for a in answer_options:
        if a['word'] == word['word']:
            f = 0

    if f == 1:
        answer_options.append(word)
    else:
        for a in dt.quiz_list:
            ok = 1
            for b in answer_options:
                if a['word'] == b['word']:
                    ok = 0

            if ok == 1:
                answer_options.append(a)
                break

    print(answer_options)  # for debugging
    random.shuffle(answer_options)
    return word, answer_options


@bot.message_handler(commands=['quiz'])
def send_quiz(message):
    word, answer_options = generate_quiz()
    quiz_text = f"What is the Russian translation of the word '{word['word']}'?\n\n"
    quiz_keyboard = types.InlineKeyboardMarkup()
    for answer_option in answer_options:
        quiz_keyboard.add(
            types.InlineKeyboardButton(answer_option['translation'], callback_data=str(answer_option == word)))
    bot.send_message(chat_id=message.chat.id, text=quiz_text, reply_markup=quiz_keyboard)


@bot.callback_query_handler(func=lambda call: True)
def check_quiz(call):
    is_correct = call.data == "True"
    if is_correct:
        message_text = "Correct answer!"
    else:
        message_text = "Sorry, that was incorrect."
    bot.answer_callback_query(callback_query_id=call.id, text=message_text)


print(__name__)

if __name__ == '__main__':
    bot.polling()

# сделал фигню
# сделал фигню №2
