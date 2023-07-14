#include "control_and_command.h"

// General system and Command settings
int kill_pin = 41;                                 // Kill pin
int speaker_pin = 37;                              // Speaker pin
byte last_controller_state = 1;                    // Keeps track if controller state has changed
boolean screen_refresh = 1;                        // Keeps track if screen needs refreshing
boolean alarm_on = 0;                              // alarm on
byte alarm_type = 0;                               // 0:max press, 1:min press, 2:time, 3:max speed, 4 min speed

int command_active = 0;                           // Indexes for active command 
int save_command_active = 0;                      // Counter for active command 
int command_free = 0;                             // Counter for free command 
byte infinite_loop = 0;                           // program cycle count == 0 ---> infinite loop flag
int cycles_to_do = 0;                             // Keeps track of the number of cycles to be done
int cycle_count = 0;                              // Cycle counter
int start_cycle = 0;                              // Flag to start a cycle
int controller_state = 0;                         // 0 idle, 1 complete, 2 wait time, 3 paused, 4 wait TTL 
int states[] = {0,0,0,0,0};                       // 0 idle, 1 homing, 2 setup homing, 3 feedback reg, 4 move constant, 5 wait steps
int running_program = 0;                          // running program: 0-no, 1-from eeprom, 2-online
byte link[] = {0,0,0,0,0};                        //pumps available, 0 off 1 on
int n_pumps = 0;                                  // Number of pumps connected to the controller

// Functions
void(* resetFunc) (void) = 0;

void handle_commands() {
  byte prog_done = 0;
  
  // Execute status command if present
  if (status_command[0] != 0) {
    execute_command(status_command, 0);
    for(int mi = 0; mi < 6; mi++) {                         
      status_command[mi] = 0;
    }          
  }
  
  // Refresh screen if timer has passed
  if (millis() > refresh_ms) {
    refresh_ms += 1000;
    screen_refresh = 1;
  }
  
  // Process commands if not running a program or controller is idle/done
  if (running_program == 0 || controller_state < 2) {
    if (command_free > command_active) {
      // Get next command from buffer
      for(int mi = 0; mi < 6; mi++) {
        command[mi] = command_buffers[mi][command_active];
      }      
      command_active++;
      
      // Execute command based on condition
      if(command[1] < 5) {
        execute_command(command, command[1]);
      } else {
        for (int pi = 0; pi < n_pumps; pi++) {
          execute_command(command, pi);
          Serial.println(command[1]);
        }
      }
      
      // Empty buffer if online
      if (running_program == 2) {
        for (int push = 0; push < command_free; push++) {
          for(int mi = 0; mi < 6; mi++) {
            command_buffers[mi][push] = command_buffers[mi][push + 1];
          }   
        }
        command_active--;
        command_free--;
      }
    }
  }
  
  // Check if running a program and reached the last command
  if (command_free == command_active && command_free > 0 && running_program > 0) {
    millis_end = millis();
    controller_state = 1;
    running_program = 0;
  }      
}

