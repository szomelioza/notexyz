#include "eink.h"
#include <GxEPD2_BW.h>
#include <Adafruit_GFX.h>

GxEPD2_BW<GxEPD2_420_GDEY042T81, GxEPD2_420_GDEY042T81::HEIGHT> display(
  GxEPD2_420_GDEY042T81(10, 9, 8, 7)
);

void init_eink() {
  display.init(115200);
  display.setRotation(0);
}

void print_image(const uint8_t* imgBuffer) {
  display.setFullWindow();
  display.firstPage();
  do {
    display.fillScreen(GxEPD_BLACK);
    display.drawBitmap(
      0, 0,
      imgBuffer,
      400, 300,
      GxEPD_WHITE
    );
  } while (display.nextPage());
}