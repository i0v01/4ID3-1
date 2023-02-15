import mysql.connector
from mysql.connector import Error
import json
import paho.mqtt.client as mqtt
import time

MQTT_HOSTNAME = "nam1.cloud.thethings.network"
MQTT_USERNAME = "4id3-groupa-2023@ttn"
MQTT_API_KEY = "NNSXS.4HQUZ7PDGYE5I7TEVSQ55PPXLTHNE6XDQ7HOYCI.FCFY3QFBBCF5W4AAGI2IWSJQY2XNDVZSLBZIPSVSKAU6ETA24TNA"
MQTT_PORT = 1883
MQTT_TOPIC = "#"


HOST_IP = "localhost"
USER = "root"
PASSWORD = "fireball"
DB_NAME = "iot"
TABLE_NAME = "data"


print(f'\n-------\nCONFIGURATION\n-------\nIP: {MQTT_HOSTNAME}\nPORT: {MQTT_PORT}\nTOPIC: {MQTT_TOPIC}\n')

def on_connect(client, userdata, flags, rc):
    print("Connected to  "+str(rc))

def on_message(client, userdata, msg):
    #print(msg.topic+" "+str(msg.payload))
    payload = json.loads(str(msg.payload.decode('utf-8')))
    #print(payload)
    try:
        deviceId  = payload["end_device_ids"]["device_id"]
        name = list(payload["uplink_message"]["decoded_payload"]["Sensors"].keys())[0]
        valKey = list(payload["uplink_message"]["decoded_payload"]["Sensors"].keys())[0]
        val = payload["uplink_message"]["decoded_payload"]["Sensors"][valKey]
        
        connection = mysql.connector.connect(host=HOST_IP,
                                                user=USER,
                                                password=PASSWORD,
                                                database=DB_NAME)
        cursor = connection.cursor()  
        cursor.execute(f"""INSERT INTO `{TABLE_NAME}` (`DeviceName`, `SensorName`, `SensorValue`) VALUES ('{deviceId}', '{name}', '{str(val)}'); """)
        print(f"['{deviceId}', '{name}', '{str(val)}' ] MQTT -> MySQL ( `{DB_NAME}`.`{TABLE_NAME}` )")
        res = cursor.fetchall()
        print(f"Response from MySQL: {res}\n\n")
        cursor.close() 
        connection.commit()
        connection.close()
    except Error as e:
        print(f"ERROR: MQTT - / - > `{DB_NAME}`.`{TABLE_NAME}`", e)

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