#include "effectors.h"

// Effector settings
int valves[] = {8,9,10};                          // Pins for valves
int endstop_pins[] = {18,15,14,2,3};       // Pins for endstop_pins in order
float motor_calibrations[] = {0,0,0,0,0};         // Convert steps to mm (steps/mm)
double volume_factors[] = {0,0,0,0,0};            // Convert mm to ul (ul/mm)
int motor_step_pins[] = {46,60,54,36,26};  // Motor step pins in order
int motor_direction_pins[] = {48,61,55,34,28};    // Motor dir pins in order
int motor_enable_pins[] = {62,56,38,30,24};       // Motor enable pins in order
int motor_directions[] = {-1, -1, -1, -1, -1};    // Motor directions
double motor_speed_targets[] = {0, 0, 0, 0, 0};                  // Array of speed targets of motors in mm/s
double pid_motor_speed_targets[] = {0, 0, 0, 0, 0};              // Array of speed targets by PID controllers of motors in mm/s
double user_motor_speed_targets[] = {0,0,0,0,0};                 // Array of user desired speed targets of motors in mm/s
double motor_speeds[] = {0, 0, 0, 0, 0};                         // Array of actual speeds in mm/s
long motor_interrupt_counters[] = {0, 0, 0, 0, 0};               // Array of counters keeping track of interrupts(1us) for each motor since last step
long motor_interrupts_perstep[] = {0, 0, 0, 0, 0};               // Array of actual speeds in us/step
long motor_interrupts_next[] = {0, 0, 0, 0, 0};                  // Array of next steps (us)
float motor_acceleration = 100;                                  // Acceleration in mm/s^2
unsigned long accel_ms = 0;                                      // Motor speed update frequency
byte home_targets[] = {0,0,0,0,0};                               // homing direction 0:min 1 max
long max_steps[] = {0,0,0,0,0};                                  // Maximum steps of pumps 346700;  
double max_speeds[] = {0,0,0,0,0};                               // Max speed of motors (mm/s)
long motor_positions[] = {0, 0, 0, 0, 0};                        // Array of actual stepper positions in steps
long go_to_targets[] = {0, 0, 0, 0, 0};                          // Array of actual stepper positions in steps
long wait_steps[] = {0, 0, 0, 0, 0};                             // Array of actual stepper positions in steps
long wait_steps_start[] = {0, 0, 0, 0, 0};                       // Array of actual stepper positions in steps
byte timer_prescalers[] = {1,1,1,1,1};                           // Prescaler for timers (they need to be scaled if motors are very slow)
int timer_resolutions[] = {16,16,16,16,8};                       // Timer bit resolutions
long timer_compares[] = {1, 1, 1, 1, 1};                         // Timer trigger values
long motor_offset_home = 1200;                                   //offset from homing switch so it's not triggered

// Functions

void handle_motors(){
  for (int pi=0;pi<n_pumps;pi++){
    if (states[pi] == 1 || states[pi] == 2){                        // states: 0 idle, 1 homing, 2 setup homing, 3 feedback reg, 4 move constant, 5 wait steps
      homeMotor(pi);
    }
    else if(states[pi] == 3 || states[pi] == 5){
      feedbackRegulate(pi);
    }
    else if (states[pi] == 0){
      setMotorSpeed(pi, 0.0);  
    }
    delay(10);
    updateSpeeds();
  }
}

void homeMotor(int pi){
  if (states[pi] == 1){                     //we are in homing state

    if (endstop_states[pi]==1){   //if endstop hit
      
      states[pi] = 0;
      if (home_targets[pi]==0){
        motor_positions[pi] = 0 - motor_offset_home;
        user_motor_speed_targets[pi] = max_speeds[pi]/4;
        states[pi] = 4;
        go_to(pi, 0);
      }
      else{
        motor_positions[pi] = max_steps[pi] + motor_offset_home;
        user_motor_speed_targets[pi] = max_speeds[pi]/4;        
        states[pi] = 4;
        go_to(pi, max_steps[pi]);
      }
    }
    else{
      if(home_targets[pi]==0){
        setMotorSpeed(pi, max_speeds[pi]*-1);
      }
      else if (home_targets[pi]==1){
        setMotorSpeed(pi, max_speeds[pi]);              
      }
    }
  }
}

void go_to(int pi, long pos){                                
  if (motor_positions[pi]<pos){
    setMotorSpeed(pi, user_motor_speed_targets[pi]);
  }
  else{
    setMotorSpeed(pi, -user_motor_speed_targets[pi]);
  }
  go_to_targets[pi] = pos;
}

void enableMotors(boolean e){
  for (byte ei=0;ei<n_pumps; ei++){
    digitalWrite(motor_enable_pins[ei],1-e);                          // Enable motors
  }
}

void enableMotor(int ei, boolean e){
  digitalWrite(motor_enable_pins[ei],1-e);                          // Enable motors
}

