import json
import mysql.connector


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

    # Здесь должен быть пустой список
    # empty_json = {}

    # Преобразование JSON-объекта в строку
    json_data = json.dumps([])

    # user_id = 745553838
    print(user_id, access, json_data, mailing)
    # Insert user data into the database
    query = "INSERT INTO User_Dictionaries (user_id, access, dictionary, Mailing) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (user_id, access, json_data, mailing))

    # Commit the changes and close the connection
    connection.commit()

    cursor.close()
    connection.close()


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

    # Преобразование строки JSON в список
    json_data = json.loads(data)

    cursor.close()
    connection.close()
    return json_data


# Добавляет слово в database
def add_word_to_bd(new_key, new_meaning, user_id):
    connection = connect_database()
    cursor = connection.cursor()

    # Выполнение SQL-запроса
    new_item = {
        "word": new_key,
        "degree": 0,
        "translation": new_meaning
    }

    query = "UPDATE User_Dictionaries SET dictionary = JSON_ARRAY_APPEND(dictionary, '$', CAST(%s AS JSON)) WHERE user_id = %s"
    cursor.execute(query, (json.dumps(new_item), user_id))

    connection.commit()

    # Выведите сообщение об успешном добавлении
    print("Элемент успешно добавлен в ячейку базы данных.")

    cursor.close()
    connection.close()


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


