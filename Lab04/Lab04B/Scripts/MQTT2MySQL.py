import mysql.connector
from mysql.connector import Error
import json
import paho.mqtt.client as mqtt
import time
from datetime import datetime
from Config import HOST_IP, USER, PASSWORD, GROUP_NAME, DEVICE_ID, MQTT_HOSTNAME, MQTT_API_KEY, MQTT_PORT, MQTT_TOPIC, MQTT_USERNAME



print(f'\n-------\nCONFIGURATION\n-------\nIP: {MQTT_HOSTNAME}\nPORT: {MQTT_PORT}\nTOPIC: {MQTT_TOPIC}\n')

def on_connect(client, userdata, flags, rc):
    print("Connected to  "+str(rc))

def on_message(client, userdata, msg):
    #print(msg.topic+" "+str(msg.payload))
    payload = json.loads(str(msg.payload.decode('utf-8')))
    #print(payload)
    try:
        deviceId  = payload["end_device_ids"]["device_id"]
        data = dict(payload["uplink_message"]["decoded_payload"][GROUP_NAME][DEVICE_ID])
        now = datetime.now()

        for sensor, reading in data.items():
            connection = mysql.connector.connect(host=HOST_IP,
                                                user=USER,
                                                password=PASSWORD,
                                                database=GROUP_NAME)
            cursor = connection.cursor()  
            cursor.execute(f"""INSERT INTO `{GROUP_NAME}`.`{DEVICE_ID}` (`Timestamp`, `Sensor`, `Reading`) VALUES ('{now.strftime("%Y-%m-%d %H:%M:%S")}', '{sensor}', '{str(reading)}'); """)
            print(f"['{now.strftime('%Y-%m-%d %H:%M:%S')}', '{sensor}', '{str(reading)}' ] MQTT -> MySQL ( `{GROUP_NAME}`.`{DEVICE_ID}` )")
            res = cursor.fetchall()
            print(f"Response from MySQL: {res}\n\n")
            cursor.close() 
            connection.commit()
            connection.close()


    except Error as e:
        print(f"ERROR: MQTT - / - > `{GROUP_NAME}`.`{DEVICE_ID}`", e)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
print("Connecting to MQTT")
for x in range(7):
    print(".")
    time.sleep(0.7)

client.username_pw_set(MQTT_USERNAME, MQTT_API_KEY)
client.connect(MQTT_HOSTNAME, port=MQTT_PORT)
client.subscribe("#")

client.loop_forever() 