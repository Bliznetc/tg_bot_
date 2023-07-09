import telebot
import constants as const
import db_interface

if __name__ == "__main__":
    bot = telebot.TeleBot(f"{const.API_KEY_HOSTED}")
    listOfUserIds = db_interface.get_user_ids()
    text = "Мы рады сообщить, что бот снова работает.\n\nТеперь пользователи могут выбирать словарь по уровню сложности написав команду /change_dict\n\n(В данный момент мы советуем использовать словарь 'TEST_A1' или 'TEST_ALL', там находится более 3000 слов, остальные словари сейчас наполняются словами)\n\nБыли исправлены ошибки и доработаны существующие функции."
    for userId in listOfUserIds:
        try:
            bot.send_message(chat_id=userId, text=text)
            print(f"successfully sent the message to user_id = {userId}")
        except:
            print(f"user_id = {userId} - blocked the bot")