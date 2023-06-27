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

def userRegistration(user_id: int, access: str = 'user', mailing: bool = 0, dict_id='TEST1'):
    with connection_pool.get_connection() as connection:
        # check if user is already in the database
        listOfUserIds = get_user_ids()
        if user_id in listOfUserIds:
            text = 'Вы уже зарегестрированы'
        else:  # adding user to the database
            with connection.cursor() as cursor:
                query = "INSERT INTO Users (user_id, access, mailing, dict_id) VALUES (%s, %s, %s, %s)"
                cursor.execute(query, (user_id, access, mailing, dict_id))
                connection.commit()
                text = 'Добро пожаловать!\nВоспользуйтесь меню или командой /help для того, чтобы просмотреть список доступных команд'
    return text


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
