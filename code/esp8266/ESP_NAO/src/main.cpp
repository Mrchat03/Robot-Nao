/// @file main.cpp
/// @brief Programme principal de la carte ESP32. Ce programme permet de recevoir 
///        des trames UDP et de les envoyer en MQTT.
/// @author Nathanaël Amaridon 
/// @date 2022-12-07
/// @version 1.0.0
/// @details


#include <ArduinoJson.h>
#include "json_esp_32.h"
#include "wifi_esp_32.h"
#include "udp_esp_32.h"
#include "mqtt_esp_32.h"

// Variable externe globale
extern UdpEsp32 udpEsp32;
extern MqttEsp32 mqttEsp32;
extern StaticJsonDocument<512> doc;

/// @brief Initialisation de la carte ESP32
void setup()
{
  // Set software serial baud to 115200;
  Serial.begin(115200);

  // LED
  pinMode(LED_BUILTIN, OUTPUT);

  // connecte au wifi
  connectToWifi();

  // Démarre le serveur UDP
  udpEsp32.beginUdp();
  digitalWrite(LED_BUILTIN, LOW); // turn the LED on (HIGH is the voltage level)
}

/// @brief 
void loop()
{
  mqttEsp32.loopMQTT();

  // Lecture de la trame UDP
  if (udpEsp32.readTrame())
  {
    // Lecture du JSON
    if (readJson())
    {
      if (mqttEsp32.getNbRequest() > 0)
      {
        // On lit le nombre de requete
        for (int i = 0; i < mqttEsp32.getNbRequest(); i++)
        {
          // On envoie les requetes
          mqttEsp32.publish(mqttEsp32.getTopic(i), mqttEsp32.getPayload(i));
        }
        // On remet le nombre de requete à 0
        mqttEsp32.setNbRequest(0);
      }
    }
  }
  // On se connecte au broker MQTT
  mqttEsp32.connectToMqtt();

 // On envoie un broadcast pour faire savoir qu'on est là
  udpEsp32.sendBroadcast();
}
