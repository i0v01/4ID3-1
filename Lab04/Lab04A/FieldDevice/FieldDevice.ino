#include "FieldDevice.h"

void setup() {
    loraSerial.begin(57600);

  debugSerial.println("-- JOIN");
  ttn.join(appEui, appKey);

  debugSerial.begin(9600);
  
  while (!debugSerial) {}
  
  debugSerial.println("-- STATUS");
  ttn.showStatus();
  
  sensor_t sensor;
  dht.temperature().getSensor(&sensor);
  dht.humidity().getSensor(&sensor);

  Serial.println("\n\n--------------------------------------\n\n      The Things Uno\n      "
              + String(GROUP_NAME) + " - " + String(DEVICE_ID) 
              + "\n\n--------------------------------------\n\n");

}

void loop() {
   
  if(millis() - startTime > DELAY_BETWEEN_SAMPLES_MS){
    sensors_event_t event, dhtHumEvent;
    
    dht.temperature().getEvent(&event);
    delay(200);
    float temp = round(event.temperature * 10) / 10.0;
    dht.humidity().getEvent(&event);
    delay(200);
    float hum = round(event.relative_humidity * 10) / 10.0;
    //delay(1000);
    temp = random(19.2, 26.3);
    hum = random(500, 598);
    if(!isnan(temp) and !isnan(hum)){
      
      String msg = "{ \"" + String(GROUP_NAME) +  "\": { \"" + String(DEVICE_ID) 
                  + "\": { \"Temperature\": " + String(temp) 
                  + " , \"Humidity\": " + String(hum) + " } } }";
      debugSerial.println(msg);
      
      char msgData[msg.length()];
      for(int i = 0; i < msg.length(); i++){
        msgData[i] = msg[i];
      }

      ttn.sendBytes(msgData, sizeof(msgData));
    }
    
    else{
      debugSerial.println("Unable to read sensor");
    }
    
    startTime = millis();  
  }

}
