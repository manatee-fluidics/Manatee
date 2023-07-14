#ifndef TIMING_H
#define TIMING_H

#include "display.h"
#include "control_and_command.h"
#include "encoder.h"
#include "effectors.h"
#include "sensors_and_pid.h"
#include "serial.h"

// Timing and Alarm variable declarations
extern unsigned long wait_ms;                         
extern unsigned long refresh_ms;                      
extern unsigned long save_wait;                       
extern unsigned long millis_end;                      
extern unsigned long beepressure_ms;                  
extern byte wait_TTL_address;                         
extern byte wait_TTL_input_num;                       

extern boolean pressure_max_alarm_on[];                     
extern double pressure_max_alarm_triggers[];                
extern boolean pressure_min_alarm_on[];                     
extern double pressure_min_alarm_triggers[];                
extern boolean time_alarm_on[];                             
extern unsigned long time_alarms[];                             
extern boolean speed_max_alarm_on[];                        
extern double speed_max_alarm_triggers[];                   
extern boolean speed_min_alarm_on[];                        
extern double speed_min_alarm_triggers[];                   

// Timing and Alarm function declarations
void handle_alarms();
void sound_alarm();
void setupTimers();
ISR(TIMER1_COMPA_vect);
ISR(TIMER3_COMPA_vect);
ISR(TIMER4_COMPA_vect);
ISR(TIMER5_COMPA_vect);
ISR(TIMER2_COMPA_vect);

#endif // TIMING_H
