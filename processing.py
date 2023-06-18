# Обработка текста со словами необходимо немного
# усовершенствовать эту функцию (неправильный ввод пользователей)
import spacy
from googletrans import Translator

nlp = spacy.load('pl_core_news_sm/pl_core_news_sm-3.5.0')
nlp1 = spacy.load('en_core_web_sm/en_core_web_sm-3.5.0')


def prepare_text(text: str) -> list:
    arr = text.split(';')
    result = []
    for x in arr:
        if x.find('-') == -1:
            continue
        new_key, new_meaning = x.split('-', 1)
        new_key = new_key.replace('\n', '')
        new_key = new_key.lower()
        if new_key[-1] == ' ':
            new_key = new_key[0:len(new_key) - 1]

        if new_meaning[0] == ' ':
            new_meaning = new_meaning[1:len(new_meaning)]
        word_type = get_word_type(new_key)
        result.append((new_key, new_meaning, word_type))
    return result


def get_word_type(new_key) -> str:
    return get_word_type_en(translate_polish_to_english(new_key))
    # doc = nlp(new_key)
    # word_type = doc[0].pos_
    # word_type = word_type.lower()
    #
    # if word_type == 'noun' or word_type == 'adv' or word_type == 'adj' or word_type == 'verb':
    #     vari = 1
    # else:
    #     word_type = 'other'
    #
    # return word_type


def translate_polish_to_english(word):
    translator = Translator()
    translation = translator.translate(text=word, src='pl', dest='en')
    return translation.text


def get_word_type_en(new_key) -> str:
    doc = nlp1(new_key)
    word_type = doc[0].pos_
    word_type = word_type.lower()

    if word_type == 'noun' or word_type == 'adv' or word_type == 'adj' or word_type == 'verb':
        vari = 1
    else:
        word_type = 'other'

    return word_type

# print(get_word_type("labirynt"))

print(translate_polish_to_english("malina"))

# print("JEND")

# print(get_word_type_en(translate_polish_to_english("papryka")))
# print(prepare_text("niemiły - неприятный"))