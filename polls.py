# file to work with polls

import db_interface
import random

num_to_part = {
    0: "noun",
    1: "verb",
    2: "adj",
    3: "adv",
    4: "other"
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
def generate_quiz(dict_id='B1'):
    dictionary = db_interface.get_words_by_dict_id(dict_id)
    highest_number = 4
    if dict_id == 'ALL':
        highest_number = 2
    if dict_id == 'C1':
        highest_number = 3
    part_number = random.randint(0, highest_number)

    indexes_options = random.sample(range(0, len(dictionary[num_to_part[part_number]]['word'])), 4)
    answer_options = []
    for x in indexes_options:
        answer_options.append({
            "word": dictionary[num_to_part[part_number]]['word'][x],
            "trsl": dictionary[num_to_part[part_number]]['trsl'][x],
            "trsc": dictionary[num_to_part[part_number]]['trsc'][x],
        })
    word_number = random.randint(0, 3)
    return word_number, answer_options


# Creates a poll
def create_poll(dict_id='TEST_ALL'):
    word_number, answer_options = generate_quiz(dict_id)
    for answer in answer_options:
        answer['word'] = answer['word'].capitalize()
        answer['trsl'] = answer['trsl'].capitalize()

    quiz_text = f"Как переводится слово: {answer_options[word_number]['word']} [{answer_options[word_number]['trsc']}]?\n"
    possible_answers = [answer['trsl'] for answer in answer_options]
    return Poll(possible_answers, word_number, quiz_text, True)


