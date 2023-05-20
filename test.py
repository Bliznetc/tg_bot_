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

store(955008318, "developer", data) #эта штука работает, твой словарь уже лежит на бд,
#осталось только сделать так для каждого нового chat_id и можно трахать 