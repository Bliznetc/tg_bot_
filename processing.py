import spacy
import db_interface

polishSpacyLibrary = spacy.load('pl_core_news_sm/pl_core_news_sm-3.5.0')
# englishSpacyLibrary = spacy.load('en_core_web_sm/en_core_web_sm-3.5.0')


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


def check_uniqueness(word: str) -> bool:
    uniqueness = True
    dict_ids = db_interface.get_dict_ids()
    num_to_part = ["noun", "verb", "adj", "adv", "other"]
    for dict_id in dict_ids:
        if not uniqueness:
            break
        cur_dict = db_interface.get_words_by_dict_id(dict_id)
        for x in num_to_part:
            if not uniqueness:
                break
            for i in range(len(cur_dict[x]['word'])):
                if cur_dict[x]['word'][i].lower() == word.lower():
                    uniqueness = False
                    break
    return uniqueness

