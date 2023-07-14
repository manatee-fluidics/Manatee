#include "sensors_and_pid.h"

// Sensors and pid configurations
int pressure_sensor_pins[] = {A9, A5, A10, A11, A12};       // Pressure sensors in order A9, 5, 10, 11, 12
double pressure_reads[] = {0, 0, 0, 0, 0};                  // Calibrated read values of the pressure sensors
boolean endstop_states[] = {0, 0, 0, 0, 0};                 // Endstop states
int n_oversample = 10;                                       // Times to oversample analog reads
float pressure_coeff_as[] = {0,0,0,0,0};                     // Coefficient value As for pressure calibration
float pressure_coeff_bs[] = {0,0,0,0,0};                     // Coefficient value Bs for pressure calibration
byte sensor_units[] = {0,0,0,0,0};                           // Sensor units (to be implemented)
double pressure_targets[] = {25, 25, 5, 5, 5};                  // Array of desired sensor pressure targets
double Kps[] = {0,0,0,0,0};                                     // PID controllers Kp values
double Kis[] = {0,0,0,0,0};                                     // PID controllers Ki values
double Kds[] = {0,0,0,0,0};                                     // PID controllers Kd values
PID myPIDs[] = {PID(&pressure_reads[0], &pid_motor_speed_targets[0], &pressure_targets[0], 0, 0, 0, DIRECT),
                PID(&pressure_reads[1], &pid_motor_speed_targets[1], &pressure_targets[1], 0, 0, 0, DIRECT),
                PID(&pressure_reads[2], &pid_motor_speed_targets[2], &pressure_targets[2], 0, 0, 0, DIRECT),
                PID(&pressure_reads[3], &pid_motor_speed_targets[3], &pressure_targets[3], 0, 0, 0, DIRECT),
                PID(&pressure_reads[4], &pid_motor_speed_targets[4], &pressure_targets[4], 0, 0, 0, DIRECT)};

// Functions

void read_endstop_pins(){
  byte es_pi;
  for (int pi=0;pi<n_pumps;pi++){
    es_pi = 0;
    for (byte es_pi_i=0;es_pi_i<5;es_pi_i++){
      es_pi += digitalRead(endstop_pins[pi]);
    }
    if(es_pi>=4){ //pulled high
      endstop_states[pi] = 0;
    }
    if(es_pi==0){ //engaged, pulled low
      endstop_states[pi] = 1;
    }
  }
}

void read_pressures(){
  double my_read = 0; 
  int count_oversample = 0; 
  for (int pi=0;pi<n_pumps;pi++){
    my_read = 0;
    count_oversample = 0;
    while (count_oversample<n_oversample){
      count_oversample += 1;
      my_read += analogRead(pressure_sensor_pins[pi]);
    }
    pressure_reads[pi] = my_read/n_oversample;
    pressure_reads[pi] = (((pressure_reads[pi])/1023) - pressure_coeff_bs[pi])/pressure_coeff_as[pi];
  }
}

void feedbackRegulate(int pi){
  myPIDs[pi].Compute();
  setMotorSpeed(pi, pid_motor_speed_targets[pi]);             // Update speed /change to PID?
}
