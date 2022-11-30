#include <ESP8266WiFiMulti.h>
#include "wifi_esp_32.h"
#include "udp_esp_32.h"

extern UdpEsp32 udpEsp32;
ESP8266WiFiMulti wifi_multi;

// Timer for connect to wifi
uint16_t connectTimeOutPerAP = 5000; // Defines the TimeOut(ms) for each AP to connect

// WiFi 1
//const char *ssid1 = "tge_sansfil_270"; // Enter your WiFi name
const char *password = "sherbrooke";   // Enter WiFi password

// WiFi 2
const char *ssid2 = "tge_sansfil_228";

// WIFI 3
const char *ssid3 = "dlink";

void connectToWifi(void)
{
  wifi_multi.addAP(ssid3, password);
  wifi_multi.addAP(ssid2, password);

  Serial.print("Connexion aux Wi-Fi ...");
  while (wifi_multi.run(connectTimeOutPerAP) != WL_CONNECTED)
  {
    Serial.print(".");
  }
  Serial.println();
  Serial.print("Connected to " + udpEsp32.SSID() + " with IP address: " + udpEsp32.localIP().toString());
}
