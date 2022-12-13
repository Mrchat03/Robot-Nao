/// @file json_esp32.h
/// @brief Lecture du JSON et envoi des requêtes MQTT
/// @author Nathanaël Amaridon
/// @date 2022-12-07
/// @version 1.0.0
/// @details

#pragma once
#ifndef JSON_ESP_32_H
#define JSON_ESP_32_H

#include <ArduinoJson.h>
enum class enumAction : char
{
    MOVEMENT = 0,
    DIALOG,
    ANIMATION,
    DANCE,
    COMMANDE,
    LED,
    MAX_ACTION
};

enumAction getAction(String key);

bool readJson(void);

#endif // !JSON_ESP_32_H