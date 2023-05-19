import json
import random


def create_answer_options():
    with open("dictionary.json", "r", encoding="utf-8") as file:
        dictionary = json.load(file)
    dictionary.sort(key=lambda x: x['degree'])
    #using lambda 
    return random.sample(dictionary, 4)


def add_word_to_dt(cur_text):
    with open("dictionary.json", "r", encoding="utf-8") as file:
            dictionary = json.load(file)

    arr = cur_text.split(';')
    for x in arr:
        if x.find('-') == -1:
            continue

        new_key, new_meaning = x.split('-', 1)

        new_key = new_key.replace('\n', '')
        new_key = new_key.lower()

        f = 1
        for word in dictionary:
            if word['word'] == new_key:
                f = 0
                break

        #print(new_key, new_meaning, f)

        if f == 1:
            print("Добавил слово")
            dictionary.append({'word': new_key, 'translation': new_meaning, 'degree': 0})

    with open("dictionary.json", "w") as file:
        json.dump(dictionary, file, indent=4)

