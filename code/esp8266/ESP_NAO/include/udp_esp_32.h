#pragma once

#ifndef UDP_ESP_32_H
#define UDP_ESP_32_H

#include <ArduinoJson.h>
#include <WiFiUdp.h>
#include <ESP8266WiFi.h>
#define BUFFER_SIZE 512

const unsigned long TIMER_UDP = 5000UL;

/// @brief Classe pour la communication UDP
class UdpEsp32 : public WiFiUDP
{

private:
    const unsigned int localUdpPort = 4210; // local port to listen on
    const char *broadcastTrame = "allo le monde !";
    unsigned long timerUdpBroadcast = 0;
    char udpTrame[BUFFER_SIZE];

public:
    bool beginUdp();
    IPAddress broadcastIP(void);
    uint16_t getPort(void) { return localUdpPort; };
    String getTrame(void) { return udpTrame; };
    String macAddress(void);
    IPAddress localIP(void);
    bool readTrame(void);
    String SSID(void);

    void sendBroadcast(void);
};

#endif // !UDP
