#pragma once

//******* Include *******//

#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include <ESP8266WiFiMulti.h>
#include <PubSubClient.h>

//******* Prototype *******//

void callback(char *topic, byte *payload, unsigned int length);
void connectToWifi(void);
void connectToMqtt(void);
void sendBroadcast(void);

void splitTrame(char *trame, char c = '#');

struct DataMQTT
{
  char topic[255];
  char payload[255];
  int sizeTopic;
  int sizePayload;
};



//******* Global variables *******//

WiFiUDP Udp;
WiFiClient espClient;
PubSubClient client(espClient);
ESP8266WiFiMulti wifi_multi;

// Timer 
unsigned timerUdpBroadcast = 0;
unsigned timerMQTT = 0;
uint16_t connectTimeOutPerAP = 5000; // Defines the TimeOut(ms) for each AP to connect

// WiFi 1
const char *ssid1 = "tge_sansfil_270"; // Enter your WiFi name
const char *password = "sherbrooke";   // Enter WiFi password

// WiFi 2
const char *ssid2 = "tge_sansfil_228";

// MQTT Broker
const char *mqtt_broker = "10.240.8.162";
const char *topic = "zbos/dialog/set";
const char *mqtt_username = "emqx";
const char *mqtt_password = "public";
const int mqtt_port = 1883;
DataMQTT dataMQTT;

unsigned int localUdpPort = 4210; // local port to listen on
char udpTrame[255];