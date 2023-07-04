
import json
import mysql.connector
import datetime
from datetime import datetime
import time
import processing

t = time.time()
try:
    connection_pool = mysql.connector.pooling.MySQLConnectionPool(
        pool_name="my_pool",
        pool_size=5,
        pool_reset_session=True,
        host="containers-us-west-112.railway.app",
        user="root",
        password="QS8qQZtt5Ey4XhAcrhkz",
        database="railway",
        port="6633"
    )
except mysql.connector.Error as e:
    print("Error while creating connection pool:", e)
print(time.time() - t, "takes to set up the connection")


# Adding a new record to the Table Users
def userRegistration(user_id: int, access: str = 'user', mailing: bool = 0, dict_id='TEST_ALL'):
    with connection_pool.get_connection() as connection:
        # check if user is already in the database
        if check_user_in(user_id):
            text = 'Вы уже зарегестрированы'
        else:  # adding user to the database
            with connection.cursor() as cursor:
                query = "INSERT INTO Users (user_id, access, mailing, dict_id) VALUES (%s, %s, %s, %s)"
                cursor.execute(query, (user_id, access, mailing, dict_id))
                connection.commit()
                text = 'Добро пожаловать!\nВоспользуйтесь меню или командой /help для того, чтобы просмотреть список доступных команд'
    return text


# checks if user is well-known
def check_user_in(user_id: int):
    listOfUserIds = get_user_ids()
    if user_id in listOfUserIds:
        return 1
    return 0


# returns a dictionary by user id, will be used in whole_dict_handler
def get_words_by_user_id(user_id: int):
    with connection_pool.get_connection() as connection:
        with connection.cursor() as cursor:
            query = "SELECT content FROM Users JOIN Dictionaries ON Users.dict_id = Dictionaries.dict_id WHERE Users.user_id = %s"
            cursor.execute(query, (user_id,))

            dictionary = json.loads(cursor.fetchall()[0][0])  # skipping a few steps
    return dictionary


# returns a dictionary by dict_id, can be used in other functions if needed
def get_words_by_dict_id(dict_id: str):
    with connection_pool.get_connection() as connection:
        with connection.cursor() as cursor:
            query = "SELECT content FROM Dictionaries WHERE dict_id = %s"
            cursor.execute(query, (dict_id,))

            dictionary = json.loads(cursor.fetchall()[0][0])
    return dictionary


# returns ALL WORDS FROM ALL DICTIONARIES, will be used only for the development process
def get_all_words():
    with connection_pool.get_connection() as connection:
        with connection.cursor() as cursor:
            query = "SELECT content FROM Dictionaries"
            cursor.execute(query)

            dividedDictionaries = [json.loads(i[0]) for i in cursor.fetchall()]
            bigDictionary = {k: [elem for d in dividedDictionaries for elem in d[k]] for k in
                             dividedDictionaries[0].keys()}  # python magic # это какой-то реальный мэджик
    return bigDictionary


# returns list of all dict_ids
def get_dict_ids():
    with connection_pool.get_connection() as connection:
        with connection.cursor() as cursor:
            query = "SELECT dict_id FROM Dictionaries"
            cursor.execute(query, )

            dictionary = cursor.fetchall()
            dict_ids = [row[0] for row in dictionary]
    return dict_ids


# creates a new record in table Dictionaries
def add_new_dictionary(new_dictionary: dict, dict_id: str):
    with connection_pool.get_connection() as connection:
        with connection.cursor() as cursor:
            query = "INSERT INTO Dictionaries (dict_id, content) VALUES (%s, %s)"
            cursor.execute(query, (dict_id, json.dumps(new_dictionary)))

            connection.commit()
    return f"Создан новый словарь {dict_id}"


# potentially functions below can be separated into different file
# returns access of a user by user_id
def get_user_access(user_id: int):
    with connection_pool.get_connection() as connection:
        with connection.cursor() as cursor:
            query = "SELECT access FROM Users WHERE user_id = %s"
            cursor.execute(query, (user_id,))

            resultOfQuery = cursor.fetchall()
            connection.commit()
    return resultOfQuery[0][0]


# returns dict_id of a user by user_id
def get_user_dict_id(user_id: int):
    with connection_pool.get_connection() as connection:
        with connection.cursor() as cursor:
            query = "SELECT dict_id FROM Users WHERE user_id = %s"
            cursor.execute(query, (user_id,))

            resultOfQuery = cursor.fetchall()
            connection.commit()
    return resultOfQuery[0][0]



# returns list of users' id
def get_user_ids():
    with connection_pool.get_connection() as connection:
        with connection.cursor() as cursor:
            query = "SELECT user_id FROM Users"
            cursor.execute(query)
            resultOfQuery = cursor.fetchall()
            connection.commit()

            listOfUserIds = list(map(lambda x: x[0], resultOfQuery))
    return listOfUserIds


