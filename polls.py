# file to work with polls

import db_interface
import random

# It should be const all the time. It is to know the number in the list of words for each part
part_to_num = {
    "adj": 0,
    "adv": 1,
    "noun": 2,
    "other": 4,
    "verb": 3
}

num_to_part = {
    0: "adj",
    1: "adv",
    2: "noun",
    3: "verb",
    4: "other",
}


class Poll:
    def __init__(self, options, correct_option_id, question, is_anonymous):
        self.options = options
        self.correct_option_id = correct_option_id
        self.question = question
        self.is_anonymous = is_anonymous

    def send(self, chat_id, bot):
        poll_message = bot.send_poll(chat_id=chat_id,
                                     options=self.options,
                                     correct_option_id=self.correct_option_id,
                                     type='quiz',
                                     question=self.question,
                                     is_anonymous=self.is_anonymous)
        return poll_message


# generates quiz when user types "/quiz"
def generate_quiz(dict_id='TEST'):
    dictionary = db_interface.get_words_by_dict_id(dict_id)
    part_number = random.randint(0, 4)

    answer_options = random.sample(dictionary[num_to_part[part_number]], 4)
    word_number = random.randint(0, 3)
    return word_number, answer_options


# Creates a poll
def create_poll(dict_id='TEST'):
    word_number, answer_options = generate_quiz(dict_id)
    for answer in answer_options:
        answer['word'] = answer['word'].capitalize()
        answer['translation'] = answer['translation'].capitalize()

    quiz_text = f"Как переводится слово: {answer_options[word_number]['word']}?\n"
    possible_answers = [answer['translation'] for answer in answer_options]

    poll = Poll(possible_answers, word_number, quiz_text, False)
    return poll


