import json
import mysql.connector
import datetime
from datetime import datetime
import time


def connect_database():
    connection = mysql.connector.connect(
        host="containers-us-west-112.railway.app",
        user="root",
        password="QS8qQZtt5Ey4XhAcrhkz",
        database="railway",
        port="6633"
    )
    return connection


# Добавляет пользователя в database
def store(user_id: int, access: str, mailing: bool):
    t = time.time()
    connection = connect_database()
    cursor = connection.cursor()

    # new_block
    query_check = "SELECT user_id FROM User_Dictionaries"
    cursor.execute(query_check)
    data = [i[0] for i in cursor.fetchall()]
    # print(data)

    if user_id in data:
        cursor.close()
        connection.close()
        print(time.time()-t, "регистрация пользователя")
        return "Вы уже зарегестрированы"
    else:
        json_data = json.dumps([])

        print(user_id, access, json_data, mailing)
        # Insert user data into the database
        query = "INSERT INTO User_Dictionaries (user_id, access, dictionary, Mailing) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (user_id, access, json_data, mailing))

        # Commit the changes and close the connection
        connection.commit()
        cursor.close()
        connection.close()
        print(time.time()-t, "регестрация пользователя")
        return "Добро пожаловать!"


# Получает все слова
def get_words():
    t = time.time()
    connection = connect_database()
    print(time.time()-t, "old connect")
    cursor = connection.cursor()
    print(time.time()-t, "old cursor")
    # Выполнение SQL-запроса
    query = "SELECT dictionary FROM User_Dictionaries WHERE user_id = 955008318"
    cursor.execute(query)
    print(time.time()-t, "old query")
    # Получение результатов
    cur_dictionary_json = cursor.fetchall()
    data = cur_dictionary_json[0][0]
    dictionary = json.loads(data)
    print(time.time()-t, "old data")

    cursor.close()
    print(time.time()-t, "old cursor")
    connection.close()

    print(time.time()-t, "old")
    return dictionary


# Добавляет список слов в database
def add_word_to_bd(arr: list, user_id: int):
    start_time = datetime.datetime.now()

    connection = connect_database()
    cursor = connection.cursor()

    new_dict = [{"word": item[0], "degree": 0, "translation": item[1]} for item in arr]

    query = "SELECT dictionary FROM User_Dictionaries WHERE user_id = %s"
    cursor.execute(query, (user_id,))
    existing_dict = cursor.fetchone()[0]  # Получение существующего списка словарей

    if existing_dict:
        merged_dict = json.loads(existing_dict)
        merged_dict.extend(new_dict)  # Объединение существующего списка с новым списком
    else:
        merged_dict = new_dict

    query = "UPDATE User_Dictionaries SET dictionary = %s WHERE user_id = %s"
    cursor.execute(query, (json.dumps(merged_dict), user_id))

    connection.commit()

    # Вывод сообщения об успешном добавлении
    print("Элементы успешно добавлены в ячейку базы данных.")

    cursor.close()
    connection.close()

    end_time = datetime.datetime.now()
    execution_time = end_time - start_time
    print("время выполнения ", execution_time.seconds)


# Возвращает значение Mailing
def started_mailing(current_user_id):
    connection = connect_database()
    cursor = connection.cursor()

    query = f"SELECT Mailing FROM User_Dictionaries WHERE user_id = {current_user_id}"
    cursor.execute(query)

    # Получение результатов
    cur_json = cursor.fetchall()
    return cur_json[0][0]


# обновляет значение Mailing
def update_mailing(current_user_id, new_value):
    connection = connect_database()
    cursor = connection.cursor()

    # Выполнение SQL-запроса
    query = f"UPDATE User_Dictionaries SET Mailing = {int(new_value)}, sent_time = CURRENT_TIME() WHERE user_id = {current_user_id}"
    cursor.execute(query)

    connection.commit()

    # Выведите сообщение об успешном добавлении
    print("Изменил значение Mailing")

    cursor.close()
    connection.close()


# Добавил проверку прямо в store()
# Проверяет, существует ли user с указанным id
def check_user_exists(user_id):
    connection = connect_database()
    cursor = connection.cursor()

    # Выполнение SQL-запроса
    query = f"SELECT COUNT(*) FROM User_Dictionaries WHERE user_id = {user_id}"
    cursor.execute(query)

    # Получение результата
    result = cursor.fetchone()[0]

    cursor.close()
    connection.close()
    if result == 0:
        return False
    else:
        return True


# Возвращает список всех юзеров, которым нужно отправить квиз в текущий момент
def get_needed_users():
    connection = connect_database()
    cursor = connection.cursor()

    query = f"SELECT user_id, sent_time, Mailing FROM User_Dictionaries WHERE Mailing != 0"
    cursor.execute(query)

    result = cursor.fetchall()
    print(result)

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

        print(now_allm, sent_allm, (now_allm - sent_allm), period)
        if (now_allm - sent_allm) % period == 0:
            cur_list.append(a[0])
        # print(sent_h, sent_m, cur_time, now_h, now_m)
    #убрал
    print(cur_list)
    return cur_list

