import telebot
import constants as const
import db_interface_test

if __name__ == "__main__":
    bot = telebot.TeleBot(f"{const.API_KEY_HOSTED}")
    listOfUserIds = db_interface_test.get_user_ids()
    text = "Наша команда считает, что необходимо уведомлять пользователей о текущем состоянии бота и последних новостях, поэтому мы создаем эту рассылку.\n\nВ будущем мы планируем реализовать новый функционал, который позволит пользователям давать обратную связь непосредственно через бота. Таким образом, мы сможем быстро и точно исправлять возникающие ошибки при его работе.\n\nВ данный момент мы обновляем польский словарь, так как старый содержал мало слов и множество неточностей. По этой причине бот выключен.\n\nПока что это все. Ждите новостей в ближайшее время."
    for userId in listOfUserIds:
        try:
            bot.send_message(chat_id=userId, text=text)
            print(f"successfully sent the message to user_id = {userId}")
        except:
            print(f"user_id = {userId} - blocked the bot")