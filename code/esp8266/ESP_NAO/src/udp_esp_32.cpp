#include <WiFiUdp.h>
#include "udp_esp_32.h"

extern ESP8266WiFiClass WiFi;

bool UdpEsp32::beginUdp()
{
    if (WiFiUDP::begin(getPort()))
    {
        Serial.printf("UDP écoute sur l'IP %s et sur le port %d\n", localIP().toString().c_str(), getPort());
        return true;
    }
    else
    {
        Serial.printf("UDP n'a pas réussi à se connecter sur le port %d\n", getPort());
        return false;
    }
}

IPAddress UdpEsp32::broadcastIP(void)
{
    return WiFi.broadcastIP();
}

IPAddress UdpEsp32::localIP(void)
{
    return WiFi.localIP();
}

String UdpEsp32::macAddress(void)
{
    return WiFi.macAddress();
}

bool UdpEsp32::readTrame(void)
{
    int packetSize = parsePacket();
    if (packetSize)
    {
        int len = WiFiUDP::read(udpTrame, BUFFER_SIZE);
        Serial.printf("UDP reçu %d octets de %s sur le port %d\n", len, remoteIP().toString().c_str(), remotePort());
        if (len)
        {
            udpTrame[len] = 0;
            Serial.printf("Le message reçu est : %s\n", udpTrame);

            return true;
        }
    }

    return false;
}

void UdpEsp32::sendBroadcast(void)
{
    if (millis() - timerUdpBroadcast > 5000UL)
    {
        // Send a broadcast message to the local network
        beginPacketMulticast(broadcastIP(), localUdpPort, localIP());
        write(broadcastTrame);
        endPacket();
        timerUdpBroadcast = millis();
    }
}

String UdpEsp32::SSID(void)
{
    return WiFi.SSID();
}