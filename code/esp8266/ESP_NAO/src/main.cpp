#include "wifi_esp_32.h"
#include "udp_esp_32.h"
#include "mqtt_esp_32.h"

UdpEsp32 udpEsp32;
MqttEsp32 mqttEsp32;

String subscribeMQTT = "";

void setup()
{
  // Set software serial baud to 115200;
  Serial.begin(115200);

  // LED
  pinMode(LED_BUILTIN, OUTPUT);

  // connecting to a WiFi network
  connectToWifi();

  // Print ESP8266 Local IP Address
  udpEsp32.beginUdp();
  digitalWrite(LED_BUILTIN, LOW); // turn the LED on (HIGH is the voltage level)
}

void loop()
{
  mqttEsp32.loopMQTT();

  if (udpEsp32.readTrame())
  {

    if (mqttEsp32.splitTrame(udpEsp32.getTrame()))
    {

      for (int i = 0; i < mqttEsp32.getNumberAnimation(); i++)
      {

        if (mqttEsp32.subscribe("zbos/motion/event"))
        {
          Serial.printf("Topic: %s \nPayload: %s\n", mqttEsp32.getTopic(i), mqttEsp32.getPayload(i));
          if (mqttEsp32.publish(mqttEsp32.getTopic(i), mqttEsp32.getPayload(i)))
          {
            //mqttEsp32.unsubscribe(subscribeMQTT.c_str());
          }
        }
      }
    }
  }
  mqttEsp32.connectToMqtt();

  udpEsp32.sendBroadcast();
}