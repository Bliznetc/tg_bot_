import spacy
from googletrans import Translator
import time

polishSpacyLibrary = spacy.load('pl_core_news_sm/pl_core_news_sm-3.5.0')
englishSpacyLibrary = spacy.load('en_core_web_sm/en_core_web_sm-3.5.0')


def prepare_text(text: str) -> dict:
    arr = text.split(';')
    new_dictionary = {
        "noun": [],
        "verb": [],
        "adj": [],
        "adv": [],
        "other": []
    }
    for x in arr:
        if x.find('-') == -1:
            continue
        new_key, new_meaning = x.split('-', 1)
        new_key = new_key.replace('\n', '')
        new_key = new_key.lower()
        if new_key[-1] == ' ':
            new_key = new_key[:-1]
        if new_meaning[0] == ' ':
            new_meaning = new_meaning[1:]

        partOfSpeech = get_word_type(new_key)
        new_dictionary[partOfSpeech].append({"word": new_key, "degree": 0, "translation": new_meaning})   
    return new_dictionary


def get_word_type(word: str) -> str:
    doc = polishSpacyLibrary(word)
    word_type = doc[0].pos_
    word_type = word_type.lower()

    if word_type != 'noun' and word_type != 'adv' and word_type != 'adj' and word_type != 'verb':
        word_type = 'other'
    
    return word_type


def get_word_type_en(word: str) -> str:
    word = translate_to_english(word, "pl")
    doc = englishSpacyLibrary(word)
    word_type = doc[0].pos_
    word_type = word_type.lower()

    if word_type != 'noun' and word_type != 'adv' and word_type != 'adj' and word_type != 'verb':
        word_type = 'other'

    return word_type


def translate_to_english(word, src_language):
    translator = Translator()
    translation = translator.translate(text=word, src=f"{src_language}", dest='en')
    # print(translation.text)
    return translation.text
