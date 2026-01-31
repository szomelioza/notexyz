#include "network.h"
#include "secrets.h"
#include <HTTPClient.h>
#include <WiFi.h>

bool init_wifi(int timeout) {
  WiFi.mode(WIFI_STA);
  WiFi.begin(SSID, PASSWD);

  unsigned long start = millis();
  while (WiFi.status() != WL_CONNECTED && millis() - start < timeout) {
    delay(100);
  }

  if (WiFi.status() == WL_CONNECTED) {
    return true;
  }
  return false;
}

bool fetch_image(uint8_t* imgBuffer, size_t bufferSize) {
  HTTPClient http;
  http.begin(API_URL);

  int statusCode = http.GET();
  if (statusCode != 200) {
    http.end();
    return false;
  }

  WiFiClient* stream = http.getStreamPtr();
  size_t offset = 0;

  while (stream->available() && offset < bufferSize) {
    imgBuffer[offset++] = stream->read();
  }

  http.end();

  WiFi.disconnect(true);
  WiFi.mode(WIFI_OFF);

  return offset == bufferSize;
}