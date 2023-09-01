import spacy
import time

polishSpacyLibrary = spacy.load('pl_core_news_sm/pl_core_news_sm-3.5.0')
englishSpacyLibrary = spacy.load('en_core_web_sm/en_core_web_sm-3.5.0')


def prepare_text(text: str) -> dict:
    arr = text.split(';')

    new_dictionary = {
        "noun": {
            "word": [],
            "trsl": [],
            "trsc": []
        },
        "verb": {
            "word": [],
            "trsl": [],
            "trsc": []
        },
        "adj": {
            "word": [],
            "trsl": [],
            "trsc": []
        },
        "adv": {
            "word": [],
            "trsl": [],
            "trsc": []
        },
        "other": {
            "word": [],
            "trsl": [],
            "trsc": []
        }
    }

    for x in arr:
        if x.find('-') == -1:
            continue
        new_key, new_meaning, new_trsc = x.split('-', 2)
        new_key = new_key.replace('\n', '')
        new_key = new_key.lower()
        if new_key[-1] == ' ':
            new_key = new_key[:-1]
        if new_meaning[0] == ' ':
            new_meaning = new_meaning[1:]

        partOfSpeech = get_word_type(new_key)
        new_dictionary[partOfSpeech]['word'].append(new_key)
        new_dictionary[partOfSpeech]['trsl'].append(new_meaning)
        new_dictionary[partOfSpeech]['trsc'].append(new_trsc)
    return new_dictionary


def get_word_type(word: str) -> str:
    doc = polishSpacyLibrary(word)
    word_type = doc[0].pos_
    word_type = word_type.lower()

    if word_type != 'noun' and word_type != 'adv' and word_type != 'adj' and word_type != 'verb':
        word_type = 'other'
    
    return word_type


# print(translate_to_english("piłka", "pl"))
