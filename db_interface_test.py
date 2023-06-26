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
    "other" : 4,
    "verb" : 3
}





