#pragma once
#include <Arduino.h>

bool init_wifi(int timeout);
bool fetch_image(uint8_t* imgBuffer, size_t bufferSize);