import functools
import os
import threading
import time
import datetime

import telebot
from telebot import types
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
import constants as const
import processing
import processing as pr
import db_interface
import polls

from telegram.error import Conflict
from requests.exceptions import ConnectionError

# from functools import wraps

# Initialize the bot using the bot token
bot = telebot.TeleBot(f"{const.API_KEY_HOSTED}")

num_to_part = ["noun", "verb", "adj", "adv", "other"]


def retry_on_connection_error(max_retries=5):
    def decorator(func):
        # print("retry is done")

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except ConnectionError as e:
                    wait = 2 ** i  # exponential backoff
                    time.sleep(wait)
                    continue
            return None  # or you can re-raise the last exception

        return wrapper

    return decorator


def dec_check_user_in(func):
    """_summary_
        Checks if user is registered in the database;
        If not, sends a message to the user that he needs to register (/start)
    Args:
        func (_type_): function
    """

    @functools.wraps(func)
    def wrapper(message, *args, **kwargs):
        # print("check_user_in is done")
        # print(func.__name__)

        if db_interface.check_user_in(message.chat.id):
            func(message, *args, **kwargs)
        else:
            print("unregistered user tries to use the bot")
            bot.send_message(message.chat.id, "Для использования бота нажмите /start")

    return wrapper


# Debugs our great code to find the bug
def tryExceptWithFunctionName(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # print("try func is done")
        # print(func.__name__)
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(e)
            print(f"{func.__name__} - error occurred here")

    return wrapper


last_message_time = {}
rate_limit_window = 1
rate_limit_max_messages = 1


# A global rate limiter to ensure no single user gets above a fixed number of messages per second.
def rate_limit_decorator(func):
    @functools.wraps(func)
    def wrapper(message, *args, **kwargs):
        print("rate_limit is done")
        print(message.text)
        print(func.__name__)
        user_id = message.from_user.id
        now = time.time()
        print(now)
        print(last_message_time)
        # Check if the user is in the dictionary and the rate limit is exceeded
        if user_id in last_message_time:
            if now - last_message_time[user_id] < rate_limit_window:
                bot.send_message(user_id, "You've exceeded the rate limit.")
                return

        # Update the last message time for the user
        last_message_time[user_id] = now

        # Call the original function
        func(message, *args, **kwargs)

    return wrapper


# checks if there are users asking for quiz
# def set_interval(func, sec):
#     """_summary_
#         Sets an interval
#     Args:
#         func (_type_): function
#         sec (_type_): interval
#     """
#
#     def func_wrapper():
#         set_interval(func, sec)
#         func()
#
#     global t
#     t = threading.Timer(sec, func_wrapper)
#     t.start()
#     return t


# Define a function to handle the /help command
@bot.message_handler(commands=['help'])
@retry_on_connection_error(max_retries=5)
@tryExceptWithFunctionName
@rate_limit_decorator
@dec_check_user_in
def help_handler(message):
    bot.reply_to(message,
                 'Type:\n"/quiz" - to get a quiz\n'
                 '"/whole_dict" - to get all the words in your dictionary\n'
                 '"/start_mailing" - to start getting quizzes\n'
                 '"/stop_mailing" - to stop mailing\n'
                 '"/change_mailing_time" - to change mailing time\n'
                 '"/improve_word" - secret\n'
                 '"/admin_joking" - secret #2\n'
                 '"/game" - to get a game\n'
                 '"/add_word" - to add word to a dictionary\n'
                 '"/change_dict" - to change level of your dictionary')


# Define a function to handle the /start command
@bot.message_handler(commands=['start'])
@retry_on_connection_error(max_retries=5)
@tryExceptWithFunctionName
@rate_limit_decorator
def start_handler(message):
    menu_keyboard = ReplyKeyboardMarkup(row_width=1)
    menu_keyboard.add(KeyboardButton('/help'))
    reply_text = db_interface.userRegistration(message.chat.id)
    bot.reply_to(message, reply_text, reply_markup=menu_keyboard)


@bot.message_handler(commands=['whole_dict'])
@retry_on_connection_error(max_retries=5)
@tryExceptWithFunctionName
@rate_limit_decorator
@dec_check_user_in
def whole_dict_handler(message):
    bot.send_message(chat_id=message.chat.id, text="Генерирую файл...")
    dictionary = db_interface.get_words_by_user_id(message.chat.id)
    file_path = "./cache/output.txt"

    with open(file_path, "w", encoding="utf-8") as file:
        for partOfSpeech in dictionary:
            file.write(f"{partOfSpeech}:\n")
            for x in range(len(dictionary[partOfSpeech]['word'])):
                file.write(
                    f"{dictionary[partOfSpeech]['word'][x]}-{dictionary[partOfSpeech]['trsl'][x]}-{dictionary[partOfSpeech]['trsc'][x]}\n")

    bot.send_document(chat_id=message.chat.id, document=open(file_path, "rb"))
    os.remove(file_path)


# Add words from files to the dict
@bot.message_handler(content_types=['document'])
@retry_on_connection_error(max_retries=5)
@tryExceptWithFunctionName
@rate_limit_decorator
@dec_check_user_in
def add_dictionary_from_file(message):
    if db_interface.get_user_access(message.chat.id) == 'user':
        bot.reply_to(message, "Ваш уровень доступа не позволяет добавлять новый словарь.")
    else:
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

        new_dictionary = pr.prepare_text(file_content)
        text = db_interface.add_new_dictionary(new_dictionary, 'TEST')
        bot.reply_to(message, text)


# Sends messages to all users using the bot
@bot.message_handler(commands=['admin_joking'])
@retry_on_connection_error(max_retries=5)
@tryExceptWithFunctionName
@rate_limit_decorator
@dec_check_user_in
def admin_sends_message(message):
    if db_interface.get_user_access(message.chat.id) == 'user':
        bot.reply_to(message, "Ваш уровень доступа не позволяет добавлять новый словарь.")
        return

    bot.reply_to(message, "Брат, введи сообщение, которое хочешь отправить юзерам")
    bot.register_next_step_handler(message, admin_0)


@tryExceptWithFunctionName
def admin_0(message):
    list_of_users = db_interface.get_user_ids()
    for id in list_of_users:
        if db_interface.get_user_access(id) == 'admin' and id != message.chat.id:
            bot.send_message(id, message.text)

    bot.send_message(message.chat.id, "Отправил :)")


# sends quiz
@bot.message_handler(commands=['quiz'])
@retry_on_connection_error(max_retries=5)
@tryExceptWithFunctionName
@rate_limit_decorator
@dec_check_user_in
def send_quiz(MesOrNum, need_list=None):
    if need_list is None:
        need_list = []

    if not isinstance(MesOrNum, int):
        need_list.append(MesOrNum.chat.id)
    elif MesOrNum != 0:
        need_list.append(MesOrNum)

    if not db_interface.check_user_in(need_list[0]):
        bot.send_message(need_list[0], "Нажмите /start")
        return

    polls_by_dict_id = {}
    for user_id in need_list:
        dict_id = db_interface.get_user_dict_id(user_id)
        print(user_id, dict_id)
        if dict_id in polls_by_dict_id:
            polls_by_dict_id[dict_id].send(user_id, bot)
            continue
        polls_by_dict_id[dict_id] = polls.create_poll(dict_id)
        polls_by_dict_id[dict_id].send(user_id, bot)


# sends quiz with specific dict_id
@retry_on_connection_error(max_retries=5)
@tryExceptWithFunctionName
def send_quiz_with_dict_id(dict_id, chat_id):
    poll = polls.create_poll(dict_id)
    poll.send(chat_id, bot)


# function to send quizzes to the users
@retry_on_connection_error(max_retries=5)
@tryExceptWithFunctionName
def check_send_quiz():
    need_list = db_interface.get_needed_users()
    if len(need_list) == 0:
        return
    send_quiz(0, need_list)


# asks for a valid number
def get_valid_integer(text):
    while True:
        try:
            return int(text)
        except ValueError:
            return None


# updates user's mailing status
@bot.message_handler(commands=['start_mailing'])
@retry_on_connection_error(max_retries=5)
@tryExceptWithFunctionName
@rate_limit_decorator
@dec_check_user_in
def start_mailing(message):
    f = db_interface.started_mailing(message.chat.id)
    if f != 0:
        bot.send_message(message.chat.id, "У Вас уже запущена рассылка")
        return

    bot.send_message(message.chat.id, "Введите, как часто Вы хотите, чтобы приходили квизы(в минутах)")
    bot.register_next_step_handler(message, start_mailing_set)


@retry_on_connection_error(max_retries=5)
@tryExceptWithFunctionName
def start_mailing_set(message):
    try:
        minutes = get_valid_integer(message.text)
        if minutes is None:
            bot.reply_to(message, 'Пожалуйста, введите число')
            bot.register_next_step_handler(message, start_mailing_set)
            return
    except:
        bot.reply_to(message, 'Пожалуйста, введите число')
        bot.register_next_step_handler(message, start_mailing_set)
        return

    bot.send_message(message.chat.id, "Установил время рассылки")
    db_interface.update_mailing(message.chat.id, minutes)


# Stops mailing
@bot.message_handler(commands=['stop_mailing'])
@retry_on_connection_error(max_retries=5)
@tryExceptWithFunctionName
@rate_limit_decorator
@dec_check_user_in
def stop_mailing(message):
    f = db_interface.started_mailing(message.chat.id)
    if f != 0:
        bot.send_message(message.chat.id, "Остановил рассылку")
        db_interface.update_mailing(message.chat.id, 0)
    else:
        bot.send_message(message.chat.id, "У Вас не запущена рассылка")


# Changes a period of mailing
@bot.message_handler(commands=['change_mailing_time'])
@retry_on_connection_error(max_retries=5)
@tryExceptWithFunctionName
@rate_limit_decorator
@dec_check_user_in
def change_mailing_time(message):
    f = db_interface.started_mailing(message.chat.id)
    if f == 0:
        bot.send_message(message.chat.id, "У Вас не запущена рассылка")
        return

    # asks for number of minutes
    bot.reply_to(message, 'Введите, как часто Вы хотите, чтобы приходили квизы(в минутах)')
    bot.register_next_step_handler(message, start_mailing_set)  # start_mailing_set sets only new time for a user and
    # can be used in this function too


# Changes user's dict_id
@bot.message_handler(commands=['change_dict'])
@retry_on_connection_error(max_retries=5)
@tryExceptWithFunctionName
@rate_limit_decorator
@dec_check_user_in
def change_dict(message):
    keyboard = types.ReplyKeyboardMarkup()
    dict_ids = db_interface.get_dict_ids()
    for dict_id in dict_ids:
        if dict_id == "ALL":
            continue

        keyboard.row(dict_id)
    bot.send_message(message.chat.id, "Перед изменением словаря Вам будут даны несколько квизов, чтобы примерно "
                                      "понимать, какой уровень слов в словаре. Выберите словарь", reply_markup=keyboard)
    bot.register_next_step_handler(message, handle_buttons, dict_ids)


@retry_on_connection_error(max_retries=5)
@tryExceptWithFunctionName
def handle_buttons(message, dict_ids):
    chosen_option = message.text
    if chosen_option not in dict_ids:
        bot.send_message(message.chat.id, "Такой опции не было o_0. Try again", reply_markup=ReplyKeyboardRemove())
        return

    for i in range(3):
        send_quiz_with_dict_id(chosen_option, message.chat.id)

    bot.send_message(message.chat.id, "Если вас устраивает словарь, нажмите /yes, иначе выберите другой словарь")
    bot.register_next_step_handler(message, update_dict_in_bd, dict_ids, chosen_option)


@retry_on_connection_error(max_retries=5)
@tryExceptWithFunctionName
def update_dict_in_bd(message, dict_ids, chosen_option):
    cur_text = message.text
    if cur_text != "/yes":
        handle_buttons(message, dict_ids)
        return

    bot.send_message(message.chat.id, "Успешно изменил словарь", reply_markup=ReplyKeyboardRemove())
    db_interface.update_dict_id(message.chat.id, chosen_option)


# Creates a game for users
@bot.message_handler(commands=['game'])
@retry_on_connection_error(max_retries=5)
@tryExceptWithFunctionName
@rate_limit_decorator
@dec_check_user_in
def game_get_num(message):
    bot.reply_to(message, 'Введите количество квизов, которое вы хотите получить')
    bot.register_next_step_handler(message, game)


@retry_on_connection_error(max_retries=5)
@tryExceptWithFunctionName
@rate_limit_decorator
def game(message):
    try:
        times = get_valid_integer(message.text)
        if times is None:
            bot.reply_to(message, 'Пожалуйста, введите число')
            bot.register_next_step_handler(message, game)
            return
    except:
        bot.reply_to(message, 'Пожалуйста, введите число')
        bot.register_next_step_handler(message, game)
        return

    t_times = times
    cnt_correct = 0

    if times > 100 or times <= 0:
        bot.send_message(message.chat.id, "Мне кажется, вам не надо столько квизов. Выберите число меньше 100")
        bot.register_next_step_handler(message, game)
        return

    bot.send_message(message.chat.id, "На каждый вопрос у Вас будет 10 секунд")
    users_dict_id = db_interface.get_user_dict_id(message.chat.id)

    while times > 0:
        times = times - 1
        poll = polls.create_poll(users_dict_id)

        poll_message = poll.send(message.chat.id, bot)
        poll_message_id = poll_message.message_id

        time.sleep(10)
        poll_data = bot.stop_poll(message.chat.id, poll_message_id)

        user_option = None
        for i in range(4):
            option = poll_data.options[i]
            num_voters = option.voter_count
            if num_voters:
                user_option = i
                break

        if user_option == poll.correct_option_id:
            cnt_correct += 1

    bot.send_message(message.chat.id, f"Вы ответили правильно на {cnt_correct} вопросов из {t_times}")


# Fixes the word
@bot.message_handler(commands=['improve_word'])
@retry_on_connection_error(max_retries=5)
@tryExceptWithFunctionName
@rate_limit_decorator
@dec_check_user_in
def improve_word_0(message, is_add=0):
    access = db_interface.get_user_access(message.chat.id)
    if access != "admin":
        bot.send_message(message.chat.id, "У вас недостаточно прав o_0")
        return
    bot.send_message(message.chat.id, "формат: слово,перевод,транскрипция,часть речи (без пробелов!!)")
    bot.register_next_step_handler(message, improve_word_1, is_add)


# @bot.message_handler(content_types=['text'])
@retry_on_connection_error(max_retries=5)
@tryExceptWithFunctionName
def improve_word_1(message, is_add=0):
    access = db_interface.get_user_access(message.chat.id)
    if access != "admin":
        bot.send_message(message.chat.id, "У вас недостаточно прав o_0")
        return
    arr = message.text.split(",")
    keyboard = types.ReplyKeyboardMarkup()
    dict_ids = db_interface.get_dict_ids()
    for dict_id in dict_ids:
        keyboard.row(dict_id)
    bot.send_message(message.chat.id, "Выберите словарь", reply_markup=keyboard)
    bot.register_next_step_handler(message, improve_word, arr, is_add)


@retry_on_connection_error(max_retries=5)
@tryExceptWithFunctionName
def improve_word(message, arr, is_add=0):
    arr.append(message.text)
    for i in range(len(arr) - 1):
        arr[i] = arr[i].lower()
    print(arr)
    print(is_add)
    if is_add:
        uniqueness = processing.check_uniqueness(arr[0])
        if not uniqueness:
            bot.send_message(message.chat.id, "Такое слово уже существует :)", reply_markup=ReplyKeyboardRemove())
            return
        print(uniqueness)
        text = db_interface.add_word_to_dict(arr[0], arr[1], arr[2], arr[3], arr[4])
        print("good")
        bot.send_message(message.chat.id, text, reply_markup=ReplyKeyboardRemove())
        return

    if is_add:
        uniqueness = processing.check_uniqueness(arr[0])
        if not uniqueness:
            bot.send_message(message.chat.id, "Такое слово уже существует :)", reply_markup=ReplyKeyboardRemove())
            return
        text = db_interface.add_word_to_dict(arr[0], arr[1], arr[2], arr[3], arr[4])
        bot.send_message(message.chat.id, text, reply_markup=ReplyKeyboardRemove())
        return

    text = db_interface.fix_the_word(message.chat.id, arr)
    bot.send_message(message.chat.id, text, reply_markup=ReplyKeyboardRemove())


# adds word manually
@bot.message_handler(commands=['add_word'])
@retry_on_connection_error(max_retries=5)
@tryExceptWithFunctionName
def add_word_manually(message):
    improve_word_0(message, 1)


# After that goes a function that works with text not a command

@bot.message_handler(content_types=['text'])
@retry_on_connection_error(max_retries=5)
@tryExceptWithFunctionName
@rate_limit_decorator
@dec_check_user_in
def is_reply_to_bot_message(message):
    access = db_interface.get_user_access(message.chat.id)
    if access != "admin":
        bot.send_message(message.chat.id, "У вас недостаточно прав o_0")
        return
    if message.reply_to_message is not None:
        if message.reply_to_message.content_type == 'text':
            reply_process_text(message)
        elif message.reply_to_message.content_type == 'poll':
            reply_process_poll(message)
    else:
        improve_word_1(message)


# здесь надо обработать ответ на text
@retry_on_connection_error(max_retries=5)
@tryExceptWithFunctionName
def reply_process_text(message):
    word_text = message.reply_to_message.text
    partOfSpeech = message.text
    if word_text.count('-') != 2:
        bot.send_message(message.chat.id, "Видимо, Вы ответили не на нужное сообщение. Попробуйте /improve_word")
        return
    arr = [word_text.split("-")[0], partOfSpeech]
    keyboard = types.ReplyKeyboardMarkup()
    dict_ids = db_interface.get_dict_ids()
    for dict_id in dict_ids:
        keyboard.row(dict_id)
    bot.send_message(message.chat.id, "Выберите словарь", reply_markup=keyboard)
    bot.register_next_step_handler(message, improve_word, arr)


# здесь надо обработать ответ на poll
@retry_on_connection_error(max_retries=5)
@tryExceptWithFunctionName
def reply_process_poll(message):
    poll = message.reply_to_message.poll
    quest = poll.question

    # extracting the word
    quest = quest.split(":")[1]
    quest = quest.split("[")[0]
    position = 0
    quest = quest[:position] + quest[position + 1:]
    position = len(quest) - 1
    quest = quest[:position] + quest[position + 1:]

    arr = [quest, message.text]
    keyboard = types.ReplyKeyboardMarkup()
    dict_ids = db_interface.get_dict_ids()
    for dict_id in dict_ids:
        keyboard.row(dict_id)
    bot.send_message(message.chat.id, "Выберите словарь", reply_markup=keyboard)
    bot.register_next_step_handler(message, improve_word, arr)


def check_and_call():
    while True:
        current_time = datetime.datetime.now().time()
        current_seconds = current_time.second
        print(current_time)
        if current_seconds == 0:
            check_send_quiz()

        print("dictionary: ")
        print(last_message_time)

        # Adjust the sleep duration as needed (e.g., every minute)
        time.sleep(10)


def main():
    try:
        print(__name__)
        # set_interval(check_send_quiz, 60)

        # Start the time-checking function in a separate thread
        # time_check_thread = threading.Thread(target=check_and_call)
        # time_check_thread.daemon = True  # Set the thread as a daemon, so it exits when the main program exits
        # time_check_thread.start()

        bot.polling(none_stop=True)
    except Conflict:
        print("Another instance of the bot is running. Exiting.")
        exit(1)


if __name__ == '__main__':
    main()
