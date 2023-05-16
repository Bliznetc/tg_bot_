import json
import random


def create_answer_options():
    with open("dictionary.json", "r", encoding="utf-8") as file:
        dictionary = json.load(file)

    return random.sample(dictionary, 4)


def add_word_to_dt(cur_text):
    arr = cur_text.split(';')
    for x in arr:
        if (x.find('-') == -1):
            continue;

        new_key = x.split('-')[0]
        new_meaning = x.split('-')[1]

        with open("dictionary.json", "r", encoding="utf-8") as file:
            dictionary = json.load(file)

        dictionary.append({'word': new_key, 'translation': new_meaning})

        with open("dictionary.json", "w") as file:
            json.dump(dictionary, file, indent=4)
