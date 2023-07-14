#include "timing.h"

// Timing and Alarm settings
unsigned long wait_ms = 0;                         // Millis value to wait for
unsigned long refresh_ms = 0;                      // Next screen refresh
unsigned long save_wait = 0;                       // Remember millis at pause
unsigned long millis_end = 0;                      // Millis value of program complete
unsigned long beepressure_ms = 0;                  // Next time to beep
byte wait_TTL_address = 2;                         // Slave address for ttl input
byte wait_TTL_input_num = 1;                       // Input number on ttl slave
boolean pressure_max_alarm_on[] = {0, 0, 0, 0, 0};                     // Max pressure alarm states
double pressure_max_alarm_triggers[] = {0, 0, 0, 0, 0};                // Max pressure values to trigger alarm
boolean pressure_min_alarm_on[] = {0, 0, 0, 0, 0};                     // Min pressure alarm states
double pressure_min_alarm_triggers[] = {0, 0, 0, 0, 0};                // Min pressure values to trigger alarm
boolean time_alarm_on[] = {0, 0, 0, 0, 0};                             // Timing alarm states
unsigned long time_alarms[] = {0,0,0,0,0};                             // Timer values to trigger alarm
boolean speed_max_alarm_on[] = {0, 0, 0, 0, 0};                        // Max speed alarm states
double speed_max_alarm_triggers[] = {0, 0, 0, 0, 0};                   // Max speed values to trigger alarm
boolean speed_min_alarm_on[] = {0, 0, 0, 0, 0};                        // Min speed alarm states
double speed_min_alarm_triggers[] = {0, 0, 0, 0, 0};                   // Min speed values to trigger alarm

// Functions

void handle_alarms(){
  for (int pi=0;pi<n_pumps;pi++){                               //go through pumps
    if (pressure_max_alarm_on[pi]==1 && pressure_max_alarm_triggers[pi]<pressure_reads[pi]){
      alarm_on = 1;
      controller_state = 4;
      alarm_type = 0;
    }
    if (pressure_min_alarm_on[pi]==1 && pressure_min_alarm_triggers[pi]>pressure_reads[pi]){
      alarm_on = 1;
      controller_state = 4;
      alarm_type = 1;
    }
    if (time_alarm_on[pi]==1 && time_alarms[pi]<millis()){
      alarm_on = 1;
      controller_state = 4;
      alarm_type = 2;
    }
    if (speed_max_alarm_on[pi]==1 && speed_max_alarm_triggers[pi]<motor_speeds[pi]){
      alarm_on = 1;
      controller_state = 4;
      alarm_type = 3;
    }
    if (speed_min_alarm_on[pi]==1 && speed_min_alarm_triggers[pi]>motor_speeds[pi]){
      alarm_on = 1;
      controller_state = 4;
      alarm_type = 4;
    }
  }
}

void sound_alarm(){
  if(alarm_on==1 && millis()>beepressure_ms){
    for (int alai=0;alai<100;alai++){
      digitalWrite(speaker_pin, HIGH);
      delayMicroseconds(100);
      digitalWrite(speaker_pin, LOW);
      delayMicroseconds(100);
    }
    beepressure_ms = millis() + 500;
  }
}

void setupTimers(){
  TCCR1A = 0b00000000;
  TCCR1B = 0b00001001;
  TIMSK1 |= 0<<OCIE1A;

  TCCR3A = 0b00000000;
  TCCR3B = 0b00001001;
  TIMSK3 |= 0<<OCIE3A;

  TCCR4A = 0b00000000;
  TCCR4B = 0b00001001;
  TIMSK4 |= 0<<OCIE4A;

  TCCR5A = 0b00000000;
  TCCR5B = 0b00001001;
  TIMSK5 |= 0<<OCIE5A;

  TCCR2A = 0b00000000;
  TCCR2B = 0b00001001;
  TIMSK2 |= 0<<OCIE2A;
}

