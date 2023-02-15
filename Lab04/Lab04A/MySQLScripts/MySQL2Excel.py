import mysql.connector
from mysql.connector import Error
import json

HOST_IP = "localhost"
USER = "root"
PASSWORD = "fireball"
DB_NAME = "iot"
TABLE_NAME = "data"



connection = mysql.connector.connect(host=HOST_IP,
                                            user=USER,
                                            password=PASSWORD,
                                            database=DB_NAME)
try:
    cursor = connection.cursor()  
    cursor.execute(f"""SELECT * FROM `{DB_NAME}`.`{TABLE_NAME}`; """)
    table = cursor.fetchall()
    f = open(f'{DB_NAME}_{TABLE_NAME}.csv', 'w')
    for row in table:
        print(f"{row[1]}, {row[2]}, {row[3]}", file=f)

    f.close()
    cursor.close() 
    connection.commit()
    connection.close()

except Error as e:
    print(f"ERROR: MQTT - / - > `{DB_NAME}`.`{TABLE_NAME}`", e)