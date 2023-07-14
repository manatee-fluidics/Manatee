#ifndef DISPLAY_H
#define DISPLAY_H

#include <U8glib.h>
#include "control_and_command.h"
#include "encoder.h"
#include "timing.h"
#include "effectors.h"
#include "sensors_and_pid.h"
#include "serial.h"

// Global object declaration
extern U8GLIB_ST7920_128X64_1X u8g;           // SPI Com: SCK = en = 23, MOSI = rw = 17, CS = di = 16

// Function declaration
void draw();

#endif // DISPLAY_H
