import json
import random

import db_interface


# def create_answer_options():
#     dictionary = db_interface.get_words()
#     dictionary.sort(key=lambda x: x['degree'])
#     #using lambda
#     return random.sample(dictionary, 4)


def add_word_to_dt(cur_text, user_id=745553839):
    arr = cur_text.split(';')
    for x in arr:
        if x.find('-') == -1:
            continue

        new_key, new_meaning = x.split('-', 1)

        new_key = new_key.replace('\n', '')
        new_key = new_key.lower()
        
        db_interface.add_word_to_bd(new_key, new_meaning, user_id)
            

