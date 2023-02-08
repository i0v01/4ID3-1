//Libraries
#include "EBYTE.h"
#include <HardwareSerial.h>

//Pin defines
#define PIN_RX 16   // Serial2 RX -> EBYTE TX
#define PIN_TX 17   // Serial2 TX pin -> EBYTE RX
#define PIN_M0 27 
#define PIN_M1 26
#define PIN_AX 25

#define TIME_PER_SEND_MS 3000

//Transceiver setup
#define TRANSCEIVER_CHANNEL 42
EBYTE Transceiver(&Serial2, PIN_M0, PIN_M1, PIN_AX);

//Device details
String GROUP_NAME = "GroupA";
String DEVICE_ID = "Device5";
