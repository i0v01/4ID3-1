//Libraries
#include <Arduino.h>
#include <Wire.h>
#include <AsyncAPDS9306.h>
#include "EBYTE.h"
#include <HardwareSerial.h>

//Pin definitions 
#define PIN_RX 16   
#define PIN_TX 17   
#define PIN_M0 27  
#define PIN_M1 26   
#define PIN_AX 25  

//Sample frequency
#define DELAY_BETWEEN_SAMPLES_MS 5000

//Datarate enumeration
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

//Device information
String groupName = "GroupA";
String deviceName = "DeviceA";

//Sensor IIC addresses
#define ADDR (byte)(0x40)
#define TMP_CMD (byte)(0xF3)

//Instantiating sensor object and configuration
AsyncAPDS9306 lightSensor;
const APDS9306_ALS_GAIN_t aGain = APDS9306_ALS_GAIN_1;
const APDS9306_ALS_MEAS_RES_t aTime = APDS9306_ALS_MEAS_RES_16BIT_25MS;
