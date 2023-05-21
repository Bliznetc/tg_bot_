import json
import random

import test


def create_answer_options():
    dictionary = test.get_words()
    dictionary.sort(key=lambda x: x['degree'])
    #using lambda
    return random.sample(dictionary, 4)


print(create_answer_options())


def add_word_to_dt(cur_text, user_id=745553839):
    arr = cur_text.split(';')
    for x in arr:
        if x.find('-') == -1:
            continue

        new_key, new_meaning = x.split('-', 1)

        new_key = new_key.replace('\n', '')
        new_key = new_key.lower()

        f = 1
        #for word in dictionary:
        #    if word['word'] == new_key:
        #        f = 0
        #        break

        #print(new_key, new_meaning, f)

        if f == 1:
            # print("Добавил слово")
            test.add_word_to_bd(new_key, new_meaning, user_id)
            # dictionary.append({'word': new_key, 'translation': new_meaning, 'degree': 0})

    #with open("dictionary.json", "w") as file:
    #    json.dump(dictionary, file, indent=4)

