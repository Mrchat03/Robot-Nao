#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include <ESP8266WiFiMulti.h>
#include <PubSubClient.h>
#include "main.h"

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
  if (!client.connected() && (millis() - timerMQTT > 10000))
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
  for (unsigned int i = 0; i < length; i++)
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

void splitTrame(char *trame, char c)
{
  int i = 0;
  int j = 0;
  bool split = false;
  while (trame[i] != '\0')
  {
    if (trame[i] == c)
    {
      dataMQTT.topic[j] = '\0';
      dataMQTT.sizeTopic = j;
      j = 0;
      split = true;
    }
    else
    {
      if (split == false)
      {
        dataMQTT.topic[j] = trame[i];
        j++;
      }
      else
      {
        dataMQTT.payload[j] = trame[i];
        j++;
      }
    }
    i++;
  }
  dataMQTT.payload[j] = '\0';
  dataMQTT.sizePayload = j;
}

void setup()
{
  // Set software serial baud to 115200;
  Serial.begin(115200);

  // LED
  pinMode(LED_BUILTIN, OUTPUT);

  // connecting to a WiFi network

  connectToWifi();

  // Print ESP8266 Local IP Address
  Udp.begin(localUdpPort);
  Serial.printf("Now listening at IP %s, UDP port %d\n", WiFi.localIP().toString().c_str(), localUdpPort);

  digitalWrite(LED_BUILTIN, LOW); // turn the LED on (HIGH is the voltage level)
}

void loop()
{

  client.loop();

  int packetSize = Udp.parsePacket();
  if (packetSize)
  {
    // receive incoming UDP packets
    Serial.printf("Received %d bytes from %s, port %d : ", packetSize, Udp.remoteIP().toString().c_str(), Udp.remotePort());
    int len = Udp.read(udpTrame, 512);

    if (len > 0)
    {
      udpTrame[len] = 0;
      splitTrame(udpTrame);
      Serial.println(udpTrame);
      if (dataMQTT.sizeTopic > 0 && dataMQTT.sizePayload > 0)
      {

        Serial.printf("Sending to MQTT topic %s, payload %s\n", dataMQTT.topic, dataMQTT.payload);
        Serial.println();
        client.publish(dataMQTT.topic, dataMQTT.payload);
      }
    }
  }

  connectToMqtt();
  sendBroadcast();
}