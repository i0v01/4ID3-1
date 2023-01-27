#
#   Simple IoT Server 
#   Adam Sokacz
#   2023 - 01 - 26
#

#   Libraries
from http.server import HTTPServer, BaseHTTPRequestHandler
import time
import json
import pymongo
import paho.mqtt.client as mqtt


#   HTTP Server
HTTP_IP = 'localhost'
HTTP_PORT = 9000

#   MQTT Connection
MQTT_IP = 'test.mosquitto.org'
MQTT_PORT = 1883
MQTT_ROUTE = '/'

#   Database Connection
MONGODB_IP = "mongodb://localhost"
MONGODB_PORT = 27017
MONGODB_ROUTE = '/'

LIGHT = 'OFF'

#   Instantiating MQTT and callback functions
def on_connect(client, userdata, flags, rc):
    print("Connected to  "+str(rc))

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    data = str(msg.payload.decode('utf-8'))

    if data.strip() == "{\"Light\":\"ON\"}":
        LIGHT = "ON"
    elif data.strip() == "{\"Light\":\"OFF\"}":
        LIGHT = "OFF"


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_IP, MQTT_PORT, 60)
client.subscribe('Light', 2)
#   Instantiating database connection
myclient = pymongo.MongoClient(f"{MONGODB_IP}:{MONGODB_PORT}{MONGODB_ROUTE}")


#   Handles when a device makes a POST or GET request to HTTP server
class requestHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        if self.path.endswith('/light'):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(f'{LIGHT}\n')

    def do_POST(self):
        if self.path.endswith('/database'):
            #Reading the data sent from microcontroller and formatting it
            content_length = int(self.headers['Content-Length'])
            data = self.rfile.read(content_length)
            self.send_response(200)
            self.end_headers()
            data = str(data)
            firstSplitIndex = data.find('{')
            secondSplitIndex = data.rfind('}')
            data = data[firstSplitIndex: secondSplitIndex+1]

            #Interpreting microcontroller data as JSON
            jDict = json.loads(data)
            groupName = list(jDict.keys())[0]
            deviceId = list(jDict[groupName])[0]
            mydb = myclient[groupName]
            mycollection = mydb[deviceId]

            #Inserting into database
            ret = mycollection.insert_one(jDict[groupName][deviceId])

            #Returning data + OK
            self.wfile.write(f'{data}\nOK\n'.encode())
            
        if self.path.endswith('/mqtt'):
            #Reading the data sent from microcontroller and formatting it
            content_length = int(self.headers['Content-Length'])
            data = self.rfile.read(content_length)
            self.send_response(200)
            self.end_headers()
            data = str(data)
            firstSplitIndex = data.find('{')
            secondSplitIndex = data.rfind('}')
            data = data[firstSplitIndex: secondSplitIndex+1]

            #Interpreting microcontroller data as JSON
            jDict = json.loads(data)
            groupName = list(jDict.keys())[0]
            deviceId = list(jDict[groupName])[0]
            
            #Publishing to MQTT
            for key, val in jDict[groupName][deviceId].items():
                client.publish(f'{groupName}/{deviceId}/{key}', val.encode("UTF-8"))
            
            #Returning data + OK
            self.wfile.write(f'{data}\n'.encode())
            self.wfile.write(b'OK\n')


def main():
    serverAddress = (HTTP_IP, HTTP_PORT)
    server = HTTPServer(serverAddress, requestHandler)
    print('\n\n---------------------\nSimple HTTP IoT Server\n---------------------\n\n')
    print(f'HTTP server running on {HTTP_IP} port {HTTP_PORT}')
    time.sleep(2.16)
    print('Routes active: \n   -> \\mqtt \n   -> \\database')
    print(f"Connecting to MQTT -> {MQTT_IP}:{MQTT_PORT}")
    time.sleep(1.12)
    print(f"Connecting to Database -> {MONGODB_IP}:{MONGODB_PORT}{MONGODB_ROUTE}")
    time.sleep(1.78)
    print("\n\nServer Ready\n")
    
    server.serve_forever()

if __name__ == '__main__':
    main()




