import os
import threading
import time

import telebot
from telebot import types
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, Message
import constants as const
import processing as pr
import db_interface
import polls

# Initialize the bot using the bot token
bot = telebot.TeleBot(f"{const.API_KEY_HOSTED}")

#зачем нам это
class Poll:
    def __init__(self, options, correct_option_id, question, is_anonymous):
        self.options = options
        self.correct_option_id = correct_option_id
        self.question = question
        self.is_anonymous = is_anonymous

    def send(self, chat_id, bot):
        poll_message= bot.send_poll(chat_id=chat_id, options=self.options,
                      correct_option_id=self.correct_option_id, type='quiz',
                      question=self.question, is_anonymous=self.is_anonymous)
        return poll_message


# Define a function to handle the /start command
@bot.message_handler(commands=['start'])
def start_handler(message):
    menu_keyboard = ReplyKeyboardMarkup(row_width=1)
    menu_keyboard.add(KeyboardButton('/help'))
    reply_text = db_interface.userRegistration(
        message.chat.id)  
    bot.reply_to(message, reply_text, reply_markup=menu_keyboard)


# Define a function to handle the /help command
@bot.message_handler(commands=['help'])
def help_handler(message):
    bot.reply_to(message,
                 'Type:\n"/quiz" - to get a quiz\n'
                 '"/whole_dict" - to check all the words\n'
                 '"/start_mailing" - to start getting quizzes\n'
                 '"/stop_mailing" - to stop mailing\n'
                 '"/change_mailing_time" - to change mailing time\n'
                 '"/game" - to get a game\n')

# '"/change_dict" - to change level of your dictionary\n'



@bot.message_handler(commands=['whole_dict'])
def whole_dict_handler(message):

    # t = time.time()
    # bot.send_message(chat_id=message.chat.id, text="Генерирую файл...")
    # dictionary = db_interface.get_all_words() #change it ---------------------------------------------
    # file_path = "./cache/output.txt"

    # with open(file_path, "w", encoding="utf-8") as file:
    #     for word in dictionary:
    #         file.write(f"{word['word']}-{word['translation']};\n")

    # bot.send_document(chat_id=message.chat.id, document=open(file_path, "rb"))
    # os.remove(file_path)
    # bot.send_message(chat_id=message.chat.id, text="Файл успешно сгенерирован")

    # print(time.time() - t, "out")
    bot.send_message(chat_id=message.chat.id, text="Временно недоступно")



# Add words from files to the dict
@bot.message_handler(content_types=['document'])
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

        bot.send_message(message.chat.id, "Добавляю...")

        new_dictionary = pr.prepare_text(file_content)
        text = db_interface.add_new_dictionary(new_dictionary, 'TEST')

        bot.reply_to(message, text)


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

    polls_by_dict_id = {}
    for user_id in need_list:
        dict_id = db_interface.get_user_dict_id(user_id)
        if dict_id in polls_by_dict_id:
            polls_by_dict_id[dict_id].send(user_id, bot)
            continue

        polls_by_dict_id[dict_id] = polls.create_poll(dict_id)
        polls_by_dict_id[dict_id].send(user_id, bot)

    print("Квизы успещно отправлены")


# function to send quizzes to the users
def check_send_quiz():
    need_list = db_interface.get_needed_users()
    send_quiz(0, need_list)


# checks if there are users asking for quiz
def set_interval(func, sec):
    print("Я вызвал set_interval")

    def func_wrapper():
        set_interval(func, sec)
        func()

    global t
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t


def get_valid_integer(text):
    while True:
        try:
            return int(text)
        except ValueError:
            return None


# updates user's mailing status
@bot.message_handler(commands=['start_mailing'])
def start_mailing(message):
    f = db_interface.started_mailing(message.chat.id)
    if f != 0:
        bot.send_message(message.chat.id, "У Вас уже запущена рассылка")
        return

    bot.send_message(message.chat.id, "Введите, как часто Вы хотите, чтобы приходили квизы(в минутах)")
    bot.register_next_step_handler(message, start_mailing_time)


def start_mailing_time(message):
    try:
        minutes = get_valid_integer(message.text)
        if minutes is None:
            bot.reply_to(message, 'Пожалуйста, введите число')
            bot.register_next_step_handler(message, change_mailing_time)
            return
    except:
        bot.reply_to(message, 'Пожалуйста, введите число')
        bot.register_next_step_handler(message, change_mailing_time)
        return

    f = db_interface.started_mailing(message.chat.id)
    if f == 0:
        bot.send_message(message.chat.id, "Запустил рассылку")
        db_interface.update_mailing(message.chat.id, minutes)

    else:
        bot.send_message(message.chat.id, "У Вас уже запущена рассылка")


