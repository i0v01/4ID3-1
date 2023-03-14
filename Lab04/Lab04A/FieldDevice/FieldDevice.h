#include <TheThingsNetwork.h>
#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <DHT_U.h>

//  Macros
#define DHTPIN 2
#define DHTTYPE DHT11
#define DELAY_BETWEEN_SAMPLES_MS 5000
#define GROUP_NAME "GroupA"
#define DEVICE_ID "DeviceA"

DHT_Unified dht(DHTPIN, DHTTYPE);
#define loraSerial Serial1
#define debugSerial Serial

// Set your AppEUI and AppKey
#define freqPlan TTN_FP_US915
const char *appEui = "0000000000000000";
const char *appKey = "0F330CCBF3FA77D6AE1A5268EC51B7B7";
TheThingsNetwork ttn(loraSerial, debugSerial, freqPlan);

unsigned long startTime = millis();
