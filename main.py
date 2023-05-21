import json
import os
import threading

import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, Message
import constants as const
import random
from telebot import types
import json_functions as jsonFunc
import test

# Initialize the bot using the bot token
bot = telebot.TeleBot(f"{const.API_KEY_TEST}")


# Define a function to handle the /start command
@bot.message_handler(commands=['start'])
def start_handler(message):
    menu_keyboard = ReplyKeyboardMarkup(row_width=1)
    menu_keyboard.add(KeyboardButton('/help'))
    test.store(message.chat.id, "user", 0)
    bot.reply_to(message, 'Welcome to my bot!', reply_markup=menu_keyboard)


# Define a function to handle the /help command
@bot.message_handler(commands=['help'])
def help_handler(message):
    bot.reply_to(message, 'Type:\n"/quiz" - to get a quiz\n "/add_word" - to add a new word\n "/whole_dict" - to check all the words\n'
                '"/start_mailing" - to start getting quizes\n "/stop_mailing" - to stop mailing' )


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
    jsonFunc.add_word_to_dt(message.text)
    bot.send_message(message.chat.id, "Словарь обновлен!")

#Add words from files to the dict
@bot.message_handler(content_types=['document'])
def add_word_from_file (message):
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
    
    jsonFunc.add_word_to_dt(file_content)

    bot.reply_to(message, "Словарь обновлен")



# generates quiz when user types "/quiz"
def generate_quiz():
    answer_options = jsonFunc.create_answer_options()
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
    possible_answers = []
    for answer in answer_options:
        possible_answers.append(answer['translation'])

    bot.send_poll(message.chat.id, options=possible_answers, correct_option_id=word_number, type='quiz', question=quiz_text)


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


def start_mailing_time (message):
    minutes = int(message.text)

    #запуск рассылки, время переводится в секунды
    f = test.started_mailing(message.chat.id)
    if f == 0:
        set_interval(message, send_quiz, minutes * 60)
        bot.send_message(message.chat.id, "запустил рассылку")
        test.update_mailing(message.chat.id, 1)
    else:
        bot.send_message(message.chat.id, "у Вас уже запущена рассылка")

@bot.message_handler(commands=['stop_mailing'])
def stop_mailing(message):
    f = test.started_mailing(message.chat.id)
    if f == 1:
        t.cancel()
        bot.send_message(message.chat.id, "остановил рассылку")
        test.update_mailing(message.chat.id, 0)
    else:
        bot.send_message(message.chat.id, "у Вас не запущена рассылка")


print(__name__)

if __name__ == '__main__':
    bot.polling()



# Кстати этот сервис который на м хостит бота, также может хостить БД, что можно использовать для хранения id чатов и
# отдельных словарей для пользователей

# B последнее, было бы неплохо изменить /add_word, чтобы он можно было закидывать много слов (например "слово1-перевод1;
# слово2-перевод2;..."), а также добавить
# возможность закидывать файл

# постараюсь добавить всё в issues, чтобы оно просто висело, а то заметки в коде - это пиздец