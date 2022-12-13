/// @file json_esp32.cpp
/// @brief Lecture du JSON et envoi des requêtes MQTT
/// @author Nathanaël Amaridon 
/// @date 2022-12-07
/// @version 1.0.0
/// @details

#include <ArduinoJson.h>

#include "json_esp_32.h"
#include "mqtt_esp_32.h"
#include "wifi_esp_32.h"

StaticJsonDocument<512> doc;
extern MqttEsp32 mqttEsp32;

/// @brief Lecture du JSON
/// @param  
/// @return Vrai si le JSON est valide
bool readJson(void)
{
    String strObj = "";
    int nbRequest = 0;

    enumAction action = enumAction::MAX_ACTION;

    if (doc.isNull())
    {
        Serial.println("obj est null");
        return false;
    }

    for (auto iter : doc.as<JsonObject>())
    {
        Serial.println(iter.key().c_str());

        action = getAction(iter.key().c_str());
        if (action == enumAction::COMMANDE)
        {
            if (iter.value().containsKey("mqtt"))
            {
                auto ipBroker = iter.value()["mqtt"];
                Serial.println(ipBroker.as<String>().c_str());
                if (ipBroker.containsKey("set"))
                {
                    Serial.println(mqttEsp32.getBroker());
                    Serial.println(ipBroker["set"].as<String>().c_str());
                    mqttEsp32.setNewBroker(ipBroker["set"].as<String>());
                    Serial.println(mqttEsp32.getBroker());
                   
                }
            }
            if (iter.value().containsKey("wifi"))
            {
                auto wifi = iter.value()["wifi"];
                Serial.println(wifi.as<String>().c_str());
                if (wifi.containsKey("set"))
                {
                    auto setWifi = wifi["set"];
                    if (!setWifi.containsKey("ssid") || !setWifi.containsKey("pwd"))
                    {
                        Serial.println("La commande wifi n'est pas valide");
                        return false;
                    }
                    auto ssid = setWifi["ssid"].as<String>();
                    auto password = setWifi["pwd"].as<String>();
                    Serial.println("Reçu : SSID: " + ssid + " MDP :" + password);
                    setNewWifi(ssid.c_str(), password.c_str());
                }
            }
            else
            {
                Serial.println("Aucune commande trouvée");
                return false;
            }
        }
        else if (action == enumAction::MOVEMENT ||
                 action == enumAction::DIALOG ||
                 action == enumAction::ANIMATION ||
                 action == enumAction::DANCE ||
                 action == enumAction::LED)
        {
            auto topic = iter.value()["topic"];
            auto payload = iter.value()["payload"];
            Serial.println(topic.as<String>().c_str());
            Serial.println(payload.as<String>().c_str());

            mqttEsp32.setTopic(nbRequest, topic.as<String>().c_str());

            mqttEsp32.setPayload(nbRequest, payload.as<String>().c_str());
            mqttEsp32.setNbRequest(++nbRequest);
        }
        else
        {
            return false;
        }
    }
    return true;
}

/// @brief Récupération de l'action
enumAction getAction(String key)
{
    enumAction action = enumAction::MAX_ACTION;
    if (key == "commande")
    {
        action = enumAction::COMMANDE;
    }
    else if (key == "movement")
    {
        action = enumAction::MOVEMENT;
    }
    else if (key == "dialog")
    {
        action = enumAction::DIALOG;
    }
    else if (key == "animation")
    {
        action = enumAction::ANIMATION;
    }
    else if (key == "dance")
    {
        action = enumAction::DANCE;
    }
    else if (key == "led")
    {
        action = enumAction::LED;
    }
    else
    {
        Serial.println("Aucune action trouvée");
    }
    return action;
}