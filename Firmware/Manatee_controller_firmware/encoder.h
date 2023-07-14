#ifndef ENCODER_H
#define ENCODER_H
#include <Encoder.h>

#include "display.h"
#include "control_and_command.h"
#include "timing.h"
#include "effectors.h"
#include "sensors_and_pid.h"
#include "serial.h"

// Encoder function variable declarations
extern Encoder myEnc;
extern long encoder_pososition;                          
extern long new_encoder_pososition;                       
extern int encoder_button_pin;                       
extern long new_encoder_position;                         
extern long encoder_position;                             
extern boolean encoder_button;                                                       

// Encoder function function declarations
void handle_encoder();
void handleBtn();

#endif // ENCODER_H
