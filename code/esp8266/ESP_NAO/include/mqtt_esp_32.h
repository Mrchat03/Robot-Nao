/// @file mqtt_esp32.h
/// @brief Gestion des requêtes MQTT
/// @author Nathanaël Amaridon 
/// @date 2022-12-07
/// @version 1.0.0
/// @details


#pragma once

#ifndef MQTT_ESP_32_H
#define MQTT_ESP_32_H


#include <PubSubClient.h>
#include <ArduinoJson.h>

#define MAX_REQUEST 5
const unsigned long TIMER_MQTT = 10000UL;

/// @brief Structure pour stocker les données MQTT
struct DataMqtt
{
    String m_topic;
    String m_payload;
    DataMqtt()
    {
        m_topic = "";
        m_payload = "";
    }
};


/// @brief Classe pour la communication MQTT
class MqttEsp32
{

private:
    // MQTT Broker
    String mqtt_broker = "10.240.8.169";
    const char *mqtt_username = "emqx";
    const char *mqtt_password = "public";
    const int mqtt_port = 1883;
    unsigned long timerMQTT = 0;
    int m_nbRequest = 0;
    DataMqtt m_dataMqtt[MAX_REQUEST];

public:
    void connectToMqtt(void);
    const char *getTopic(int pos);
    const char *getPayload(int pos);
    int getNbRequest(void) { return m_nbRequest; };
    const char* getBroker(void) { return mqtt_broker.c_str(); };
    void setNewBroker(String broker);
    void setNbRequest(int nbRequest);
    void setTopic(int pos, const char *topic);
    void setPayload(int pos, const char *payload);
    bool subscribe(const char *topic);
    bool unsubscribe(const char *topic);
    bool loopMQTT(void);
    bool publish(const char* topic, const char* payload);
}; // class MqttEsp32

#endif // !MQTT_ESP_32_H