# returns value of Mailing
def started_mailing(user_id: int):
    with connection_pool.get_connection() as connection:
        cursor = connection.cursor()

        query = f"SELECT Mailing FROM Users WHERE user_id = {user_id}"
        cursor.execute(query)

        cur_json = cursor.fetchall()
        cursor.close()
        return cur_json[0][0]


# updates value of Mailing
def update_mailing(user_id: int, new_value):
    with connection_pool.get_connection() as connection:
        cursor = connection.cursor()

        query = f"UPDATE Users SET Mailing = {int(new_value)}, sent_time = CURRENT_TIME() WHERE user_id = {user_id}"
        cursor.execute(query)

        connection.commit()
        print("Изменил значение Mailing")
        cursor.close()


# updates dict_id of a user
def update_dict_id(user_id: int, new_value: str):
    with connection_pool.get_connection() as connection:
        cursor = connection.cursor()

        print(new_value, user_id)
        query = "UPDATE Users SET dict_id = %s WHERE user_id = %s"
        cursor.execute(query, (new_value, user_id))

        connection.commit()
        print("Изменил значение dict_id")
        cursor.close()


# Returns list of users, whom we need to send a quiz to
def get_needed_users():
    with connection_pool.get_connection() as connection:
        cursor = connection.cursor()

        query = f"SELECT user_id, sent_time, Mailing FROM Users WHERE Mailing != 0"
        cursor.execute(query)

        result = cursor.fetchall()
        cur_list = []
        for a in result:
            cur_time = a[1]
            period = a[2]
            sent_h = cur_time.seconds // 3600
            sent_m = (cur_time.seconds // 60) % 60

            now = datetime.now()
            now_h = now.hour
            now_m = now.minute

            sent_allm = sent_h * 60 + sent_m
            now_allm = now_h * 60 + now_m
            if now_allm < sent_allm:
                now_allm += 1440
            if (now_allm - sent_allm) % period == 0:
                cur_list.append(a[0])

        print(cur_list)
        cursor.close()
        return cur_list


# Deletes a word from its dictionary
def delete_word_from_dict (query, word, translation, transcription, partOfSpeech, dict_id) -> list:
    with connection_pool.get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, (dict_id,))
            f = 0
            dictionary = json.loads(cursor.fetchall()[0][0])
            for cur_part in dictionary:
                for i in range(len(dictionary[cur_part])):
                    if dictionary[cur_part][i]['word'] == word:
                        if translation == "":
                            translation = dictionary[cur_part][i]['translation']
                        if transcription == "":
                            transcription = dictionary[cur_part][i]['transcription']
                        if partOfSpeech == "":
                            partOfSpeech = cur_part
                        del dictionary[cur_part][i]
                        f = 1
                        break

            cur = [translation, transcription, partOfSpeech]
            if f == 0:
                return ["Такое слово не найдено"]

            part_to_num = ["adj", "adv", "noun", "other", "verb"]

            if partOfSpeech not in part_to_num:
                return ["Такая часть речи не найдена"]

            content = json.dumps(dictionary)
            query = "UPDATE Dictionaries SET content = %s WHERE dict_id = %s"
            cursor.execute(query, (content, dict_id))

            connection.commit()
            return cur


# Adds a word to new dictionary
def add_word_to_dict (word, translation, transcription, partOfSpeech, Dictionary) -> str:
    with connection_pool.get_connection() as connection:
        with connection.cursor() as cursor:
            query = "SELECT content FROM Dictionaries WHERE dict_id = %s"
            cursor.execute(query, (Dictionary,))

            dictionary = json.loads(cursor.fetchall()[0][0])
            dictionary[partOfSpeech].append(
                {'word': word, 'degree': 0, 'translation': translation, 'transcription': transcription})

            print("Обновил словарь - " + word + " " + translation + " " + Dictionary)
            content = json.dumps(dictionary)
            query = "UPDATE Dictionaries SET content = %s WHERE dict_id = %s"
            cursor.execute(query, (content, Dictionary))

            connection.commit()
            return "Сделяль"


# Fixes bugs in the word
def fix_the_word(user_id: int, set_word: list):
    dict_id = get_user_dict_id(user_id=user_id)
    word = translation = transcription = partOfSpeech = Dictionary = ""

    if len(set_word) == 5:
        word, translation, transcription, partOfSpeech, Dictionary = set_word
    if len(set_word) == 2:
        word, Dictionary = set_word
    if len(set_word) == 3:
        word, partOfSpeech, Dictionary = set_word

    # Удаляем
    query = "SELECT content FROM Dictionaries WHERE dict_id = %s"
    cur = delete_word_from_dict(query, word, translation, transcription, partOfSpeech, dict_id)
    if len(cur) == 1:
        return cur[0]

    translation, transcription, partOfSpeech = cur

    # Добавляем
    text = add_word_to_dict(word, translation, transcription, partOfSpeech, Dictionary)

    return text





# не понятно, зачем
# менять!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Проверка на уникальность
# def check_in (new_key, dictionary):
#     f = 1
#     for word in dictionary:
#         if word['word'] == new_key:
#             f = 0
#             break
#     return f

