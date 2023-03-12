from digi.xbee.devices import XBeeDevice
from digi.xbee.io import IOLine, IOMode
import paho.mqtt.client as mqtt
import mysql.connector
from mysql.connector import Error
from datetime import datetime



#------------------------------------
#       CONFIGURATIONS
#------------------------------------

#   Database Connection
HOST_IP = "localhost"
USER = "root"
PASSWORD = "9055259140"

#   MQTT Connection
MQTT_IP = 'test.mosquitto.org'
MQTT_PORT = 1883
GROUP_NAME = "GroupA"
DEVICE_ID = "DeviceA"

#   Device Connection
PORT = "COM12"
BAUD_RATE = 9600
REMOTE_NODE_ID = "ROUTER"
IO_SAMPLING_RATE = 5  # 5 seconds.






#------------------------------------
#       CONNECTIONS
#------------------------------------

#   IO initialization
io = dict({
    "UserButton": {
        "IO": IOLine.DIO4_AD4,
        "Prev": None,
        "Curr": None,
        "Type": "DIO"
    },
    "Potentiometer": {
        "IO": IOLine.DIO2_AD2,
        "Prev": None,
        "Curr": None,
        "Type": "AIO"
    },
    "Photoresistor": {
        "IO": IOLine.DIO3_AD3,
        "Prev": None,
        "Curr": None,
        "Type": "AIO"
    }
})

class IOWrapper:

    def __init__(self, profile: dict):
        self._profile = profile

    def __repr__(self):
        for sensor in self._profile.keys():
            print("Sensor: \{")
            for key, value in sensor.items():
                print(f"{key}: {value}\n")

        print("}\n")

    def sensor(self, sensor: str):
        return self._profile[sensor]
    
    def get(self):
        return self._profile

    def parse(self, data: str):
        for d in range(str(data).count('[')):
            key = list(self._profile.keys())[d]
            sensor = self._profile[key]
            s = str(sensor["IO"])
            start = str(data).index(s)
            end = str(data).index(']', start)
            parsed = str(data)[start + len(s) + 2 : end]
            
            if(sensor["Type"] == "DIO"):
                sensor["Prev"] = sensor["Curr"]
                sensor["Curr"] = parsed[8:]
            
            elif(sensor["Type"] == "AIO"):
                sensor["Prev"] = sensor["Curr"]
                sensor["Curr"] = parsed
        
        return self._profile

sman = IOWrapper(io)



try:
    print("---\nDatabase reset:")
    connection = mysql.connector.connect(host=HOST_IP,
                                         user=USER,
                                         password=PASSWORD)
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("    > Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
        cursor.execute(f"DROP DATABASE `{GROUP_NAME}`")
        print("    > Database dropped successfully")
        cursor.close() 
        connection.commit()
        cursor = connection.cursor()
        cursor.execute(f"CREATE SCHEMA IF NOT EXISTS `{GROUP_NAME}` DEFAULT CHARACTER SET utf8;")
        cursor.close() 
        connection.commit()
        print("     > Created Database")
        cursor = connection.cursor()
        cursor.execute(f"DROP TABLE IF EXISTS `{GROUP_NAME}`.`{DEVICE_ID}`;")
        cursor.close()
        connection.commit() 
        print(f"    > Dropped table {DEVICE_ID}")
        cursor = connection.cursor()
        cursor.execute(f"""CREATE TABLE IF NOT EXISTS `{GROUP_NAME}`.`{DEVICE_ID}`
                    (`id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
                    `Time` VARCHAR(45) NOT NULL,
                    `Sensor` VARCHAR(45) NOT NULL,
                    `Value` VARCHAR(45) NOT NULL,
                    PRIMARY KEY (`id`),
                    UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE)
                    ENGINE = InnoDB;
                    SET SQL_MODE=@OLD_SQL_MODE;
                    SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
                    SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS; """)

        print("     > Created table")
        print(cursor.fetchall())
        cursor.close() 
        #connection.commit()
        connection.close()
        print("Database reset successful\n---\n\n")

except Error as e:
    print(f"!! - Failed to reset database: {e}\n---\n\n")


#   Instantiating MQTT and callback functions
def on_connect(client, userdata, flags, rc):
    print("Connected to  "+str(rc))

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    data = str(msg.payload.decode('utf-8'))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_IP, MQTT_PORT, 60)
client.subscribe('Light', 2)




 





#------------------------------------
#       MAIN METHOD
#------------------------------------

def main():
    print(" +----------------------------------------------+")
    print(" | XBee Python Library Handle IO Samples Sample |")
    print(" +----------------------------------------------+\n")

    device = XBeeDevice(PORT, BAUD_RATE)

    try:
        device.open()

        # Obtain the remote XBee device from the XBee network.
        xbee_network = device.get_network()
        remote_device = xbee_network.discover_device(REMOTE_NODE_ID)
        if remote_device is None:
            print("Could not find the remote device")
            exit(1)

        # Set the local device as destination address of the remote.
        remote_device.set_dest_address(device.get_64bit_addr())
        # Enable periodic sampling every IO_SAMPLING_RATE seconds in the remote device.
        remote_device.set_io_sampling_rate(IO_SAMPLING_RATE)


        for val in sman.get().values():
            if(val["Type"] == "DIO"):
                remote_device.set_io_configuration(val["IO"], IOMode.DIGITAL_IN)
                remote_device.set_dio_change_detection({val["IO"]})
            
            elif(val["Type"] == "AIO"):
                remote_device.set_io_configuration(val["IO"], IOMode.ADC)


        # Register a listener to handle the samples received by the local device.
        def io_samples_callback(sample, remote, time):
            print("New sample received from %s - %s" % (remote.get_64bit_addr(), sample))
            data = sman.parse(sample)
            
            print(data)
            now = datetime.now()
            for x in data.keys():
                print(f'{GROUP_NAME}/{DEVICE_ID}/{x}', str(data[x]["Curr"]).encode('utf-8'))
                try:
                    client.publish(f'{GROUP_NAME}/{DEVICE_ID}/{x}', str(data[x]["Curr"]).encode('utf-8'))
                except:
                    print("Failed to send to MQTT")

                try:
                    connection = mysql.connector.connect(host=HOST_IP,
                                            user=USER,
                                            password=PASSWORD,
                                            database=GROUP_NAME)
                    cursor = connection.cursor()
                    ts = now.strftime("%d/%m/%Y %H:%M:%S")
                    query = f"INSERT INTO `{GROUP_NAME}`.`{DEVICE_ID}` (`Time`, `Sensor`, `Value`) VALUES ('{str(ts)}', '{str(x)}', '{str(data[x]['Curr'])}'); "
                    print(query)
                    cursor.execute(query)
                    cursor.close()
                    connection.commit()
                    connection.close()
                except:
                    print("Failed to send to MySQL")
            
        
        device.add_io_sample_received_callback(io_samples_callback)

        input()

    finally:
        if device is not None and device.is_open():
            device.close()


if __name__ == '__main__':
    main()
