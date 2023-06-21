import spacy
from googletrans import Translator
import time

polishSpacyLibrary = spacy.load('pl_core_news_sm/pl_core_news_sm-3.5.0')

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


def get_word_type(word: str) -> str:
    doc = polishSpacyLibrary(word)
    word_type = doc[0].pos_
    word_type = word_type.lower()
    
    if word_type != 'noun' and word_type != 'adv' and word_type != 'adj' and word_type != 'verb':
        word_type = 'other'
    
    return word_type

def translate_to_english(word, src_language):
    translator = Translator()
    translation = translator.translate(text=word, src=f"{src_language}", dest='en')
    print(translation.text)
    return translation.text

# if __name__=="__main__":
#     pass
