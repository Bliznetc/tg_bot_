import os
import threading
import time

import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, Message
import constants as const
import random
import processing as pr
import db_interface_test

# Initialize the bot using the bot token
bot = telebot.TeleBot(f"{const.API_KEY_HOSTED}")


# Define a function to handle the /start command
@bot.message_handler(commands=['start'])
def start_handler(message):
    menu_keyboard = ReplyKeyboardMarkup(row_width=1)
    menu_keyboard.add(KeyboardButton('/help'))
    reply_text = db_interface_test.store(message.chat.id, "user", 0)
    bot.reply_to(message, reply_text, reply_markup=menu_keyboard)


# Define a function to handle the /help command
@bot.message_handler(commands=['help'])
def help_handler(message):
    bot.reply_to(message,
                 'Type:\n"/quiz" - to get a quiz\n "/add_word" - to add a new word\n "/whole_dict" - to check all the words\n'
                 '"/start_mailing" - to start getting quizes\n "/stop_mailing" - to stop mailing')


# Define a function to handle the /whole_dict command
@bot.message_handler(commands=['whole_dict'])
def whole_dict_handler(message):
    t = time.time()
    bot.send_message(chat_id=message.chat.id, text="Генерирую файл...")
    dictionary = db_interface_test.get_words()
    file_path = "./cache/output.txt"

    with open(file_path, "w", encoding="utf-8") as file:
        for word in dictionary:
            file.write(f"{word['word']}-{word['translation']};\n")

    bot.send_document(chat_id=message.chat.id, document=open(file_path, "rb"))
    os.remove(file_path)
    bot.send_message(chat_id=message.chat.id, text="Файл успешно сгенерирован")
    
    print(time.time() - t, "out")


# adds word to the dictionary.json file
@bot.message_handler(commands=['add_word'])
def add_word(message):
    bot.reply_to(message, 'Введите новое слово и перевод в формате "слово1-перевод1;слово2-перевод2;и тд"')
    bot.register_next_step_handler(message, add_and_verify)


# Добавляет слова непосредственно в словарь
def add_and_verify(message):
    bot.send_message(message.chat.id, "Добавляю...")
    listOfNewWords = pr.prepare_text(message.text)
    db_interface_test.add_word_to_bd(listOfNewWords, message.chat.id)
    bot.send_message(message.chat.id, "Словарь обновлен!")


# Add words from files to the dict
@bot.message_handler(content_types=['document'])
def add_word_from_file(message):
    file_info = message.document
    file_id = file_info.file_id
    file_name = file_info.file_name

    # Запрос файла с использованием его file_id
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    # Сохранение файла локально
    with open(file_name, 'wb') as new_file:
        new_file.write(downloaded_file)

    # Чтение содержимого файла
    with open(file_name, 'r', encoding='utf-8') as file:
        file_content = file.read()

    os.remove(file_name)

    bot.send_message(message.chat.id, "Добавляю...")

    listOfNewWords = pr.prepare_text(file_content)
    db_interface_test.add_word_to_bd(listOfNewWords, message.chat.id)

    bot.reply_to(message, "Словарь обновлен")


# generates quiz when user types "/quiz"
def generate_quiz():
    dictionary = db_interface_test.get_words()
   
    answer_options = random.sample(dictionary, 4)
    word_number = random.randint(0, 3)
    print(answer_options)  # for debugging
    return word_number, answer_options


# sends quiz
@bot.message_handler(commands=['quiz'])
def send_quiz(MesOrNum, need_list=None):
    if need_list is None:
        need_list = []

    if isinstance(MesOrNum, int):
        chat_id = MesOrNum
    else:
        chat_id = MesOrNum.chat.id
        need_list.append(chat_id)

    word_number, answer_options = generate_quiz()
    
    for answer in answer_options:
        answer['word'] = answer['word'].capitalize()
        answer['translation'] = answer['translation'].capitalize()

    # Отправка опроса в чат
    quiz_text = f"Как переводится слово: {answer_options[word_number]['word']}?\n"
    possible_answers = [answer['translation'] for answer in answer_options]

    # print(need_list)

    for chat_id1 in need_list:
        bot.send_poll(chat_id1, options=possible_answers, correct_option_id=word_number, type='quiz',
                      question=quiz_text)
    

# function to send quizzes to the users
def check_send_quiz():
    need_list = db_interface_test.get_needed_users()
    send_quiz(0, need_list)


def set_interval(func, sec):
    print("Я вызвал set_interval")

    def func_wrapper():
        set_interval(func, sec)
        func()

    global t
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t


@bot.message_handler(commands=['start_mailing'])
def start_mailing(message):
    bot.send_message(message.chat.id, "Введите, как часто Вы хотите, чтобы приходили квизы(в минутах)")
    bot.register_next_step_handler(message, start_mailing_time)


def start_mailing_time(message):
    minutes = int(message.text)
    # запуск рассылки, время переводится в секунды
    f = db_interface_test.started_mailing(message.chat.id)
    if f == 0:
        bot.send_message(message.chat.id, "Запустил рассылку")
        db_interface_test.update_mailing(message.chat.id, minutes)

    else:
        bot.send_message(message.chat.id, "У Вас уже запущена рассылка")


@bot.message_handler(commands=['stop_mailing'])
def stop_mailing(message):
    f = db_interface_test.started_mailing(message.chat.id)
    if f != 0:
        # t.cancel()
        bot.send_message(message.chat.id, "Остановил рассылку")
        db_interface_test.update_mailing(message.chat.id, 0)
    else:
        bot.send_message(message.chat.id, "У Вас не запущена рассылка")


print(__name__)
set_interval(check_send_quiz, 60)

if __name__ == '__main__':
    bot.polling()
