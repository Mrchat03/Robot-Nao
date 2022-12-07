/// @file udp_esp32.cpp
/// @brief Communication UDP
/// @author Nathanaël Amaridon 
/// @date 2022-12-07
/// @version 1.0.0
/// @details

#include <WiFiUdp.h>
#include <ArduinoJson.h>
#include "udp_esp_32.h"

UdpEsp32 udpEsp32;
extern ESP8266WiFiClass WiFi;
extern StaticJsonDocument<512> doc;

/// @brief Commence une communication UDP
/// @param
/// @return
bool UdpEsp32::beginUdp(void)
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

/// @brief Retourne l'adresse IP de broadcast
/// @param
/// @return
IPAddress UdpEsp32::broadcastIP(void)
{
    return WiFi.broadcastIP();
}

/// @brief Retourne l'ip de l'appareil
/// @param
/// @return
IPAddress UdpEsp32::localIP(void)
{
    return WiFi.localIP();
}

/// @brief Retourne l'adresse MAC de l'appareil
/// @param
/// @return
String UdpEsp32::macAddress(void)
{
    return WiFi.macAddress();
}

/// @brief Lit la trame UDP et la retourne sous forme de JsonObject
/// @param
/// @return Un objet JSON
bool UdpEsp32::readTrame(void)
{
    DeserializationError err;
    // Si une trame UDP est reçue
    int packetSize = parsePacket();
    if (packetSize)
    {
        // Lecture de la trame UDP
        int len = WiFiUDP::read(udpTrame, BUFFER_SIZE);
        if (len)
        {
            udpTrame[len] = 0;

            Serial.printf("UDP reçu %d octets de %s sur le port %d\n", len, remoteIP().toString().c_str(), remotePort());
            Serial.printf("Le message reçu est : %s\n", udpTrame);

            // Si la trame UDP n'est pas un objet JSON
            if (udpTrame[0] != '{') return false;
            
            err = deserializeJson(doc, udpTrame);
            if (err == DeserializationError::Ok)
            {
                // Si aucune erreur n'est survenue lors du deserialisation
                return true;
            }
            else
            {
                Serial.print(F("deserializeJson() failed with code "));
                Serial.println(err.f_str());
                return false;
            }
        }
    }

    return false;
}

/// @brief Envoie un broadcast UDP
/// @param
void UdpEsp32::sendBroadcast(void)
{
    // Tout les 10 secondes, on envoie un broadcast UDP
    if (millis() - timerUdpBroadcast > TIMER_UDP)
    {
        // Send a broadcast message to the local network
        beginPacketMulticast(broadcastIP(), localUdpPort, localIP());
        write(broadcastTrame);
        endPacket();
        timerUdpBroadcast = millis();
    }
}

/// @brief Retourne le SSID de l'appareil
/// @param
/// @return
String UdpEsp32::SSID(void)
{
    return WiFi.SSID();
}