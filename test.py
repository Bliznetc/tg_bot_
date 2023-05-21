import json
import mysql.connector

#удаление словаря
def delete_dictionary():
    with open("dictionary.json", "w") as file:
        json.dump([], file)

def connect_database():
    connection = mysql.connector.connect(
        host="containers-us-west-112.railway.app",
        user="root",
        password="QS8qQZtt5Ey4XhAcrhkz",
        database="railway",
        port="6633"
    )
    return connection

def store(user_id: int, access: str, dt: dict):
    connection = connect_database()
    cursor = connection.cursor()

    # Convert dictionary to JSON string
    json_data = json.dumps(dt)

    # Insert user data into the database
    query = "INSERT INTO User_Dictionaries (user_id, access, dictionary) VALUES (%s, %s, %s)"
    cursor.execute(query, (user_id, access, json_data))

    # Commit the changes and close the connection
    connection.commit()
    cursor.close()
    connection.close()


with open("dictionary.json", "r", encoding="utf-8") as file:
    data = json.load(file)

#store(955008318, "developer", data) #эта штука работает, твой словарь уже лежит на бд,
#осталось только сделать так для каждого нового chat_id и можно трахать

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