#include "eink.h"
#include "network.h"

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
}

void loop() {}
