// ------------------------------------------------------
//    David DDI Lukasek 2025/04/10
// ------------------------------------------------------

#include "LedControl.h"

#define DIN 27
#define CS  26
#define CLK 22
#define FPS 15
#define FRAMES 3286

// ------------------------------------------------------

LedControl ledMat=LedControl(DIN, CLK, CS, 0);

byte all_frames[FRAMES][8] = {{/* PUT YOUR TEXT HERE (I KNOW, IT'S LONG, I KNOW) */}}

void drawFrame(byte* frame);

// ------------------------------------------------------

void setup() {
  ledMat.shutdown(0,false);
  ledMat.setIntensity(0,7);
  ledMat.clearDisplay(0);

  for(int i = 0; i < FRAMES; i++) {
    drawFrame(all_frames[i]);
    delay(66);
  }
}

void loop() {}

// ------------------------------------------------------

void drawFrame(byte* frame) {
  for(int i=0; i<8; i++) {
    ledMat.setRow(0,i,frame[i]);
  }
}