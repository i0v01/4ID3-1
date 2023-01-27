
#define PIN_RX 16   // Serial2 RX (connect this to the EBYTE Tx pin)
#define PIN_TX 17   // Serial2 TX pin (connect this to the EBYTE Rx pin)

#define PIN_M0 27    // D4 on the board (possibly pin 24)
#define PIN_M1 26   // D2 on the board (possibly called pin 22)
#define PIN_AX 25   // D15 on the board (possibly called pin 21)

enum eAirDataRate {
  BAUD300 = 0b000, 
  BAUD1200 = 0b001,
  BAUD2400 = 0b010,
  BAUD4800 = 0b011,
  BAUD9600 = 0b100,
  BAUD19200 = 0b101
};

const eAirDataRate AIR_DATA_RATE = BAUD300;

String GROUP_NAME = "GroupA";
String DEVICE_ID = "Device6";

#define TIME_PER_SEND_MS 3000
