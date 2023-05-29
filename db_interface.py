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


# Добавляет пользовате
with connection_pool.get_connection() as connection:
    cursor = connection.cursor()

    query = f"SELECT access FROM User_Dictionaries WHERE user_id = 745553839"
    cursor.execute(query)

    # Получение результатов
    cur_json = cursor.fetchall()
    l = cur_json[0][0]
    cursor.close()
    print(l)