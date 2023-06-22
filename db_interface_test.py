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


# It should be const all the time. It is to know the number in the list of words for each part
part_to_num = {
    "adj" : 0,
    "adv" : 1,
    "noun" : 2,
    "other" : 3,
    "verb" : 4
}

#done
# Добавляет пользователя в database
def store(user_id: int, access: str, mailing: bool):
    # t = time.time()
    with connection_pool.get_connection() as connection:
        cursor = connection.cursor()

        query_check = "SELECT user_id FROM Users"
        cursor.execute(query_check)
        data = [i[0] for i in cursor.fetchall()]

        if user_id in data:
            text = "Вы уже зарегестрированы"
        else:
            json_data = json.dumps([])
            print(user_id, access, json_data, mailing)
            # Insert user data into the database
            query = "INSERT INTO Users (user_id, access, dictionary, Mailing) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (user_id, access, json_data, mailing))
            # Commit the changes and close the connection
            connection.commit()
            text = "Добро пожаловать!"

        cursor.close()
        # print(time.time() - t)
        return text

#done
# Получает все слова, которые есть в бд
def get_words():
    # t = time.time()
    with connection_pool.get_connection() as connection:
        cursor = connection.cursor()
        # Выполнение SQL-запроса
        query = "SELECT dictionary FROM PartsOfSpeech"
        cursor.execute(query)

        # Получение результатов
        cur_dictionary_json = cursor.fetchall()

        dict_parts = [] # Словарь, разбитый по частям речи
        all_dict = [] # Полный словарь
        for i in cur_dictionary_json:
            dictionary = json.loads(i[0])
            dict_parts.append(dictionary)  # Объединение существующего списка с новым списком
            for word in dictionary:
                all_dict.append(word)

        cursor.close()

        # print(time.time() - t)
        return dict_parts, all_dict

#done
# Получает все слова, которые есть в словаре юзера
def get_words_by_user_id(id):
    # t = time.time()
    with connection_pool.get_connection() as connection:
        cursor = connection.cursor()
        # Выполнение SQL-запроса
        query = f"SELECT dictionary FROM Users WHERE user_id = {id}"
        cursor.execute(query)

        # Получение результатов
        cur_dictionary_json = cursor.fetchall()
        data = cur_dictionary_json[0][0]
        dictionary = json.loads(data)

        cursor.close()
        return dictionary

#менять!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Проверка на уникальность
def check_in (new_key, dictionary):
    f = 1
    for word in dictionary:
        if word['word'] == new_key:
            f = 0
            break
    return f


#ok$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# Возвращает значение Mailing
def started_mailing(current_user_id):
    with connection_pool.get_connection() as connection:
        cursor = connection.cursor()

        query = f"SELECT Mailing FROM Users WHERE user_id = {current_user_id}"
        cursor.execute(query)

        # Получение результатов
        cur_json = cursor.fetchall()
        cursor.close()
        return cur_json[0][0]

#ok$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# обновляет значение Mailing
def update_mailing(current_user_id, new_value):
    with connection_pool.get_connection() as connection:
        cursor = connection.cursor()

        # Выполнение SQL-запроса
        query = f"UPDATE Users SET Mailing = {int(new_value)}, sent_time = CURRENT_TIME() WHERE user_id = {current_user_id}"
        cursor.execute(query)

        connection.commit()

        # Выведите сообщение об успешном добавлении
        print("Изменил значение Mailing")

        cursor.close()

#ok$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# Возвращает список всех юзеров, которым нужно отправить квиз в текущий момент
def get_needed_users():
    with connection_pool.get_connection() as connection:
        cursor = connection.cursor()

        query = f"SELECT user_id, sent_time, Mailing FROM Users WHERE Mailing != 0"
        cursor.execute(query)

        result = cursor.fetchall()
        # print(result)

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

        # убрал
        print(cur_list)
        cursor.close()
        return cur_list

#done    
def get_user_ids():
    with connection_pool.get_connection() as connection:
        cursor = connection.cursor()

        query = "SELECT user_id FROM Users"
        cursor.execute(query)
        resultOfQuery = cursor.fetchall()
        
        listOfUserIds = list(map(lambda x: x[0], resultOfQuery))

        return listOfUserIds