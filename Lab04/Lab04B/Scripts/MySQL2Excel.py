import mysql.connector
from mysql.connector import Error
import json
from datetime import datetime
from Config import HOST_IP, USER, PASSWORD, GROUP_NAME, DEVICE_ID



connection = mysql.connector.connect(host=HOST_IP,
                                            user=USER,
                                            password=PASSWORD,
                                            database=GROUP_NAME)
try:
    cursor = connection.cursor()  
    cursor.execute(f"""SELECT * FROM `{GROUP_NAME}`.`{DEVICE_ID}`; """)
    table = cursor.fetchall()
    now = datetime.now()
    f = open(f'{GROUP_NAME}_{DEVICE_ID}_{now.strftime("%Y-%m-%d_%H-%M-%S")}.csv', 'w')
    for row in table:
        print(f"{row[1]}, {row[2]}, {row[3]}", file=f)

    f.close()
    cursor.close() 
    connection.commit()
    connection.close()

except Error as e:
    print(f"ERROR: MQTT - / - > `{GROUP_NAME}`.`{DEVICE_ID}`", e)