void updateSpeeds(){ //update speed (delay in homing) in ms  
  byte speed_changed = 0;
  float refresh_speed = millis() - accel_ms;
  accel_ms = millis();
  for (int pi=0;pi<n_pumps;pi++){
    if((motor_positions[pi]>=0-motor_offset_home && motor_positions[pi]<=max_steps[pi]+motor_offset_home) || (motor_positions[pi]>=0 && motor_positions[pi]<=max_steps[pi] && endstop_states[pi]==0)){                                    //don't move outside 
      if (motor_speeds[pi]!=motor_speed_targets[pi]){                                               //if target speed is not reached
        speed_changed = 1;                                                                          //flag
        if (motor_speeds[pi]-motor_acceleration*refresh_speed/1000>motor_speed_targets[pi]){        //decel
          motor_speeds[pi] = motor_speeds[pi] - motor_acceleration*refresh_speed/1000;
        }
        else if (motor_speeds[pi]+motor_acceleration*refresh_speed/1000<motor_speed_targets[pi]){   //accel
          motor_speeds[pi] = motor_speeds[pi] + motor_acceleration*refresh_speed/1000;
        }
        else{
          motor_speeds[pi] = motor_speed_targets[pi];                                               //if too close to accel
        }
      
        if (motor_speeds[pi]!=0){                                                                   //calc timer compares and prescalers
        
          timer_compares[pi] = 16000000 / (motor_speeds[pi]*motor_calibrations[pi]);
          byte presc = 1;
          if (timer_compares[pi]>pow(2,timer_resolutions[pi] )*1024){
            presc = 5;
            timer_compares[pi] = pow(2,timer_resolutions[pi] )*1024;
            //send error we cant go this slow     
          }
          if (timer_compares[pi]>pow(2,timer_resolutions[pi] )*256){
            presc = 5;
            timer_compares[pi] = timer_compares[pi]/1024;      
          }
        
          if (timer_compares[pi]>pow(2,timer_resolutions[pi] )*64){
            presc = 4;
            timer_compares[pi] = timer_compares[pi]/256;      
          }
        
          if (timer_compares[pi]>pow(2,timer_resolutions[pi] )*8){
            presc = 3;
            timer_compares[pi] = timer_compares[pi]/64;      
          }
        
          if (timer_compares[pi]>pow(2,timer_resolutions[pi] )){
            presc = 2;
            timer_compares[pi] = timer_compares[pi]/8;      
          }
          timer_prescalers[pi] = presc;
        }    
      }
    }
    else{
      speed_changed = 1;
      motor_speed_targets[pi] = 0;
      motor_speeds[pi] = 0;
      states[pi] = 0;
    }
    if(motor_positions[pi]<0-motor_offset_home){
      motor_positions[pi] = 0-motor_offset_home;
    }
    if(motor_positions[pi]>max_steps[pi]+motor_offset_home){
      motor_positions[pi] = max_steps[pi]+motor_offset_home;
    }
  }
  if (speed_changed == 1){
    
    if (motor_speeds[0]!=0){
      TIMSK1 |= 1<<OCIE1A;
      TCCR1B = (TCCR1B & 0b11111000) | timer_prescalers[0];
      OCR1A = timer_compares[0] - 1;
      enableMotor(0, 1);
    }
    else{
      TIMSK1 &= 0<<OCIE1A;
      enableMotor(0, 0);
    }
    if (motor_speeds[1]!=0){
      TIMSK3 |= 1<<OCIE3A;
      TCCR3B = (TCCR3B & 0b11111000) | timer_prescalers[1];
      OCR3A = timer_compares[1] - 1;
      enableMotor(1, 1);
    }
    else{
      TIMSK3 &= 0<<OCIE3A;
      enableMotor(1, 0);
    }
    if (motor_speeds[2]!=0){
      TIMSK4 |= 1<<OCIE4A;
      TCCR4B = (TCCR4B & 0b11111000) | timer_prescalers[2];
      OCR4A = timer_compares[2] - 1;
      enableMotor(2, 1);
    }
    else{
      TIMSK4 &= 0<<OCIE4A;
      enableMotor(2, 0);
    }
    if (motor_speeds[3]!=0){
      TIMSK5 |= 1<<OCIE5A;
      TCCR5B = (TCCR5B & 0b11111000) | timer_prescalers[3];
      OCR5A = timer_compares[3] - 1;
      enableMotor(3, 1);
    }
    else{
      TIMSK5 &= 0<<OCIE5A;
      enableMotor(3, 0);
    }
    if (motor_speeds[4]!=0){
      TIMSK2 |= 1<<OCIE2A;
      TCCR2B = (TCCR2B & 0b11111000) | timer_prescalers[4];
      OCR2A = timer_compares[4] - 1;
      enableMotor(4, 1);
    }
    else{
      TIMSK2 &= 0<<OCIE2A;
      enableMotor(4, 0);
    }
  }
}

void setMotorSpeed(int pi, float my_speed){
  if (my_speed<0){
    motor_directions[pi] = -1;
    my_speed  = my_speed*-1;
    digitalWrite(motor_direction_pins[pi], LOW);                 
  }
  else if (my_speed>0){
    motor_directions[pi] = 1;
    digitalWrite(motor_direction_pins[pi], HIGH);
  }
  if (my_speed>max_speeds[pi]){
    my_speed = max_speeds[pi];
  }
  motor_speed_targets[pi]  = my_speed;
  
  accel_ms = millis();
}

void setValve(int addr, byte state){
  digitalWrite(valves[addr],state);
  if (state == 1){                            // if we are turning on wait 50 ms and lover voltage for cool valves
    delay(50);
    analogWrite(valves[addr], 255);
  }
}
