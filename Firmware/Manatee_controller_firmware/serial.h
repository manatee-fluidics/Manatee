#ifndef SERIAL_H
#define SERIAL_H

#include "display.h"
#include "control_and_command.h"
#include "encoder.h"
#include "effectors.h"
#include "sensors_and_pid.h"

// Serial communication variable declarations
extern byte upload;                                   
extern byte serial_counter;                          
extern boolean got_message;                           
extern byte serial_command[];                           
extern byte command_buffers[][500];                      
extern byte command[];                                   
extern byte status_command[];                            

// Serial communication function declarations
void get_serial();
void handle_serial_message();
void readSettingsAndReport();
void sendValue(byte command, byte address, float value);

#endif // SERIAL_H
