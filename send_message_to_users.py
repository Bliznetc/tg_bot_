import telebot
import constants as const
import db_interface


def sendmessage(text):
    bot = telebot.TeleBot(f"{const.API_KEY_HOSTED}")
    listOfUserIds = db_interface.get_user_ids()
    for userId in listOfUserIds:
        try:
            bot.send_message(chat_id=userId, text=text)
            print(f"successfully sent the message to user_id = {userId}")
        except:
            print(f"user_id = {userId} - blocked the bot")