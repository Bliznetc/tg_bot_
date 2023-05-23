#Обработка текста со словами необходимо немного
#усовершентсвовать эту функцию (неправильный ввод пользователей)
def prepare_text(text: str) -> list:
    arr = text.split(';')
    result = []
    for x in arr:
        if x.find('-') == -1:
            continue
        new_key, new_meaning = x.split('-', 1)
        new_key = new_key.replace('\n', '')
        new_key = new_key.lower()
        result.append((new_key,new_meaning))
    return result



            

