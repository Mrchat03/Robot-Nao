/// @file mqtt_esp32.cpp
/// @brief Gestion des requêtes MQTT
/// @author Nathanaël Amaridon 
/// @date 2022-12-07
/// @version 1.0.0
/// @details

#include <ArduinoJson.h>
#include <PubSubClient.h>
#include <ESP8266WiFiMulti.h>
#include "udp_esp_32.h"
#include "mqtt_esp_32.h"

// Variables globales
MqttEsp32 mqttEsp32;
WiFiClient espClient;
PubSubClient client(espClient);
extern UdpEsp32 udpEsp32;
extern StaticJsonDocument<512> doc;

/// @brief
/// @param topic
/// @param payload
/// @param length
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

/// @brief Connexion au broker MQTT et vérification de la connexion toutes les 5 secondes
/// @param
void MqttEsp32::connectToMqtt(void)
{

  if ((millis() - timerMQTT > TIMER_MQTT) && !client.connected())
  {

    // connecting to a mqtt broker
    client.setServer(mqtt_broker.c_str(), mqtt_port);
    client.setCallback(callback);

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

/// @brief Récupère le topic d'une requête MQTT
/// @param pos position de la requête dans le buffer
/// @return
const char *MqttEsp32::getTopic(int pos)
{
  return m_dataMqtt[pos].m_topic.c_str();
}

/// @brief Récupère le topic d'une requête MQTT
/// @param pos position de la requête dans le buffer
/// @return
const char *MqttEsp32::getPayload(int pos)
{
  return m_dataMqtt[pos].m_payload.c_str();
}

/// @brief
/// @param
/// @return
bool MqttEsp32::loopMQTT(void)
{
  return client.loop();
}

/// @brief Envoi d'un message MQTT
/// @param topic
/// @param payload
/// @return
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

/// @brief Affecte une nouvelle du broker MQTT
/// @param broker
void MqttEsp32::setNewBroker(String broker)
{
  mqtt_broker = broker;
  client.disconnect();
}

/// @brief Affecte le nombre de requête
void MqttEsp32::setNbRequest(int nbRequest)
{
  if (nbRequest > MAX_REQUEST)
    nbRequest = MAX_REQUEST;
  m_nbRequest = nbRequest;
}

/// @brief Affecte la valeur du topic
void MqttEsp32::setTopic(int pos, const char *topic)
{
  m_dataMqtt[pos].m_topic = topic;
}

/// @brief Affecte la valeur du payload
void MqttEsp32::setPayload(int pos, const char *payload)
{
  m_dataMqtt[pos].m_payload = payload;
}

/// @brief S'abonne d'un topic MQTT
/// @param topic
/// @return
bool MqttEsp32::subscribe(const char *topic)
{

  Serial.printf("Subscribing to topic %s\n", topic);
  return client.subscribe(topic);
}

/// @brief Se désabonne d'un topic MQTT
/// @param topic
/// @return
bool MqttEsp32::unsubscribe(const char *topic)
{
  Serial.printf("Unsubscribing to topic %s\n", topic);
  return client.unsubscribe(topic);
}