ISR(TIMER1_COMPA_vect) {
  // motor 0 (X), timer 1 (16b)
  if (states[0]==4){
    if (motor_positions[0] == go_to_targets[0]){
      states[0] = 0;
      motor_speed_targets[0] = 0;
      motor_speeds[0] = 0;
      TIMSK1 &= 0<<OCIE1A;
      enableMotor(0, 0);
    }
    else{
      PORTL =  PORTL |= 0b00001000; //d46 PL3
      PORTL =  PORTL &= 0b11110111;   
      motor_positions[0] += motor_directions[0];  
    }
  }
  else{
    PORTL =  PORTL |= 0b00001000; //d46 PL3
    PORTL =  PORTL &= 0b11110111;   
    motor_positions[0] += motor_directions[0];
  }
}

ISR(TIMER3_COMPA_vect) {
  // motor 1 (Y), timer 3(16b)
  if (states[1]==4){
    if (motor_positions[1] == go_to_targets[1]){
      states[1] = 0;
      motor_speed_targets[1] = 0;
      motor_speeds[1] = 0;
      TIMSK3 &= 0<<OCIE3A;
      enableMotor(1, 0);
    }
    else{
      PORTF =  PORTF |= 0b01000000;  //d60 PF7
      PORTF =  PORTF &= 0b10111111;   
      motor_positions[1] += motor_directions[1];
    }
  }
  else{
    PORTF =  PORTF |= 0b01000000;  //d60 PF7
    PORTF =  PORTF &= 0b10111111;   
    motor_positions[1] += motor_directions[1];
  }
}


ISR(TIMER4_COMPA_vect) {
  // motor 2 (Z), timer 4(16b)
  if (states[2]==4){
    if (motor_positions[2] == go_to_targets[2]){
      states[2] = 0;
      motor_speed_targets[2] = 0;
      motor_speeds[2] = 0;
      TIMSK4 &= 0<<OCIE4A;
      enableMotor(2, 0);
    }
    else{
      PORTF =  PORTF |= 0b00000001;  //d54 PF0
      PORTF =  PORTF &= 0b11111110;   
      motor_positions[2] += motor_directions[2];    }
    }
  else{
    PORTF =  PORTF |= 0b00000001;  //d54 PF0
    PORTF =  PORTF &= 0b11111110;   
    motor_positions[2] += motor_directions[2];
  }
}


ISR(TIMER5_COMPA_vect) {
  // motor 3 (E0), timer 5(16b)
  if (states[3]==4){
    if (motor_positions[3] == go_to_targets[3]){
      states[3] = 0;
      motor_speed_targets[3] = 0;
      motor_speeds[3] = 0;
      TIMSK5 &= 0<<OCIE5A;
      enableMotor(3, 0);
    }
    else{
      PORTC =  PORTC |= 0b00000010;  //d36 PC1
      PORTC =  PORTC &= 0b11111101;      
      motor_positions[3] += motor_directions[3];
    }
  }
  else{
    PORTC =  PORTC |= 0b00000010;  //d36 PC1
    PORTC =  PORTC &= 0b11111101;      
    motor_positions[3] += motor_directions[3];
  }
}

ISR(TIMER2_COMPA_vect) {
  // motor 4 (E1), timer 2(8b)
  if (states[4]==4){
    if (motor_positions[4] == go_to_targets[4]){
      states[4] = 0;
      motor_speed_targets[4] = 0;
      motor_speeds[4] = 0;
      TIMSK2 &= 0<<OCIE2A;
      enableMotor(4, 0);
    }
    else{
      PORTA =  PORTA |= 0b00010000;  //d26 PA4
      PORTA =  PORTA &= 0b11101111;
      motor_positions[4] += motor_directions[4];
    }
  }
  else{
    PORTA =  PORTA |= 0b00010000;  //d26 PA4
    PORTA =  PORTA &= 0b11101111;
    motor_positions[4] += motor_directions[4];
  }
}
