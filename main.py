import json
import os
import threading
import time

import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, Message
import constants as const
import random
from telebot import types
import processing as pr
import db_interface

# Initialize the bot using the bot token
bot = telebot.TeleBot(f"{const.API_KEY_TEST}")


# Define a function to handle the /start command
@bot.message_handler(commands=['start'])
def start_handler(message):
    menu_keyboard = ReplyKeyboardMarkup(row_width=1)
    menu_keyboard.add(KeyboardButton('/help'))
    reply_text = db_interface.store(message.chat.id, "user", 0)
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
    dictionary = db_interface.get_words()
    file_path = "./cache/output.txt"

    with open(file_path, "w", encoding="utf-8") as file:
        for word in dictionary:
            file.write(f"{word['word']}-{word['translation']};\n")

    bot.send_document(chat_id=message.chat.id, document=open(file_path, "rb"))
    os.remove(file_path)
    bot.send_message(chat_id=message.chat.id, text="Файл успешно сгенерирован")
    # bot.send_message(message.chat.id, "Nope")


# adds word to the dictionary.json file
@bot.message_handler(commands=['add_word'])
def add_word(message):
    bot.reply_to(message, 'Введите новое слово и перевод в формате "слово-перевод"')
    bot.register_next_step_handler(message, add_and_verify)


def add_and_verify(message):
    bot.send_message(message.chat.id, "Добавляю...")
    listOfNewWords = pr.prepare_text(message.text)
    db_interface.add_word_to_bd(listOfNewWords, message.chat.id)
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
    db_interface.add_word_to_bd(listOfNewWords, message.chat.id)

    bot.reply_to(message, "Словарь обновлен")


# generates quiz when user types "/quiz"
def generate_quiz():
    # it takes 3.5 seconds to execute this function, 2.5 of which are dedicated to connect to db
    dictionary = db_interface.get_words()
    # dictionary.sort(key=lambda x: x['degree']) - не имеет смысла, так как мы и так берём все слова в рандом
    answer_options = random.sample(dictionary, 4)
    word_number = random.randint(0, 3)
    print(answer_options)  # for debugging
    return word_number, answer_options


# sends quiz
@bot.message_handler(commands=['quiz'])
def send_quiz(message):
    word_number, answer_options = generate_quiz()
    for answer in answer_options:
        answer['word'] = answer['word'].capitalize()
        answer['translation'] = answer['translation'].capitalize()

    # Отправка опроса в чат
    quiz_text = f"Какой перевод у слова: {answer_options[word_number]['word']}?\n"
    possible_answers = [answer['translation'] for answer in answer_options]

    bot.send_poll(message.chat.id, options=possible_answers, correct_option_id=word_number, type='quiz',
                  question=quiz_text)


# sets the interval for sending quizes
def set_interval(message, func, sec):
    print("Я вызвал set_interval")

    def func_wrapper():
        set_interval(message, func, sec)
        func(message)

    global t
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t


@bot.message_handler(commands=['start_mailing'])
def start_mailing(message):
    bot.send_message(message.chat.id, "введите, как часто Вы хотите, чтобы приходили квизы(в минутых)")

    bot.register_next_step_handler(message, start_mailing_time)


def start_mailing_time(message):
    minutes = int(message.text)

    # запуск рассылки, время переводится в секунды
    f = db_interface.started_mailing(message.chat.id)
    if f == 0:
        set_interval(message, send_quiz, minutes * 60)
        bot.send_message(message.chat.id, "запустил рассылку")
        db_interface.update_mailing(message.chat.id, 1)
    else:
        bot.send_message(message.chat.id, "У вас уже запущена рассылка")


@bot.message_handler(commands=['stop_mailing'])
def stop_mailing(message):
    f = db_interface.started_mailing(message.chat.id)
    if f == 1:
        t.cancel()
        bot.send_message(message.chat.id, "остановил рассылку")
        db_interface.update_mailing(message.chat.id, 0)
    else:
        bot.send_message(message.chat.id, "у Вас не запущена рассылка")


print(__name__)

if __name__ == '__main__':
    bot.polling()

