#include <TheThingsNetwork.h>

#define loraSerial Serial1
#define debugSerial Serial
#define freqPlan TTN_FP_US915

TheThingsNetwork ttn(loraSerial, debugSerial, freqPlan);

void setup(){
  loraSerial.begin(57600);
  debugSerial.begin(9600);
  
  while (!debugSerial) {}
  
  debugSerial.println("-- STATUS");
  ttn.showStatus();
}
void loop()
{
}
