import json
import mysql.connector
import random
import time  # was used to calculate the time
import datetime


# удаление словаря
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
        return "Добро пожаловать!"


# Получает все слова
def get_words():
    connection = connect_database()
    cursor = connection.cursor()

    # Выполнение SQL-запроса
    query = "SELECT dictionary FROM User_Dictionaries WHERE user_id = 955008318"
    cursor.execute(query)

    # Получение результатов
    cur_dictionary_json = cursor.fetchall()
    data = cur_dictionary_json[0][0]

    cursor.close()
    connection.close()

    # перенёс create_answer_options
    dictionary = json.loads(data)

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
    query = f"UPDATE User_Dictionaries SET Mailing = {int(new_value)} WHERE user_id = {current_user_id}"
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