/// @file udp_esp32.cpp
/// @brief communication wifi
/// @author Nathanaël Amaridon
/// @date 2022-12-07
/// @version 1.0.0
/// @details


#include <ESP8266WiFiMulti.h>
#include "wifi_esp_32.h"
#include "udp_esp_32.h"

extern UdpEsp32 udpEsp32;
ESP8266WiFiMulti wifi_multi;

// Timer for connect to wifi
uint16_t connectTimeOutPerAP = 5000; // Defines the TimeOut(ms) for each AP to connect

// WiFi 1
const char *ssid1 = "tge_sansfil_270"; // Enter your WiFi name
// WiFi 2
const char *ssid2 = "tge_sansfil_228";

// WIFI 3
const char *ssid3 = "dlink";

const char *password = "sherbrooke"; // Enter WiFi password

/// @brief Connecte l'ESP32 à un réseau Wi-Fi
/// @param  
void connectToWifi(void)
{
  wifi_multi.addAP(ssid1, password);
  wifi_multi.addAP(ssid2, password);
  wifi_multi.addAP(ssid3, password);

  Serial.print("Connexion aux Wi-Fi ...");
  while (wifi_multi.run(connectTimeOutPerAP) != WL_CONNECTED)
  {
    Serial.print(".");
  }
  Serial.println();
  Serial.print("Connecté au réseau " + udpEsp32.SSID() + " avec l'adresse IP: " + udpEsp32.localIP().toString() + "\n");
}

/// @brief Défini un nouveau réseau Wi-Fi
/// @param ssid 
/// @param password 
void setNewWifi(const char *ssid, const char *password)
{
  // Supprime les anciens réseaux
  wifi_multi.cleanAPlist();
  // Ajoute le nouveau réseau
  wifi_multi.addAP(ssid, password);
  Serial.print("Connexion aux Wi-Fi ...");
  while (wifi_multi.run(connectTimeOutPerAP) != WL_CONNECTED)
  {
    Serial.print(".");
  }
  Serial.println();
  Serial.print("Connecté au réseau " + udpEsp32.SSID() + " avec l'adresse IP: " + udpEsp32.localIP().toString() + "\n");
  
  // Redémarre une nouvelle communication UDP
  udpEsp32.restartUDP();

}
