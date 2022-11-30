#include <PubSubClient.h>
#include <ESP8266WiFiMulti.h>
#include "udp_esp_32.h"
#include "mqtt_esp_32.h"

WiFiClient espClient;
PubSubClient client(espClient);
extern UdpEsp32 udpEsp32;

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

void MqttEsp32::connectToMqtt(void)
{
  // connecting to a mqtt broker
  client.setServer(mqtt_broker, mqtt_port);
  client.setCallback(callback);

  if ((millis() - timerMQTT > 10000UL) && !client.connected())
  {
    String client_id = "esp8266-client" + udpEsp32.macAddress();
    Serial.printf("The client %s connects to the NAO mqtt broker\n", client_id.c_str());
    if (client.connect(client_id.c_str())) /*, mqtt_username, mqtt_password))*/
    {
      Serial.println("Connecté à ZORA MQTT");
    }
    else
    {
      Serial.printf("failed with state %d\n", client.state());
    }
    
    timerMQTT = millis();
  }
}

bool MqttEsp32::loopMQTT(void)
{
  return client.loop();
}

bool MqttEsp32::publish(const char *topic, const char *payload)
{
  if (client.connected())
  {
    Serial.printf("Publishing to topic %s, payload %s\n", topic, payload);
    return client.publish(topic, payload);
  }
  else
  {
    Serial.println("Not connected to MQTT broker");
    return false;
  }
}

bool MqttEsp32::subscribe(const char *topic)
{

  Serial.printf("Subscribing to topic %s\n", topic);
  return client.subscribe(topic);
}

bool MqttEsp32::unsubscribe(const char *topic)
{
  Serial.printf("Unsubscribing to topic %s\n", topic);
  return client.unsubscribe(topic);
}

bool MqttEsp32::splitTrame(String trame)
{

  String m_buffer_request[MAX_REQUEST];

  int index_buffer = 0;
  int pos = 0;
  // Décomposition de la trame

  while (trame.indexOf('!') != -1)
  {
    m_buffer_request[index_buffer] = trame.substring(0, trame.indexOf('!'));
    trame = trame.substring(trame.indexOf('!') + 1);
    index_buffer++;
  }

  m_buffer_request[index_buffer] = trame;
  m_numberAnimation = index_buffer + 1;
  // décomposition de chaque requête
  for (int i = 0; i < m_numberAnimation; i++)
  {
    pos = m_buffer_request[i].indexOf('#');
    m_dataMqtt[i].m_topic = m_buffer_request[i].substring(0, pos);
    m_dataMqtt[i].m_payload = m_buffer_request[i].substring(pos + 1);
  }
  return true;
}