# Stops mailing
@bot.message_handler(commands=['stop_mailing'])
def stop_mailing(message):
    f = db_interface.started_mailing(message.chat.id)
    if f != 0:
        bot.send_message(message.chat.id, "Остановил рассылку")
        db_interface.update_mailing(message.chat.id, 0)
    else:
        bot.send_message(message.chat.id, "У Вас не запущена рассылка")


# Changes a period of mailing
@bot.message_handler(commands=['change_mailing_time'])
def change_mailing_time_0(message):
    f = db_interface.started_mailing(message.chat.id)
    if f == 0:
        bot.send_message(message.chat.id, "У Вас не запущена рассылка")
        return

    bot.reply_to(message, 'Введите, как часто Вы хотите, чтобы приходили квизы(в минутах)')
    bot.register_next_step_handler(message, change_mailing_time)


def change_mailing_time(message):
    try:
        minutes = get_valid_integer(message.text)
        if minutes is None:
            bot.reply_to(message, 'Пожалуйста, введите число')
            bot.register_next_step_handler(message, change_mailing_time)
            return
    except:
        bot.reply_to(message, 'Пожалуйста, введите число')
        bot.register_next_step_handler(message, change_mailing_time)
        return


    f = db_interface.started_mailing(message.chat.id)
    if f != 0:
        bot.send_message(message.chat.id, "Изменил время")
        db_interface.update_mailing(message.chat.id, minutes)
    else:
        bot.send_message(message.chat.id, "У Вас не запущена рассылка")


# Changes user's dict_id
@bot.message_handler(commands=['change_dict'])
def change_dict(message):
    keyboard = types.ReplyKeyboardMarkup()
    dict_ids = db_interface.get_dict_ids()
    for dict_id in dict_ids:
        keyboard.row(dict_id)
    bot.send_message(message.chat.id, "Выберите словарь", reply_markup=keyboard)
    bot.register_next_step_handler(message, handle_buttons, dict_ids)


def handle_buttons(message, dict_ids):
    chosen_option = message.text
    if chosen_option in dict_ids:
        db_interface.update_dict_id(message.chat.id, chosen_option)
        bot.send_message(message.chat.id, "Успешно изменил словарь")
    else:
        bot.send_message(message.chat.id, "Такой опции не было o_0")


# Creates a game for users
@bot.message_handler(commands=['game'])
def game_get_num(message):
    bot.reply_to(message, 'Введите количество квизов, которое вы хотите получить')
    bot.register_next_step_handler(message, game)


def game(message):
    global user_option
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

    bot.send_message(message.chat.id, "На каждый вопрос у Вас будет 10 секунд")
    while times > 0:
        times = times - 1
        poll = polls.create_poll()


        poll_message = poll.send(message.chat.id, bot)
        poll_message_id = poll_message.message_id

        time.sleep(10)
        poll_data = bot.stop_poll(message.chat.id, poll_message_id)

        print(poll_data)
        user_option = None
        for i in range(4):
            option = poll_data.options[i]
            print(option)  # Print each option for debugging

            num_voters = option.voter_count
            if num_voters:
                user_option = i
                break

        if user_option == poll.correct_option_id:
            cnt_correct += 1

    bot.send_message(message.chat.id, f"Вы ответили правильно на {cnt_correct} вопросов из {t_times}")


# Creates a game for users
@bot.message_handler(commands=['improve_word'])
def improve_word_0(message):
    access = db_interface.get_user_access(message.chat.id)
    if access != "admin":
        bot.send_message(message.chat.id, "У вас недостаточно прав o_0")
        return
    bot.send_message(message.chat.id, "формат: слово,перевод,транскрипция,часть речи")
    bot.register_next_step_handler(message, improve_word_1)


def improve_word_1(message):
    arr = message.text.split(",")
    keyboard = types.ReplyKeyboardMarkup()
    dict_ids = db_interface.get_dict_ids()
    for dict_id in dict_ids:
        keyboard.row(dict_id)
    bot.send_message(message.chat.id, "Выберите словарь", reply_markup=keyboard)
    bot.register_next_step_handler(message, improve_word, arr)


def improve_word(message, arr):
    arr.append(message.text)
    for i in range(len(arr)):
        arr[i] = arr[i].lower()
        print(arr[i])
    bot.send_message(message.chat.id, f"слово - {arr[0]}, перевод - {arr[1]}, транскр - {arr[2]}, часть речи - {arr[3]}, словарь - {arr[4]}")
    text = db_interface.fix_the_word(message.chat.id, arr)
    bot.send_message(message.chat.id, text)

print(__name__)
set_interval(check_send_quiz, 60)



if __name__ == '__main__':
    bot.polling()