void execute_command(byte this_command[], int pi){
  double command_value;
  
  union u_tag {
  byte b[4]; 
  double fval;
  } u;

  // Assigning command values
  u.b[0] = this_command[2];
  u.b[1] = this_command[3];
  u.b[2] = this_command[4];
  u.b[3] = this_command[5];
    
  command_value = u.fval;

  // Execute command based on value
  switch (this_command[0]){
    case 0x10:{                                                   // Set speed
      user_motor_speed_targets[pi] = command_value / volume_factors[pi];
    }
    break;

    case 0x11:{                                                  // Set target          
      pressure_targets[pi] = command_value;
    }
    break;

    case 0x12:{                                                  // Move motor to an absolute position          
      states[pi] = 4;
      go_to(pi, command_value * motor_calibrations[pi] / volume_factors[pi]);
    }         
    break;
    
    case 0x13:{                                                  // Move motor relative to current position
      states[pi] = 4;
      go_to(pi, command_value * motor_calibrations[pi] / volume_factors[pi] + motor_positions[pi]);
    }       
    break;

    case 0x14:{                                                  // Open/close valve          
      setValve(this_command[1], this_command[2]);
    }       
    break;

    case 0x15:{                                                  // Home             
      if(this_command[2]==0){                 //endstop_pins open, run to min
        motor_positions[pi] = max_steps[pi];
        setMotorSpeed(pi, max_speeds[pi]*-1);
        home_targets[pi] = 0;
      }
      else if (this_command[2]==1){           //endstop_pins open, run to max
        motor_positions[pi] = 0;
        setMotorSpeed(pi, max_speeds[pi]);              
        home_targets[pi] = 1;
      }
      states[pi] = 1;
      controller_state = 2;
    }                 
    break;
  
    case 0x16:{                                                  // Start/stop regulating
      if (command_value == 0){
        states[pi] = 0;
      }
      else{
        states[pi] = 3;
      }
    }         
    break;
    
    case 0x17:{                                                  // Send to slave
      Wire.beginTransmission(this_command[1]); // transmit to device #8
      Wire.write(0);
      Wire.write(0);
      for (int mycomi=0;mycomi<6;mycomi++){
        Wire.write(this_command[mycomi]);
      }
      Wire.write(0);
      Wire.write(0);
      Wire.endTransmission();
    }         
    break;
    
    case 0x18:{                                                  // Wait time
      wait_ms = (unsigned long)(command_value*1000) + millis();
      controller_state = 2;
    }
    break;
    
    case 0x19:{                                                  // Wait volume
      if ((command_value * motor_calibrations[pi] / volume_factors[pi] + motor_positions[pi]) > 0){
        wait_steps[pi] = (long)(command_value * motor_calibrations[pi] / volume_factors[pi]) + motor_positions[pi];
      }
      else{
        wait_steps[pi] = 0;
      }
      if (wait_steps[pi] > max_steps[pi]){
        wait_steps[pi] = max_steps[pi];
      }
      wait_steps_start[pi] = motor_positions[pi];
      states[pi] = 5;
      controller_state = 2;
    }      
    break;
    
    case 0x20:{                                                  // Wait slave
      wait_TTL_address = this_command[1];
      wait_TTL_input_num = this_command[2];
      Wire.beginTransmission(this_command[1]); // transmit to device #8
      Wire.write(0);
      Wire.write(0);
      Wire.write(0);
      Wire.write(0);
      Wire.write(0x23);
      Wire.write(0);
      Wire.write(0);
      Wire.write(0);
      Wire.write(0);
      Wire.write(0);
      Wire.endTransmission();      
      controller_state = 4;
    }      
    break;
    
    case 0x21:{                                                  // Cycle start
      start_cycle = command_active;
      cycles_to_do = (int) command_value;                            // We did one already
      cycle_count ++;
      if (cycles_to_do < 1){                                   // If cycles_to_do <1 infinite loop
        cycles_to_do = 2;
        infinite_loop = 1;
      }
    }        
    break;
  
    case 0x22:{                                                  // Cycle stop
      cycles_to_do --;
      cycle_count ++;
      if (cycles_to_do > 0){
        command_active = start_cycle;
      }
      else{
        cycle_count = 0;
      }
    }
    break;

    case 0x23:{                                                  // activate alarm
      byte alarm_type = this_command[1]/8;                       
      if (pi == 0){                                             //dont run this 5 times if pi>4
        pi = this_command[1]%8;
        switch(alarm_type){
          case 0:{
            pressure_max_alarm_on[pi] = this_command[2];
          }
          break;
          case 1:{
            pressure_min_alarm_on[pi] = this_command[2];
          }
          break;
          case 2:{
            time_alarm_on[pi] = this_command[2];
            time_alarms[pi] += millis();
          }
          break;
          case 3:{
            speed_max_alarm_on[pi] = this_command[2];
          }
          break;
          case 4:{
            speed_min_alarm_on[pi] = this_command[2];
          }
          break;
        }
      }
    }
    break;

    case 0x24:{                                                  // set alarm value
      byte alarm_type = this_command[1]/8;                             
      if (pi == 0){                                             //dont run this 5 times if pi>4
        pi = this_command[1]%8;
        switch(alarm_type){
          case 0:{
            pressure_max_alarm_triggers[pi] = command_value;
          }
          break;
          case 1:{
            pressure_min_alarm_triggers[pi] = command_value;
          }
          break;
          case 2:{
            time_alarms[pi] = (unsigned long) command_value*1000;
            
          }
          break;
          case 3:{
            speed_max_alarm_triggers[pi] = command_value / volume_factors[pi];
          }
          break;
          case 4:{
            speed_min_alarm_triggers[pi] = command_value / volume_factors[pi];
          }
          break;
        }
      }
    }
    break;

    case 0x26:{                                                  // sound alarm
      alarm_on = this_command[2];
    }
    break;

    case 0x40:{                                                  // Upload
      if(command_value == 1){
        clearEeprom();
        command_active = 0;                                  //while uploading these keep track of the eeprom adresses
        upload = 1;
      }
      else{
        resetFunc();                                             // if upload complete reset
      }
    }
    break;

    case 0x41:{                                                  // Online
      if(command_value == 1){
        Serial.println("runningProg");
        command_free = 0;
        command_active = 0;
        running_program = 2;
        
      }
      //else{
        //resetFunc();                                             // when online ends
      //}
    }
    break;

    case 0x42:{                                                  // Get motor positions
      for (int mypi=0;mypi<n_pumps;mypi++){
        sendValue(0x42, mypi, motor_positions[mypi] / motor_calibrations[mypi] * volume_factors[mypi]);
      }
    }
    break;

    case 0x43:{                                                  // Get motor speeds
      for (int mypi=0;mypi<n_pumps;mypi++){
        sendValue(0x43, mypi, motor_speeds[mypi] * motor_directions[mypi] * volume_factors[mypi]);
      }
    }
    break;

    case 0x44:{                                                  // Get pressures
      for (int mypi=0;mypi<n_pumps;mypi++){
        sendValue(0x44, mypi, pressure_reads[mypi]);
      }
    }      
    break;

    case 0x45:{                                                  // Clear buffer
      clearBuffer();
    }
    break;

    case 0x46:{                                                  // read settings      
      readSettingsAndReport();
    }
    break;

    case 0x47:{                                                  // change setting
      changeEEPROMSetting(this_command[1]/11, this_command[1]%11, command_value);
    }
    break;

    case 0x48:{                                                  // commands in buffer
      if ((command_free-command_active)>=0){
        sendValue(0x48, 0, command_free-command_active);
      }
      else{
        sendValue(0x48, 0, command_free-command_active+500);
      }
    }  
    break;

    case 0x49:{                                                  // Reset controller
        resetFunc();                                             
    }
    break;
  }
}

