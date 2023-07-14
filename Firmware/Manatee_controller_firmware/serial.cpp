#include "serial.h"

// Serial communication settings
byte upload = 0;                                   // commands from serial or program only execute if enabled
byte serial_counter = 11;                          // Serial byte counter
boolean got_message = 0;                           // Trigger on message complete
byte serial_command[11];                           // Incoming serial command buffer
byte command_buffers[6][500];                      // Command buffer from Serial or EEprom
byte command[6];                                   // Current to be executed
byte status_command[6];                            // Current to be executed

// Functions

void get_serial(){
  while(Serial.available()){
    byte charbyte = Serial.read();
    serial_command[serial_counter] = charbyte;
    if(charbyte == 0xAA && serial_counter>=11){
      //start byte
      serial_counter = 0;
    }

    if(charbyte == 0x55 && serial_counter == 10){
      //stop byte
      got_message = 1;
      handle_serial_message();
    }
    serial_counter++;   
  }
}

void handle_serial_message(){
  if (got_message == 1){
    
    if(serial_command[2] < 0x40){                          // program commands go in the commands buffer
      if(upload == 1){
        int pi = 0;
        if (serial_command[3]%8 <= n_pumps){              //last 3 bits are pump address - 0-4, if 5, 6, 7 set to 0      first 5 = I2C slave addresses
          pi = serial_command[3]%8;
        }
        for(int mi=0;mi<6;mi++){                              //put it in the schedulder at pos 0 from where it is written to eeprom
          command_buffers[mi][0] = serial_command[mi+2];
        }
        writeToEeprom();
        command_active ++;
        //Serial.println(command_active);
      }
      else{                                             //if not uploading or triggering upload add it to the command buffer
        int pi = 0;
        if (serial_command[3]%8 <= n_pumps){              //last 3 bits shedulder address - 0-4, if 5, 6, 7 set to 0      first 5 = I2C slave addresses
          pi = serial_command[3]%8;
        }
  
        for(int mi=0;mi<6;mi++){
          command_buffers[mi][command_free] = serial_command[mi+2];
          
        }
        command_free ++;  
        if (command_free>498){
          command_free = 1;
          command_active = 0;
        }
      }
    }
    else {                                             // status commands are executed immediately
      for(int mi=0;mi<6;mi++){                         
        status_command[mi] = serial_command[mi+2];
      }      
    }
    got_message=0;
    handle_commands();
  }
}

void readSettingsAndReport(){
  int eaddr = 0;
  int byte_size = 0;
  n_pumps = 0;
  for (int pi=0;pi<5;pi++){
    
    // Read PID settings
    byte_size = 4; //doubles
    EEPROM.get( eaddr, Kps[pi] );
    eaddr += byte_size;
    EEPROM.get( eaddr, Kis[pi] );
    eaddr += byte_size;
    EEPROM.get( eaddr, Kds[pi] );
    eaddr += byte_size;

    // Read step to mm conversions
    byte_size = 4; //floats
    EEPROM.get( eaddr, motor_calibrations[pi]);
    eaddr += byte_size;

    // Read mm to ml conversions
    byte_size = 4; //floats
    EEPROM.get( eaddr, volume_factors[pi]);
    eaddr += byte_size;

    // Read max steps
    byte_size = 4; //longs
    EEPROM.get( eaddr, max_steps[pi]);
    motor_positions[pi] = max_steps[pi]/2;
    eaddr += byte_size;
    
    // Read max speeds
    byte_size = 4; //doubles
    EEPROM.get( eaddr, max_speeds[pi]);
    eaddr += byte_size;

    // Read channel-motor linking
    byte_size = 1; //bytes
    EEPROM.get( eaddr, link[pi]);
    eaddr += byte_size;

    // Read pressure coeffs
    byte_size = 4; //floats
    EEPROM.get( eaddr, pressure_coeff_as[pi]);
    eaddr += byte_size;
    EEPROM.get( eaddr, pressure_coeff_bs[pi]);
    eaddr += byte_size;

    // Read sensor units
    byte_size = 1; //bytes
    EEPROM.get( eaddr, sensor_units[pi]);
    eaddr += byte_size;

    //get npumps
    if (link[pi]>0){
      n_pumps ++;
    }
    sendValue(0x46, pi*11+0, Kps[pi]);
    sendValue(0x46, pi*11+1, Kis[pi]);
    sendValue(0x46, pi*11+2, Kds[pi]);
    sendValue(0x46, pi*11+3, motor_calibrations[pi]);
    sendValue(0x46, pi*11+4, volume_factors[pi]);
    sendValue(0x46, pi*11+5, max_steps[pi]/motor_calibrations[pi]*volume_factors[pi]);
    sendValue(0x46, pi*11+6, max_speeds[pi]);
    sendValue(0x46, pi*11+7, link[pi]);
    sendValue(0x46, pi*11+8, pressure_coeff_as[pi]);
    sendValue(0x46, pi*11+9, pressure_coeff_bs[pi]);
    sendValue(0x46, pi*11+10, sensor_units[pi]);
  } // 38 bytes per channel, 190 total
}

void sendValue(byte command, byte address, float value){
  union {
    float fval;
    byte bval[4];
  } floatAsBytes;
  floatAsBytes.fval = value;
  byte msg[] = {0xaa, 0xaa, command, address, floatAsBytes.bval[0], floatAsBytes.bval[1], floatAsBytes.bval[2], floatAsBytes.bval[3], 0x00, 0x00, 0x55};
  for (byte myi=0; myi<11; myi++){
    Serial.print(char(msg[myi]));
  }
  Serial.println();
}
