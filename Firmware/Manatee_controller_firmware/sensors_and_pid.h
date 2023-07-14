#ifndef SENSORS_AND_PID_H
#define SENSORS_AND_PID_H
#include <PID_v1.h>

#include "display.h"
#include "control_and_command.h"
#include "encoder.h"
#include "timing.h"
#include "effectors.h"
#include "serial.h"

// Sensor and PID variable declarations
extern int pressure_sensor_pins[];       
extern double pressure_reads[];                  
extern boolean endstop_states[];                 
extern int n_oversample;                                       
extern float pressure_coeff_as[];                     
extern float pressure_coeff_bs[];                     
extern byte sensor_units[];                           
extern double pressure_targets[];                  

extern double Kps[];                                     
extern double Kis[];                                     
extern double Kds[];                                     
extern PID myPIDs[];

// Sensor function declarations
void read_endstop_pins();
void read_pressures();
void feedbackRegulate(int pi);

#endif // SENSORS_AND_PID_H
