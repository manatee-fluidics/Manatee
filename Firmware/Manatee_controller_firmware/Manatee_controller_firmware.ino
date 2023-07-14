#include "display.h"
#include "control_and_command.h"
#include "encoder.h"
#include "timing.h"
#include "effectors.h"
#include "sensors_and_pid.h"
#include "serial.h"

void setup() {
  // Setup Wire and Serial
  Wire.begin();
  Serial.begin(250000);
  delay(100);
  
  // Connection and settings reports
  //reportConnect();
  readSettingsAndReport();
  
  // Slaves and timers setup
  scanSlaves();
  setupTimers();
  sei();
  
  // Pumps setup
  for (int pi = 0; pi < n_pumps; pi++) {
    pinMode(pressure_sensor_pins[pi], INPUT_PULLUP);
    myPIDs[pi].SetOutputLimits(-max_speeds[pi], max_speeds[pi]);  
    myPIDs[pi].SetTunings(Kps[pi], Kis[pi], Kds[pi]);
    myPIDs[pi].SetMode(AUTOMATIC);
    running_program = 0;
  }
  
  // Motors setup
  for (int pi = 0; pi < n_pumps; pi++) {
    pinMode(endstop_pins[pi], INPUT);                                             
    digitalWrite(endstop_pins[pi], HIGH);                                           
    pinMode(motor_step_pins[pi], OUTPUT);                                          
    pinMode(motor_direction_pins[pi], OUTPUT);                                       
    pinMode(motor_enable_pins[pi], OUTPUT);                                                  
    enableMotors(0); // Disable motors
  }
  
  // Valves setup
  for (int vi = 0; vi < 3; vi++) {
    pinMode(valves[vi], OUTPUT);                                                   
    analogWrite(valves[vi], 0); // Valves off   
  }
  
  // Encoder and kill buttons setup
  pinMode(encoder_button_pin, INPUT);                                                       
  pinMode(kill_pin, INPUT);                                                        
  digitalWrite(encoder_button_pin, HIGH);                                                     
  digitalWrite(kill_pin, HIGH);
  
  // Speaker setup
  pinMode(speaker_pin, OUTPUT);
}

void loop() {
  draw();
  handle_kill();
  read_pressures();
  read_endstop_pins();
  handle_motors();
  handle_commands();
  handle_wait();
  handle_encoder();
  get_serial();
  handle_alarms();
  sound_alarm();
}