void clearBuffer(){ 
  command_free=0;
  command_active=0;
  for (int b1i=0;b1i<500;b1i++){
    for (int b0i=0;b0i<6;b0i++){
      command_buffers[b0i][b1i] = 0;
    }
  } 
}

void handle_wait(){                          
  if(controller_state == 2 && wait_ms <= millis()){       //waiting and we passed wait_ms
    controller_state = 0;
  }
  
  if (controller_state == 4){                                 //waiting for ttl input
    byte readWire = 0;
    byte counter = 0;
    Wire.requestFrom(wait_TTL_address, (uint8_t)7);              // request 1 bytes from slave device #
    while (Wire.available()) {                                // slave may send less than requested
      readWire = Wire.read();                                 // receive a byte as character
      if (counter>0){                                         //first byte is 2 signalling its a ttl slave
        if(wait_TTL_input_num+1 == counter & readWire ==1){   //we are waiting for he right ttl input on the slave to trigger
          Serial.println("triggered");
          controller_state = 0;
        }
      }
      counter ++;
    }
  }  
  for (int pi=0;pi<n_pumps;pi++){                             
    if (states[pi]==1){                                       //states: 0 idle, 1 homing, 2 setup homing, 3 feedback reg, 4 move constant, 5 wait steps
      controller_state = 2;
    }
    else if (states[pi]==5){
      if ((wait_steps_start[pi] < wait_steps[pi] && wait_steps[pi] <= motor_positions[pi]) || (wait_steps_start[pi] > wait_steps[pi] && wait_steps[pi] >= motor_positions[pi])){          //waiting steps and we passed wait_steps
        states[pi]=3;
      }
      else{
        controller_state = 2;                                 //still waiting for steps
      }
    }
  }
}

void handle_kill(){
  if (digitalRead(kill_pin) == 0){
    resetFunc();
  }
}

void writeBufferToEeprom(){
  int ei = 0;
  for (int b1i=0;b1i<500;b1i++){
    for (int b0i=0;b0i<6;b0i++){
      if (b1i<command_free-1){
        EEPROM.write(ei+1095, command_buffers[b0i][b1i]);
      }
      else if (EEPROM.read(ei+1095)!=0){
        EEPROM.write(ei+1095, 0);
      }
     ei++;
    }
  }
}

