import random
import threading

import telebot
from telebot import types
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

import constants as const
import dictionary as dt

# Initialize the bot using the bot token
bot = telebot.TeleBot(f"{const.API_KEY_TEST}")


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
        bot.send_message(message_id, f"{word['word']} - {word['translation']}")  # зачем????


# generates quiz when user types "/quiz"
def generate_quiz():
    answer_options = random.sample(dt.quiz_list, 4)
    word = random.choice(answer_options)
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


def send_quiz_via_chatid(chat_id):
    word, answer_options = generate_quiz()
    quiz_text = f"What is the Russian translation of the word '{word['word']}'?\n\n"
    quiz_keyboard = types.InlineKeyboardMarkup()
    for answer_option in answer_options:
        quiz_keyboard.add(
            types.InlineKeyboardButton(answer_option['translation'], callback_data=str(answer_option == word)))
    bot.send_message(chat_id=chat_id, text=quiz_text,
                     reply_markup=quiz_keyboard)  # здесь была ошибка, так как функция принимала именные аргументы,
                                                    # а ты передал позиционный


def send_quiz_spam():
    word, answer_options = generate_quiz()
    quiz_text = f"What is the Russian translation of the word '{word['word']}'?\n\n"
    quiz_keyboard = types.InlineKeyboardMarkup()
    for chat_id in const.chat_ids:
        for answer_option in answer_options:
            quiz_keyboard.add(
                types.InlineKeyboardButton(answer_option['translation'], callback_data=str(answer_option == word)))
        bot.send_message(chat_id=chat_id, text=quiz_text,
                         reply_markup=quiz_keyboard)



@bot.callback_query_handler(func=lambda call: True)
def check_quiz(call):
    is_correct = call.data == "True"
    if is_correct:
        message_text = "Correct answer!"
    else:
        message_text = "Sorry, that was incorrect."
    bot.answer_callback_query(callback_query_id=call.id, text=message_text)


def set_interval(func, sec):
    print("Я вызвал set_interval")
    def func_wrapper():
        set_interval(func, sec)
        func()

    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t


set_interval(send_quiz_spam, 28)

print(__name__)

if __name__ == '__main__':
    bot.polling()

# Этот код отправит тебе один квиз после того, когда ты остановишь бота. Надо смотреть как это сделать дальше.
# Пока что не изменил dictionary.py на dictionary.json, потому что заебался и хочу спать)))

# Кстати этот сервис который на м хостит бота, также может хостить БД, что можно использовать для хранения id чатов и
# отдельных словарей для пользователей

# B последнее, было бы неплохо изменить /add_word, чтобы он можно было закидывать много слов (например "слово1-перевод1;
# слово2-перевод2;..."), а также добавить
# возможность закидывать файл

# постараюсь добавить всё в issues, чтобы оно просто висело, а то заметки в коде - это пиздец
