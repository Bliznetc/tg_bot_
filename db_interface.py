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

def userRegistration(user_id: int, access: str = 'user', mailing: bool = 0, dict_id = 'TEST1'):
    with connection_pool.get_connection() as connection:
        #check if user is already in the database
        listOfUserIds = get_user_ids()
        if user_id in listOfUserIds:
            text = 'Вы уже зарегестрированы'
        else: #adding user to the database
            with connection.cursor() as cursor:
                query = "INSERT INTO Users (user_id, access, mailing, dict_id) VALUES (%s, %s, %s, %s)"
                cursor.execute(query, (user_id, access, mailing, dict_id))
                connection.commit()
                text = 'Добро пожаловать!\nВоспользуйтесь меню или командой /help для того, чтобы просмотреть список доступных команд'    
    return text

#returns a dictionary by user id, will be used in whole_dict_handler   
def get_words_by_user_id(user_id: int):
    with connection_pool.get_connection() as connection:
        with connection.cursor() as cursor:
            query = "SELECT content FROM Users JOIN Dictionaries ON Users.dict_id = Dictionaries.dict_id WHERE Users.user_id = %s"
            cursor.execute(query, (user_id,))

            dictionary = json.loads(cursor.fetchall()[0][0]) #skipping a few steps
    return dictionary

#returns a dictionary by dict_id, can be used in other functions if needed  
def get_words_by_dict_id(dict_id: str):
    with connection_pool.get_connection() as connection:
        with connection.cursor() as cursor:
            query = "SELECT content FROM Dictionaries WHERE dict_id = %s"
            cursor.execute(query, (dict_id,))

            dictionary = json.loads(cursor.fetchall()[0][0])
    return dictionary

#returns ALL WORDS FROM ALL DICTIONARIES, will be used only for the development process
def get_all_words():
    with connection_pool.get_connection() as connection:
        with connection.cursor() as cursor:
            query = "SELECT content FROM Dictionaries"
            cursor.execute(query)

            divededDictionaries = [json.loads(i[0]) for i in cursor.fetchall()]
            bigDictionary = {k: [elem for d in divededDictionaries for elem in d[k]] for k in divededDictionaries[0].keys()} #python magic    
    return bigDictionary

#creates a new record in table Dictionaries   
def add_new_dictionary(new_dictionary: dict, dict_id: str):
    with connection_pool.get_connection() as connection:
        with connection.cursor() as cursor:
            query = "INSERT INTO Dictionaries (dict_id, content) VALUES (%s, %s)"
            cursor.execute(query, (dict_id, json.dumps(new_dictionary)))
            
            connection.commit()
    return f"Создан новый словарь {dict_id}"


        
#potentially functions below can be separated into different file
def get_user_access(user_id: int):
    with connection_pool.get_connection() as connection:
        with connection.cursor() as cursor:
            query = "SELECT access FROM Users WHERE user_id = %s"
            cursor.execute(query, (user_id,))

            resultOfQuery = cursor.fetchall()
            connection.commit()    
    return resultOfQuery[0][0]


def get_user_ids():
    with connection_pool.get_connection() as connection:
        with connection.cursor() as cursor:
            query = "SELECT user_id FROM Users"
            cursor.execute(query)
            resultOfQuery = cursor.fetchall()
            connection.commit()

            listOfUserIds = list(map(lambda x: x[0], resultOfQuery))
    return listOfUserIds