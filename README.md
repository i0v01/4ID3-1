# 4ID3
# ESP32 and ESP8266 Project Mind Map

## Project Overview

The project is divided into three main parts: BLE Scanning and Control for ESP32, WiFi and Server Communication for ESP8266, and Data Reception and Response for the Flask Server.

```mermaid
mindmap
  root((ESP32 and ESP8266 Project))
  
  %% ESP32 main functionality
  ESP32
    subnode((BLE Scanning & Control))
    subnode1[BLE Scanning]
      subnode1_1[Scan iBeacon UUID]
      subnode1_2[Get RSSI]
    subnode2[RSSI Checking]
      subnode2_1[Set Threshold]
      subnode2_2[Distance Calculation]
    subnode3[Servo Control]
      subnode3_1[Control Servo Activation]
      subnode3_2[Timed Deactivation]
    subnode4[Serial Data Transmission]
      subnode4_1[Send Activation Time]

  %% ESP8266 main functionality
  ESP8266
    subnode((WiFi and Server Communication))
    subnode1[WiFi Connection]
      subnode1_1[Connect to Specified Network]
    subnode2[Receive Activation Time]
      subnode2_1[Receive Data from ESP32 via Serial]
    subnode3[HTTP POST Request]
      subnode3_1[Send Activation Time to Flask Server]

  %% Flask Server main functionality
  Flask_Server
    subnode((Data Reception & Response))
    subnode1[Data Reception]
      subnode1_1[Receive Activation Time from ESP8266]
    subnode2[Data Logging]
      subnode2_1[Log Activation Time with Timestamp]
    subnode3[Send Success Response]
      subnode3_1[Return Success Message]
