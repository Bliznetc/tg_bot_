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

def store(user_id: int, access: str = 'user', mailing: bool = 0, dict_id = 'TEST1'):
    with connection_pool.get_connection() as connection:
        #check if user is already in the database
        listOfUserIds = get_user_ids()
        if user_id in listOfUserIds:
            text = 'Вы уже зарегестрированы'
        else: #adding user to the database
            cursor = connection.cursor()
            query = "INSERT INTO Users (user_id, access, mailing, dict_id) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (user_id, access, mailing, dict_id))
            connection.commit()
            text = 'Добро пожаловать!\nВоспользуйтесь меню или командой /help для того, чтобы просмотреть список доступных команд'
            cursor.close()
        return text
    
def get_words(user_id: int):
    with connection_pool.get_connection() as connection:
        cursor = connection.cursor()
        query = "SELECT content FROM Users JOIN Dictionaries ON Users.dict_id = Dictionaries.dict_id WHERE Users.user_id = %s"
        cursor.execute(query, (user_id,))
        dictionary = json.loads(cursor.fetchall()[0][0]) #skipping a few steps
        return dictionary


def get_user_ids():
    with connection_pool.get_connection() as connection:
        cursor = connection.cursor()
        query = "SELECT user_id FROM Users"
        cursor.execute(query)
        resultOfQuery = cursor.fetchall()
        cursor.close()

        listOfUserIds = list(map(lambda x: x[0], resultOfQuery))
        return listOfUserIds