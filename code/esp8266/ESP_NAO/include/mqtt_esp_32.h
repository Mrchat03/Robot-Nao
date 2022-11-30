 #pragma once

#ifndef MQTT_ESP_32_H
#define MQTT_ESP_32_H


#include <PubSubClient.h>

#define MAX_REQUEST 5

struct DataMqtt
{
    String m_topic;
    String m_payload;
};



class MqttEsp32
{

private:
    // MQTT Broker
    const char *mqtt_broker = "10.240.8.169";
    const char *mqtt_username = "emqx";
    const char *mqtt_password = "public";
    const int mqtt_port = 1883;
    unsigned long timerMQTT = 0;
    int m_numberAnimation = 1;
    DataMqtt m_dataMqtt[MAX_REQUEST];


public:
    void connectToMqtt(void);
    bool splitTrame(String trame);
    char *getTopic(int pos) { return (char *)m_dataMqtt[pos].m_topic.c_str(); };
    char *getPayload(int pos) { return (char *)m_dataMqtt[pos].m_payload.c_str(); };
    int getNumberAnimation() { return m_numberAnimation; };
    bool subscribe(const char *topic);
    bool unsubscribe(const char *topic);
    bool loopMQTT(void);
    bool publish(const char* topic, const char* payload);
}; // class MqttEsp32

#endif // !MQTT_ESP_32_H
