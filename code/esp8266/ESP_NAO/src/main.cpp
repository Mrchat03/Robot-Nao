#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include <ESP8266WiFiMulti.h>
#include <PubSubClient.h>

// Prototype

void callback(char *topic, byte *payload, unsigned int length);
void connectToWifi(void);
void connectToMqtt(void);
void sendBroadcast(void);

WiFiUDP Udp;
WiFiClient espClient;
PubSubClient client(espClient);
ESP8266WiFiMulti wifi_multi;

unsigned timerUdpBroadcast = 0;
unsigned timerMQTT = 0;

// WiFi 1
const char *ssid1 = "tge_sansfil_270"; // Enter your WiFi name
const char *password = "sherbrooke";   // Enter WiFi password

// WiFi 2
const char *ssid2 = "tge_sansfil_228";

// MQTT Broker
const char *mqtt_broker = "10.240.3.178";
const char *topic = "zbos/dialog/set";
const char *mqtt_username = "emqx";
const char *mqtt_password = "public";
const int mqtt_port = 1883;

uint16_t connectTimeOutPerAP = 5000; // Defines the TimeOut(ms) for each AP to connect

unsigned int localUdpPort = 4210; // local port to listen on
char incomingPacket[255];         // buffer for incoming packets

void setup()
{
  // Set software serial baud to 115200;
  Serial.begin(115200);
  // connecting to a WiFi network

  connectToWifi();

  // Print ESP8266 Local IP Address
  Udp.begin(localUdpPort);
  Serial.printf("Now listening at IP %s, UDP port %d\n", WiFi.localIP().toString().c_str(), localUdpPort);
}

void connectToWifi(void)
{
  wifi_multi.addAP(ssid1, password);
  wifi_multi.addAP(ssid2, password);

  Serial.print("Connecting to Wi-Fi...");
  while (wifi_multi.run(connectTimeOutPerAP) != WL_CONNECTED)
  {
    Serial.print(".");
    delay(500);
  }
  Serial.println();
  Serial.print("Connected to ");
  Serial.println(WiFi.SSID());
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());
}

void connectToMqtt(void)
{
  // connecting to a mqtt broker
  client.setServer(mqtt_broker, mqtt_port);
  client.setCallback(callback);
  if (!client.connected() && (millis() - timerMQTT > 10000) )
  {
    String client_id = "esp8266-client-";
    client_id += String(WiFi.macAddress());
    Serial.printf("The client %s connects to the NAO mqtt broker\n", client_id.c_str());
    if (client.connect(client_id.c_str())) /*, mqtt_username, mqtt_password))*/
    {
      Serial.println("ZORA MQTT connected");
    }
    else
    {
      Serial.print("failed with state");
      Serial.println(client.state());
    }
    timerMQTT = millis();
  }
}

void callback(char *topic, byte *payload, unsigned int length)
{
  Serial.print("Message arrived in topic: ");
  Serial.println(topic);
  Serial.print("Message:");
  for (int i = 0; i < length; i++)
  {
    Serial.print((char)payload[i]);
  }
  Serial.println();
  Serial.println("-----------------------");
}

void sendBroadcast(void)
{
  if (millis() - timerUdpBroadcast > 5000)
  {

    // Send a broadcast message to the local network
    Udp.beginPacketMulticast(WiFi.broadcastIP(), localUdpPort, WiFi.localIP());
    Udp.write(WiFi.macAddress().c_str());
    Udp.endPacket();
    timerUdpBroadcast = millis();
  }
}

void loop()
{
  int packetSize = Udp.parsePacket();
  if (packetSize)
  {
    // receive incoming UDP packets
    Serial.printf("Received %d bytes from %s, port %d\n", packetSize, Udp.remoteIP().toString().c_str(), Udp.remotePort());
    int len = Udp.read(incomingPacket, 255);
    if (len > 0)
    {
      incomingPacket[len] = 0;
    }
    Serial.printf("UDP packet contents: %s\n", incomingPacket);
  }

  connectToMqtt();
  sendBroadcast();

}