void clearEeprom(){
  for (int ei=0;ei<3000;ei++){
    if (EEPROM.read(ei+1095)!=0){
      EEPROM.write(ei+1095, 0);
    }
  }
}

void writeToEeprom(){
  for (int b0i=0;b0i<6;b0i++){
    EEPROM.write(command_active*6+b0i+1095, command_buffers[b0i][0]);
  }
}

void readBufferFromEeprom(){
  running_program = 1;
  int b0i = 0;
  int b1i = 0;
  command_free = 0;
  command_active = 0;

  for (int ei=0;ei<3000;ei++){                      //go throug the eeprom to fill command buffer
    if (b0i==0&&EEPROM.read(ei+1095)==0){           //if a command address is 0 we are at the end
      break;
    }
    command_buffers[b0i][b1i] = EEPROM.read(ei+1095);    //reshape 1x3000 bytes to 6x500
    b0i++;
    if (b0i>5){
      b0i = 0;
      b1i++;
      command_free++;
    }
  }
}

void changeEEPROMSetting(byte pi, byte setting_no, float value){
  int eaddr = pi*38;
  switch (setting_no){
    case 0:                // Kp
      Kps[pi] = value;
      EEPROM.put(eaddr, Kps[pi]);
      myPIDs[pi].SetTunings(Kps[pi], Kis[pi], Kds[pi]);
      break;

    case 1:                // Ki
      Kis[pi] = value;
      EEPROM.put(eaddr+4, Kis[pi]);
      myPIDs[pi].SetTunings(Kps[pi], Kis[pi], Kds[pi]);
      break;

    case 2:                // Kd
      Kds[pi] = value;
      EEPROM.put(eaddr+8, Kds[pi]);
      myPIDs[pi].SetTunings(Kps[pi], Kis[pi], Kds[pi]);
      break;

    case 3:                // step to mm conversions
      motor_calibrations[pi] = value;
      EEPROM.put(eaddr+12, motor_calibrations[pi]);
      break;

    case 4:                // mm to ml conversions
      volume_factors[pi] = value;
      EEPROM.put(eaddr+16, volume_factors[pi]);
      break;

    case 5:                // max steps
      max_steps[pi] = value * motor_calibrations[pi] / volume_factors[pi];
      EEPROM.put(eaddr+20, max_steps[pi]);
      break;

    case 6:                // max speeds
      max_speeds[pi] = value;
      EEPROM.put(eaddr+24, max_speeds[pi]);
      break;

    case 7:                // channel-motor linking
      link[pi] = value;
      EEPROM.put(eaddr+28, link[pi]);
      break;

    case 8:                // pressure coeffs a
      pressure_coeff_as[pi] = value;
      EEPROM.put(eaddr+29, pressure_coeff_as[pi]);
      break;

    case 9:                // pressure coeffs b
      pressure_coeff_bs[pi] = value;
      EEPROM.put(eaddr+33, pressure_coeff_bs[pi]);
      break;

    case 10:                // sensor units
      sensor_units[pi] = value;
      EEPROM.put(eaddr+37, sensor_units[pi]);
      break;
  }
}

void scanSlaves(){
  //Serial.println("START I2C Devices");
  byte error, stype;
  int nDevices = 0;
  for(byte addr = 1; addr < 10; addr++ )
  {
    Wire.beginTransmission(addr);
    error = Wire.endTransmission();
    if (error == 0)
    {
      Wire.requestFrom(addr, (uint8_t)1);    // request 1 bytes from slave device #
      while (Wire.available()) { // slave may send less than requested
        stype = Wire.read(); // receive a byte as character
      }
      //Wire.endTransmission();
      sendValue(0x17, addr, stype);
      if(stype==1){
        Wire.beginTransmission(addr);
        Wire.write(0);
        Wire.write(0);
        Wire.write(0);
        Wire.write(0);
        Wire.write(0x21);
        Wire.write(0);
        Wire.write(0);
        Wire.write(0);
        Wire.write(0);
        Wire.write(0);
        Wire.endTransmission();           
      }
      nDevices++;
    }
  }
}

void listenSlaves(){
  //listen to incoming messages from slaves, send it to serial, handle waition on slaves
}
