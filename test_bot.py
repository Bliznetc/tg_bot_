import random
import telebot
from telebot import types
import datetime
import time
import constants as const

quiz_list = [
    {'word': 'cat', 'translation': 'кот'},
    {'word': 'dog', 'translation': 'собака'},
    {'word': 'apple', 'translation': 'яблоко'},
    # add more words and translations to the list
]

bot = telebot.TeleBot(f"{const.API_KEY}")

def generate_quiz():
    word = random.choice(quiz_list)
    answer_options = random.sample(quiz_list, 3)
    answer_options.append(word)
    random.shuffle(answer_options)
    return word, answer_options

@bot.message_handler(commands=['quiz'])
def send_quiz(message):
    word, answer_options = generate_quiz()
    quiz_text = f"What is the Russian translation of the word '{word['word']}'?\n\n"
    quiz_keyboard = types.InlineKeyboardMarkup()
    for answer_option in answer_options:
        quiz_keyboard.add(types.InlineKeyboardButton(answer_option['translation'], callback_data=str(answer_option == word)))
    bot.send_message(chat_id=message.chat.id, text=quiz_text, reply_markup=quiz_keyboard)

@bot.callback_query_handler(func=lambda call: True)
def check_quiz(call):
    is_correct = call.data == "True"
    if is_correct:
        message_text = "Correct answer!"
    else:
        message_text = "Sorry, that was incorrect."
    bot.answer_callback_query(callback_query_id=call.id, text=message_text)


print(__name__)

if __name__ == '__main__':
    bot.polling()
