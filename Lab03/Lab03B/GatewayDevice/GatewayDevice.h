//Libraries
#include "EBYTE.h"
#include <WiFi.h>
#include <HTTPClient.h>
#include <HardwareSerial.h>

//Pin definitions
#define PIN_RX 16  
#define PIN_TX 17 
#define PIN_M0 27  
#define PIN_M1 26 
#define PIN_AX 25   

//Transceiver setup
enum eAirDataRate {
  BAUD300 = 0b000, 
  BAUD1200 = 0b001,
  BAUD2400 = 0b010,
  BAUD4800 = 0b011,
  BAUD9600 = 0b100,
  BAUD19200 = 0b101
};

const eAirDataRate AIR_DATA_RATE = BAUD300;
EBYTE Transceiver(&Serial2, PIN_M0, PIN_M1, PIN_AX);

//WiFi login credentials
const char* ssid = "GroupA";
const char* password = "12345678";

//HTTP server URL
//const char* serverName = "http://192.168.137.38:3000/mqtt";
const char* serverName = "http://192.168.137.38:3000/database";
