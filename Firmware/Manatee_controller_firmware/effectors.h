#ifndef EFFECTORS_H
#define EFFECTORS_H

#include "display.h"
#include "control_and_command.h"
#include "encoder.h"
#include "timing.h"
#include "sensors_and_pid.h"
#include "serial.h"

// Effector variable declarations
extern int valves[];                          
extern float motor_calibrations[];         
extern double volume_factors[];            
extern int endstop_pins[];       
extern int motor_step_pins[];  
extern int motor_direction_pins[];    
extern int motor_enable_pins[];       
extern int motor_directions[]; 

extern double motor_speed_targets[];                  
extern double pid_motor_speed_targets[];              
extern double user_motor_speed_targets[];                 
extern double motor_speeds[];                         
extern long motor_interrupt_counters[];               
extern long motor_interrupts_perstep[];               
extern long motor_interrupts_next[];                  
extern float motor_acceleration;                                  
extern unsigned long accel_ms;                                      
extern byte home_targets[];                               
extern long max_steps[];                                  
extern double max_speeds[];                               
extern long motor_positions[];                        
extern long go_to_targets[];                          
extern long wait_steps[];                             
extern long wait_steps_start[];                       
extern byte timer_prescalers[];                           
extern int timer_resolutions[];                       
extern long timer_compares[];                         
extern long motor_offset_home;                                   

// Effector function declarations
void handle_motors();
void homeMotor(int pi);
void go_to(int pi, long pos);
void enableMotors(boolean e);
void enableMotor(int ei, boolean e);
void updateSpeeds();
void setMotorSpeed(int pi, float my_speed);
void setValve(int addr, byte state);

#endif // EFFECTORS_H
