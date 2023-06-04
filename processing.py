# Обработка текста со словами необходимо немного
# усовершенствовать эту функцию (неправильный ввод пользователей)
import spacy

nlp = spacy.load('pl_core_news_sm/pl_core_news_sm-3.5.0')


def prepare_text(text: str) -> list:
    arr = text.split(';')
    result = []
    for x in arr:
        if x.find('-') == -1:
            continue
        new_key, new_meaning = x.split('-', 1)
        new_key = new_key.replace('\n', '')
        new_key = new_key.lower()
        word_type = get_word_type(new_key)
        result.append((new_key, new_meaning, word_type))
    return result


def get_word_type (new_key) -> str:
    doc = nlp(new_key)
    word_type = doc[0].pos_
    word_type = word_type.lower()

    if word_type == 'noun' or word_type == 'adv' or word_type == 'adj' or word_type == 'verb':
        vari = 1
    else:
        word_type = 'other'

    return word_type