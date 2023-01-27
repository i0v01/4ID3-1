/*
  This example shows how to connect to an EBYTE transceiver
  using an ESP32
/*
  This example shows how to connect to an EBYTE transceiver
  using an ESP32
  This code for for the sender
  ESP32 won't allow SoftwareSerial (at least I can't get that lib to work
  so you will just hardwire your EBYTE directly to the Serial2 port
*/

#include "EBYTE.h"
#include "Lab03A.h"
#include <HardwareSerial.h>
/*
WARNING: IF USING AN ESP32
DO NOT USE THE PIN NUMBERS PRINTED ON THE BOARD
YOU MUST USE THE ACTUAL GPIO NUMBER
*/

EBYTE Transceiver(&Serial2, PIN_M0, PIN_M1, PIN_AX);

void setup() {

  Serial.begin(9600);
  Serial2.begin(9600);

  Transceiver.init();
  Transceiver.SetAirDataRate(AIR_DATA_RATE);
  Transceiver.SetMode(MODE_NORMAL);
  //Transceiver.SetTransmitPower(OPT_TP20);
  //Transceiver.SaveParameters(PERMANENT);
  Transceiver.PrintParameters();
  
  
}

unsigned long startTime = millis();

void loop() {
  
  if (Serial2.available() > 1) {
    Serial.println("Receving Data...");
    String incomingData = Serial2.readString();
    Serial.println("PING: " + incomingData);

  }

  if(millis() - startTime > TIME_PER_SEND_MS){
    Serial2.println(GROUP_NAME + " - " + DEVICE_ID);
    Serial.println("PONG SENT");
    startTime = millis();
  }

}
