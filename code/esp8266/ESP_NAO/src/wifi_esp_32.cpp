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

// WIFI 4
const char *ssid4 = "OnePlus 6";

const char *password = "sherbrooke"; // Enter WiFi password
const char *password2 = "cegep.666";

void connectToWifi(void)
{
  // wifi_multi.addAP(ssid1, password);
  // wifi_multi.addAP(ssid2, password);
  wifi_multi.addAP(ssid3, password);
  // wifi_multi.addAP(ssid4, password2);

  Serial.print("Connexion aux Wi-Fi ...");
  while (wifi_multi.run(connectTimeOutPerAP) != WL_CONNECTED)
  {
    Serial.print(".");
  }
  Serial.println();
  Serial.print("Connected to " + udpEsp32.SSID() + " with IP address: " + udpEsp32.localIP().toString() + "\n");
}
