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