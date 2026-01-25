#include "eink.h"
#include "network.h"
#include "esp_sleep.h"

constexpr uint16_t IMG_WIDTH  = 400;
constexpr uint16_t IMG_HEIGHT = 300;
constexpr size_t IMG_SIZE = IMG_WIDTH * IMG_HEIGHT / 8;

uint8_t imgBuffer[IMG_SIZE];

void setup() {
  init_eink();
  bool connected = init_wifi(10000);
  if (connected) {
    if (fetch_image(imgBuffer, sizeof(imgBuffer))) {
      print_image(imgBuffer);
    }
  }

  // Sleep for 1 minute and refresh
  esp_sleep_enable_timer_wakeup(60ULL * 1000000ULL);
  esp_deep_sleep_start();
}

void loop() {}
