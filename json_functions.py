import json
import random

def create_answer_options():
    with open("dictionary.json", "r", encoding="utf-8") as file:
        dictionary = json.load(file)
    
    return random.sample(dictionary, 4)

def add_word_to_dt(message):
    new_key = message.text.split('-')[0]
    new_meaning = message.text.split('-')[1]

    with open("dictionary.json", "r", encoding="utf-8") as file:
        dictionary = json.load(file)

    dictionary.append({'word': new_key, 'translation': new_meaning})

    with open("dictionary.json", "w") as file:
        json.dump(dictionary, file, indent=4)
    
    

