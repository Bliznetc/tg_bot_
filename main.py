import json
import threading

import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import constants as const
import random
from telebot import types
import json_functions as jsonFunc

# Initialize the bot using the bot token
bot = telebot.TeleBot(f"{const.API_KEY_HOSTED}")


# Define a function to handle the /start command
@bot.message_handler(commands=['start'])
def start_handler(message):
    menu_keyboard = ReplyKeyboardMarkup(row_width=1)
    menu_keyboard.add(KeyboardButton('/help'), KeyboardButton('/info'))
    bot.reply_to(message, 'Welcome to my bot!', reply_markup=menu_keyboard)


# Define a function to handle the /help command
@bot.message_handler(commands=['help'])
def help_handler(message):
    bot.reply_to(message, 'Type\n"/quiz" - to get a quiz\n "/add_word" - to add a new word\n "/whole_dict" - to check all the words\n'
                '"/start_mailing" - to start getting quizes')


# Define a function to handle the /whole_dict command
@bot.message_handler(commands=['whole_dict'])
def whole_dict_handler(message):
    with open("dictionary.json", "r", encoding="utf-8") as file:
        dictionary = json.load(file)

    for word in dictionary:
        bot.send_message(message.chat.id, f"{word['word']} - {word['translation']}")


@bot.message_handler(commands=['info'])
def info_handler(message):
    bot.reply_to(message, 'Rostislav Budarin - Lepshy')


# adds word to the dictionary.json file
@bot.message_handler(commands=['add_word'])
def add_word(message):
    bot.reply_to(message, 'Введите новое слово и перевод в формате "слово-перевод"')
    bot.register_next_step_handler(message, add_and_verify)


def add_and_verify(message):
    jsonFunc.add_word_to_dt(message)
    bot.send_message(message.chat.id, "Словарь обновлен!")


# generates quiz when user types "/quiz"
def generate_quiz():
    answer_options = jsonFunc.create_answer_options()
    word = random.choice(answer_options)
    print(answer_options)  # for debugging
    random.shuffle(answer_options)
    return word, answer_options


# sends quiz
@bot.message_handler(commands=['quiz'])
def send_quiz(message):
    word, answer_options = generate_quiz()
    quiz_text = f"What is the Russian translation of the word '{word['word']}'?\n\n"
    quiz_keyboard = types.InlineKeyboardMarkup()
    for answer_option in answer_options:
        quiz_keyboard.add(
            types.InlineKeyboardButton(answer_option['translation'], callback_data=str(answer_option == word)))
    bot.send_message(chat_id=message.chat.id, text=quiz_text, reply_markup=quiz_keyboard)


#--------------------------
#эта функция по-моему вообще не используется, не помню для чего я ее написал
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
#-----------------------------


#sends quiz to every user
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
        
        quiz_keyboard = types.InlineKeyboardMarkup()

# checks quiz
@bot.callback_query_handler(func=lambda call: True)
def check_quiz(call):
    is_correct = call.data == "True"
    if is_correct:
        message_text = "Correct answer!"
    else:
        message_text = "Sorry, that was incorrect."
    bot.answer_callback_query(callback_query_id=call.id, text=message_text)


#sets the interval for sending quizes
def set_interval(func, sec):
    print("Я вызвал set_interval")
    def func_wrapper():
        set_interval(func, sec)
        func()

    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t


@bot.message_handler(commands=['start_mailing'])
def start_mailing(message):
    set_interval(send_quiz_spam, 10)
    bot.send_message(message.chat.id, "запустил рассылку")

@bot.message_handler(commands=['stop_mailing'])
def stop_mailing(message):
    set_interval(send_quiz_spam, 4) #запускает второй поток
    bot.send_message(message.chat.id, "остановил рассылку")

print(__name__)

if __name__ == '__main__':
    bot.polling()



# Кстати этот сервис который на м хостит бота, также может хостить БД, что можно использовать для хранения id чатов и
# отдельных словарей для пользователей

# B последнее, было бы неплохо изменить /add_word, чтобы он можно было закидывать много слов (например "слово1-перевод1;
# слово2-перевод2;..."), а также добавить
# возможность закидывать файл

# постараюсь добавить всё в issues, чтобы оно просто висело, а то заметки в коде - это пиздец