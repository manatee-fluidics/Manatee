#ifndef CONTROL_AND_COMMAND_H
#define CONTROL_AND_COMMAND_H
#include <EEPROM.h>
#include <Wire.h>

#include "display.h"
#include "encoder.h"
#include "timing.h"
#include "effectors.h"
#include "sensors_and_pid.h"
#include "serial.h"

// General system and Command and control variable declarations
extern void (*resetFunc)(void);
extern int kill_pin;                                 
extern int speaker_pin;                              
extern byte last_controller_state;                    
extern boolean screen_refresh;                        
extern boolean alarm_on;                              
extern byte alarm_type;

extern int command_active;                          
extern int save_command_active;                    
extern int command_free;                             
extern byte infinite_loop;                           
extern int cycles_to_do;                             
extern int cycle_count;                              
extern int start_cycle;                              
extern int controller_state;                         
extern int states[];                       
extern int running_program;                          
extern byte link[];                        
extern int n_pumps;                                  

// General system and Command and control function declarations
void handle_commands();
void execute_command(byte this_command[], int pi);
void clearBuffer();
void handle_wait();
void handle_kill();
void writeBufferToEeprom();
void clearEeprom();
void writeToEeprom();
void readBufferFromEeprom();
void changeEEPROMSetting(byte pi, byte setting_no, float value);
void scanSlaves();
void listenSlaves();

#endif // CONTROL_AND_COMMAND_H
