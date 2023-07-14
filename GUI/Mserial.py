from math import sqrt, exp
import struct
import serial
import time
from math import log
import numpy as np
import multiprocessing as mp
import queue
from threading import Thread
from threading import Event as tEvent

class M_serial():
    def __init__(self, SER_queues):
        # Define Hex Codes
        self.hex_codes = {
            #message bytes
            "START_BYTE" : b'\xaa',
            "END_BYTE" : b'\x55',

            #program commands
            "setSpeed" : b'\x10', "setTarget" : b'\x11', "setPositionAbs" : b'\x12', 
            "setPositionRel" : b'\x13', "setValve" : b'\x14', "homePump" : b'\x15', 
            "regulate" : b'\x16', "sendToSlave" : b'\x17', "waitTime" : b'\x18',
            "waitVol" : b'\x19', "waitSlave" : b'\x20', "startCycle" : b'\x21', 
            "stopCycle" : b'\x22', "activateAlarm" : b'\x23', "setAlarmValue" : b'\x24', 
            "setAlarmAction" : b'\x25', "soundAlarm" : b'\x26',

            #status commands
            "upload" : b'\x40', "online" : b'\x41', "getPosition" : b'\x42', 
            "getSpeed" : b'\x43', "getPressure" : b'\x44', "clearBuffer" : b'\x45', 
            "readSettings" : b'\x46', "changeSetting" : b'\x47', "commandsBuffered" : b'\x48',
            "reset" : b'\x49'
        }     #add codes for responses?

        # Initializations
        self.ser = None
        self.connected = False
        self.SER_queues = SER_queues
        self.flags = []  # need to implement
        self.pumps = []
        self.serial_buffer = b''

        # Define Machine Settings Link
        self.machine_setting_link = {
            0: "Kp", 1: "Ki", 2: "Kd", 3: "Motor cal (steps/mm)", 4: "Syringe cal (μl/mm)",
            5: "Syringe volume (μl)", 6: "Max speed (mm/sec)", 7: "Active", 8: "Pressure cal A",
            9: "Pressure cal B", 10: "Sensor unit"
        }

        self.command_functions = {
            "Serial_Connect": self.connect,
            "Serial_Disconnect": self.disconnect,
            "Serial_SendSerial": self.send_serial,
            "Serial_Target": self.set_target,
            "Serial_GetPressure": self.get_pressure,
            "Serial_GetPosition": self.get_position,
            "Serial_GetSpeed": self.get_speed,
            "Serial_Home": self.home,
            "Serial_StartAdjust": lambda x: self.regulate(x, 1),
            "Serial_StopAdjust": lambda x: self.regulate(x, 0),
            "Serial_StartConstant": lambda x: self.move_constant(x, 1),
            "Serial_StopConstant": lambda x: self.move_constant(x, 0),
            "Serial_Solenoid": self.set_valve,
            "Serial_Speed": self.set_speed,
            "Serial_MoveRel": self.set_position_rel,
            "Serial_MoveAbs": self.set_position_abs,
            "Serial_SendSettings": self.change_settings,
            "Serial_GetSettings": self.read_settings,
            "Serial_SendSlave": self.send_to_slave,
            "Serial_CommandsBuffered": self.commands_buffered,
            "Serial_StartCycle": self.start_cycle,
            "Serial_StopCycle": self.stop_cycle,
            "Serial_ActivateAlarm": self.activate_alarm,
            "Serial_SetAlarmValue": self.set_alarm_value,
            "Serial_SetAlarmAction": self.set_alarm_action,
            "Serial_SoundAlarm": self.sound_alarm,
            "Serial_Upload": self.upload,
            "Serial_Online": self.online,
            "Serial_WaitTime": self.wait_time,
            "Serial_WaitSlave": self.wait_slave,
            "Serial_WaitVolume": self.wait_volume
        }
        # Define Settings for each Machine Setting
        self.settings = {k: [0] * 5 for k in self.machine_setting_link.values()}
        self.settings_count = 0

        # Define I2C
        self.I2C = {}

        # Create pump instances
        self.pumps = [pump(self, i) for i in range(5)]

        # Create a new thread to handle queue
        self.stop_event_queue = tEvent()        
        self.handleThread = Thread(target=self.handle_queue, args=(self.stop_event_queue, ))
        self.handleThread.start()
        
                
    def connect(self, port, baud):
        self.port = port
        self.baud = baud
    
        if self.port != 'Test':
            self.ser = serial.Serial(
                port=self.port,
                baudrate=self.baud,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=None
            )
        else:
            self.ser = TestSer()
    
            # Define default settings for testing
            self.settings = {
                'Kp': [0.1]*5,
                'Ki': [1e-04]*5,
                'Kd': [1e-04, 1e-04, 0.0, 0.001, 0.001],
                'Motor cal (steps/mm)': [4000.0]*5,
                'Syringe cal (μl/mm)': [642.42426, 369.836]*5,
                'Syringe volume (μl)': [74599.91, 33289.953]*5,
                'Max speed (mm/sec)': [2.5]*5,
                'Active': [1.0]*5,
                'Pressure cal A': [0.018]*5,
                'Pressure cal B': [0.04]*5,
                'Sensor unit': [0.0, 0.0, 255.0, 0.0, 0.0]
            }
            self.SER_queues[1].put(["FromSerial_Settings", self.settings])
    
        self.connected = True
        self.connect_time = time.time()
        self.last_pressure_time = time.time()
        self.SER_queues[1].put(["FromSerial_ConnectSerial", [self.port, self.baud]])

    def disconnect(self):
        try:
            if self.ser is not None and self.ser.is_open:
                self.ser.close()
                time.sleep(1)
                if self.ser.is_open:
                    self.ser.close()
                    time.sleep(1)
                
                
        except Exception as e:
            print ("Serial exit error: " + e)
            
    def kill(self):
        self.stop_event_queue.set()

    def checksum(self, message):
        """
        Calculates the Fletcher checksum from a message.
        The checksum is then appended along with the end byte.
    
        Args:
            message (bytes): The message to compute the checksum from.
    
        Returns:
            bytes: The original message with the computed checksum and end byte appended.
        """
        sum1 = sum2 = 0
        for v in message:
            sum1 = (sum1 + v) % 255
            sum2 = (sum2 + sum1) % 255
    
        checksum = bytes([sum2]) + bytes([sum1])
        return message + checksum + self.hex_codes["END_BYTE"]
        
    def send_serial(self, message):
        """
        Sends a message through the serial port.
    
        Args:
            message (bytes): The message to be sent.
    
        Raises:
            Exception: If the serial port is not connected.
        """
        if self.ser is not None:
            self.ser.write(message)
        else:
            raise Exception("Error: Not connected to a serial port!")
        
    def send_serial_delayed(self, delay, messages):
        """
        Sends a sequence of messages through the serial port with a delay.
    
        Args:
            delay (float): The delay (in seconds) before sending the messages.
            messages (list): A list of messages to be sent.
    
        Raises:
            Exception: If the serial port is not connected.
        """
        if self.ser is not None:
            time.sleep(delay)
            for message in messages:
                self.ser.write(message)
        else:
            raise Exception("Error: Not connected to a serial port!")


    #Serial commands
    """ 
    struct {[START_BYTE][START_BYTE][COMMAND][ADDRESS][PAYLOAD3][PAYLOAD2][PAYLOAD1][PAYLOAD0][CHECKSUM1][CHECKSUM0][END_BYTE]}
        
    setTarget(pumpAddress, targetPressure)	0x10,	Sets a pump group's desired regulation pressure in sensor value (0-1024). Example: setTarget(2, 512).
    setIO(ioAddress, ioValue)	0x11,	Sets an IO to be an input or output. Alias for input/output can also be 0/1, respectively. Example: setIO(2, input).
    setPosition(pumpAddress, distance)	0x12,	Sets a pump's desired position in steps.
    getPosition(pumpAddress)	0x13,	Returns a pump's current distance from home in steps. A pumpAddress of 5 gets all connected pumps' distances Example: getPosition(2)
    startCalibrate(pumpAddress)	0x14,	[To be implemented in future versions.] Begins calibration process, which allows user to change the maximum distance away from home.
    movePump(pumpAddress, distance)	0x15,	Moves a pump by [distance] steps relative from current position. If the given distance will move the pump more than the maximum allowed distance, the command will not execute. A pumpAddress of 5 moves all connected pumps. Example movePump(3, 1000)
    getPressure(pumpAddress)	0x16,	Returns a pump's current pressure in sensor read (0-1024). A pumpAddress of 5 shows all connected pumps' pressures. Example: getPressure(2)
    getIO(ioAddress)	0x17,	Returns current state of an IO - whether it is an input or output, and if an output, whether it is triggered or not. An IOAddress of 5 returns all connected IOs' values. Example: getIO(2)
    triggerIO(ioAddress)	0x18,	If the IO at ioAddress is an output, commands that IO to send a 1 ms pulse. An ioAddress of 5 triggers all IO's set as outputs. Example: triggerIO(2)
    homePump(pumpAddress)	0x19,	Homes all pumps.
    Regulate(state)	0x20,	Start(state=1)/Stop(state=0) regulation of pumps. Example: Regulate(1)
    setValve(valveAddress, valveState)	0x21,	Manually opens or closes a valve. A pumpAddress of 5 opens/closes all valves. If a valve is already at the desired state, the command effectively does nothing. Alias for close/open can also be 0/1, respectively. Example: setValve(2, open)
    setCoupling(couplingState)	0x22,	[To be implemented in future versions.] Manually opens or closes the coupling valve. If the valve is already at the desired state, the command effectively does nothing. Alias for close/open can also be 0/1, respectively. Example: setCoupling(close)
    getFlags()	0x23,	Returns current status flags in human-readable format. The flag bits, in order, are [reserved_bit1, reserved_bit2, reserved_bit3, is_busy, is_regulating, is_homing, trigger_sent, error]. Example: getFlags()
    getError()	0x24,	[To be implemented in future versions.] Returns error code.
    primePumps()	0x25,	Primes the pumps.
    startCycle()	0x26,	Start a cycle
    stopCycle()	0x27,	Primes the pumps.
    wait()	0x28,	Primes the pumps.
    eeprom(state)	0x29,	Write commands to(state =1) or read form (state = 0) EEPROM for stand alone program.
    upload(state)	0x30,	Put controller into upload mode (1), so commands are not executed/(0) finish upload and write to EEPROM
    clearBuffer()	0x31,	Clear command buffer
    setSpeed()	0x32,	set motor speed for channel can be - for home position
    moveConstant()	0x33,	move channel pumps constantly to max or home. set_speed to control speed
    readSetting(pumpAddress, settingAddress)	0x34,	
    changeSetting(pumpAddress, settingAddress, value)	0x35,	
    """

    def set_speed(self, address, target):
        message = self.hex_codes["START_BYTE"] + self.hex_codes["START_BYTE"] + self.hex_codes["setSpeed"] + bytes([address]) + struct.pack("f", target)
        self.send_serial(self.checksum(message))

    def set_target(self, address, target):
        message = self.hex_codes["START_BYTE"] + self.hex_codes["START_BYTE"] + self.hex_codes["setTarget"] + bytes([address]) + struct.pack("f", target)
        self.send_serial(self.checksum(message))

    def set_position_abs(self, address, target):
        message = self.hex_codes["START_BYTE"] + self.hex_codes["START_BYTE"] + self.hex_codes["setPositionAbs"] + bytes([address]) + struct.pack("f", target)
        self.send_serial(self.checksum(message))

    def set_position_rel(self, address, target):
        message = self.hex_codes["START_BYTE"] + self.hex_codes["START_BYTE"] + self.hex_codes["setPositionRel"] + bytes([address]) + struct.pack("f", target)
        self.send_serial(self.checksum(message))

    def set_valve(self, valvenumber,  state):
        message = self.hex_codes["START_BYTE"] + self.hex_codes["START_BYTE"] + self.hex_codes["setValve"] + bytes([valvenumber]) + bytes([state]) + b'\x00\x00\x00'
        self.send_serial(self.checksum(message))

    def home(self, address, direction):
        message = self.hex_codes["START_BYTE"] + self.hex_codes["START_BYTE"] + self.hex_codes["homePump"] + bytes([address]) + bytes([direction]) + b'\x00\x00\x00'               
        self.send_serial(self.checksum(message))

    def regulate(self, address, state):
        message = self.hex_codes["START_BYTE"] + self.hex_codes["START_BYTE"] + self.hex_codes["regulate"] + bytes([address]) + struct.pack("f", state)
        self.send_serial(self.checksum(message))

    def send_to_slave(self, sladdress, command, payload):
        #address: first 5 bytes: slave address, last 3 bytes schedulder address
        message = self.hex_codes["START_BYTE"] + self.hex_codes["START_BYTE"] + self.hex_codes["sendToSlave"] + bytes([sladdress]) + bytes([command]) + bytes([payload[2]]) + bytes([payload[1]]) + bytes([payload[0]]) 
        self.send_serial(self.checksum(message))

    def wait_time(self, seconds):
        message = self.hex_codes["START_BYTE"] + self.hex_codes["START_BYTE"] + self.hex_codes["waitTime"] + b'\x00' + struct.pack("f", seconds)
        self.send_serial(self.checksum(message))

    def wait_slave(self, sladdress, input_num):
        message = self.hex_codes["START_BYTE"] + self.hex_codes["START_BYTE"] + self.hex_codes["waitSlave"] + bytes([sladdress]) + bytes([input_num]) + b'\x00\x00\x00' 
        self.send_serial(self.checksum(message))

    def wait_volume(self, address, volume):
        message = self.hex_codes["START_BYTE"] + self.hex_codes["START_BYTE"] + self.hex_codes["waitVol"] + bytes([address]) + struct.pack("f", volume)
        self.send_serial(self.checksum(message))

    def start_cycle(self, n_cycle):
        message = self.hex_codes["START_BYTE"] + self.hex_codes["START_BYTE"] + self.hex_codes["startCycle"] + b'\x00' + struct.pack("f", n_cycle)
        self.send_serial(self.checksum(message))

    def stop_cycle(self):
        message = self.hex_codes["START_BYTE"] + self.hex_codes["START_BYTE"] + self.hex_codes["stopCycle"] + b'\x00\x00\x00\x00\x00'
        self.send_serial(self.checksum(message))

    def activate_alarm(self, address, alarm_type, state):
        #alarm types: 0 max pressure; 1 min pressure; 2 timeout; 3 max speed; 4 min speed
        #address: first 5 bytes: alarm type, last 3 bytes schedulder address, state:1 active - 0:inactive
        message = self.hex_codes["START_BYTE"] + self.hex_codes["START_BYTE"] + self.hex_codes["activateAlarm"] + bytes([8*alarm_type+address]) + bytes([state]) + b'\x00\x00\x00' 
        self.send_serial(self.checksum(message))

    def set_alarm_value(self, address, alarm_type, value):
        #address: first 5 bytes: alarm type, last 3 bytes schedulder address
        message = self.hex_codes["START_BYTE"] + self.hex_codes["START_BYTE"] + self.hex_codes["setAlarmValue"] + bytes([8*alarm_type+address]) + struct.pack("f", value) 
        self.send_serial(self.checksum(message))

    def set_alarm_action(self, address, alarm_type, action):
        #alarm actions: 0 beep and continue; 1 beep and stop; 2 beep and home;
        #address: first 5 bytes: alarm type, last 3 bytes schedulder address, status:1 active - 0:inactive
        message = self.hex_codes["START_BYTE"] + self.hex_codes["START_BYTE"] + self.hex_codes["activateAlarm"] + bytes([8*alarm_type+address]) + bytes([action])+ b'\x00\x00\x00' 
        self.send_serial(self.checksum(message))

    def sound_alarm(self, state):
        message = self.hex_codes["START_BYTE"] + self.hex_codes["START_BYTE"] + self.hex_codes["soundAlarm"] + b'\x00' + bytes([state])+ b'\x00\x00\x00' 
        self.send_serial(self.checksum(message))

    def upload(self, state):
        message = self.hex_codes["START_BYTE"] + self.hex_codes["START_BYTE"] + self.hex_codes["upload"] + b'\x00' + struct.pack("f", state)
        self.send_serial(self.checksum(message))

    def online(self, state):
        message = self.hex_codes["START_BYTE"] + self.hex_codes["START_BYTE"] + self.hex_codes["online"] + b'\x00' + struct.pack("f", state)
        self.send_serial(self.checksum(message))

    def get_position(self, address):
        message = self.hex_codes["START_BYTE"] + self.hex_codes["START_BYTE"] + self.hex_codes["getPosition"] + bytes([address]) + b'\x00\x00\x00\x00'
        self.send_serial(self.checksum(message))

    def get_speed(self, address):
        message = self.hex_codes["START_BYTE"] + self.hex_codes["START_BYTE"] + self.hex_codes["getSpeed"] + bytes([address]) + b'\x00\x00\x00\x00'
        self.send_serial(self.checksum(message))

    def get_pressure(self, address):
        message = self.hex_codes["START_BYTE"] + self.hex_codes["START_BYTE"] + self.hex_codes["getPressure"] + bytes([address]) + b'\x00\x00\x00\x00'
        self.send_serial(self.checksum(message))

    def clear_buffer(self):
        message = self.hex_codes["START_BYTE"] + self.hex_codes["START_BYTE"] + self.hex_codes["clearBuffer"] + b'\x00\x00\x00\x00\x00'
        self.send_serial(self.checksum(message))

    def read_settings(self):
        message = self.hex_codes["START_BYTE"] + self.hex_codes["START_BYTE"] + self.hex_codes["readSettings"] + b'\x00\x00\x00\x00\x00'
        self.send_serial(self.checksum(message))

    def change_settings(self, settings):
        for pumpAddress in range(5):
            for key in self.machine_setting_link:
                settingAddress = key
                value = settings[self.machine_setting_link[key]][pumpAddress]
                a = self.settings[self.machine_setting_link[settingAddress]][pumpAddress]
                #change only if it's different
                if abs(a - value) > 1e-3 * max(abs(a), abs(value)):
                    self.settings[self.machine_setting_link[settingAddress]][pumpAddress] = value
                    self.change_setting(pumpAddress, settingAddress, value)
                    #do not overwhelm serial communication
                    time.sleep(0.5)
            

    def change_setting(self, pumpAddress, settingAddress, value):
        address = pumpAddress*11 + settingAddress
        message = self.hex_codes["START_BYTE"] + self.hex_codes["START_BYTE"] + self.hex_codes["changeSetting"] + bytes([address]) + struct.pack("f", value)
        self.send_serial(self.checksum(message))

    def commands_buffered(self, address):
        message = self.hex_codes["START_BYTE"] + self.hex_codes["START_BYTE"] + self.hex_codes["commandsBuffered"] + bytes([address]) + b'\x00\x00\x00\x00'
        self.send_serial(self.checksum(message))

    def reset(self, address):
        message = self.hex_codes["START_BYTE"] + self.hex_codes["START_BYTE"] + self.hex_codes["reset"] + b'\x00\x00\x00\x00\x00'
        self.send_serial(self.checksum(message))

    def process_serial(self):
        MINIMUM_LENGTH = 13
        VALUE_INDEX = 4
        VALUE_LENGTH = 4
        
        while len(self.serial_buffer) >= MINIMUM_LENGTH:
            line = self.serial_buffer[:MINIMUM_LENGTH]
            
            
            if not self.is_valid_line(line):
                #print("not valid line ", line)
                self.serial_buffer = b''
                continue
                
            command_type = line[2]
            address = int(line[3])
            value = self.extract_float(line, VALUE_INDEX, VALUE_LENGTH)
            #print (command_type, address, value)
    
            if command_type == self.hex_codes["readSettings"][0]:
                self.process_read_settings(address, value)
            elif command_type == self.hex_codes["getPosition"][0]:
                self.process_get_position(address, value)
            elif command_type == self.hex_codes["getSpeed"][0]:
                self.process_get_speed(address, value)
            elif command_type == self.hex_codes["getPressure"][0]:
                self.process_get_pressure(address, value)
            elif command_type == self.hex_codes["commandsBuffered"][0]:
                self.process_commands_buffered(address, value)
            elif command_type == self.hex_codes["sendToSlave"][0]:
                self.process_send_to_slave(address, value)
    
            self.serial_buffer = self.serial_buffer[MINIMUM_LENGTH:]
    
    def is_valid_line(self, line):
        return (line[0] == self.hex_codes["START_BYTE"][0] and
                line[1] == self.hex_codes["START_BYTE"][0] and
                line[10] == self.hex_codes["END_BYTE"][0])
    
    def extract_float(self, data, start, length):
        return np.float32(struct.unpack("f", data[start : start + length]))[0]
    
    def process_read_settings(self, address, value):
        #print (self.settings_count)
        pumpAddress = address // 11
        settingAddress = address % 11
        self.settings[self.machine_setting_link[settingAddress]][pumpAddress] = value
        #if len(self.serial_buffer) < MINIMUM_LENGTH:
        self.settings_count += 1
        if self.settings_count == 55:
            self.SER_queues[1].put(["FromSerial_Settings", self.settings])
            self.settings_count = 0

    
    def process_get_position(self, pumpAddress, value):
        self.SER_queues[1].put(["FromSerial_Position", [pumpAddress, value]])
    
    def process_get_speed(self, pumpAddress, value):
        self.SER_queues[1].put(["FromSerial_Speed", [pumpAddress, value]])
    
    def process_get_pressure(self, pumpAddress, value):
        self.SER_queues[1].put(["FromSerial_Pressure", [pumpAddress, value]])
    
    def process_commands_buffered(self, pumpAddress, value):
        self.SER_queues[1].put(["FromSerial_Buffer", [pumpAddress, value]])
    
    def process_send_to_slave(self, slaveAddress, value):
        device = {
            1: "24 bit switch board",
            2: "12 bit TTL board",
            3: "8 bit multipinch board",
        }.get(value, "Unknown device")
        
        self.I2C[slaveAddress] = device
        self.SER_queues[1].put(["FromSerial_I2C", self.I2C])        
        
    def handle_queue(self, stop_event):
        while (not stop_event.is_set()):
            self.handle_queue_commands()
            self.handle_serial_input()
            time.sleep(0.05)

    def handle_queue_commands(self):
        try:        
            qsize = self.SER_queues[0].qsize()
            #print(qsize)
            for i in range(qsize):
                command, command_data = self.SER_queues[0].get_nowait()
                #print (command, command_data)
                if "Serial_" not in command:
                    self.SER_queues[0].put([command, command_data])
                    continue
        
                #print("Serial processing")
                #print(command, command_data)
                
                func = self.command_functions.get(command)
                if func is None:
                    print(f"Unhandled command: {command}")
                    continue
        
                func(*command_data)
        except queue.Empty:
            time.sleep(0.05)
            #print("GUI Queue is currently empty. Retrying...")                  

    def handle_serial_input(self):
        if self.ser is None:
            return
        while self.ser.inWaiting() > 0:
            line = self.ser.readline()
            self.serial_buffer = self.serial_buffer + line
            self.process_serial()


class TestSer():
    def __init__(self):
        self.buffer = []
        # self.buffer = [
        # b'START Manatee connected!\r\n',
        # b'END\r\n',
        # b'\xaa\xaaF\x00\xcd\xcc\xcc=\x00\x00U\r\n',
        # b'\xaa\xaaF\x01\x17\xb7\xd18\x00\x00U\r\n',
        # b'\xaa\xaaF\x02\x17\xb7\xd18\x00\x00U\r\n',
        # b'\xaa\xaaF\x03\x00\x00zE\x00\x00U\r\n',
        # b"\xaa\xaaF\x04'\x9b D\x00\x00U\r\n",
        # b'\xaa\xaaF\x05\xf4\xb3\x91G\x00\x00U\r\n',
        # b'\xaa\xaaF\x06\x00\x000@\x00\x00U\r\n',
        # b'\xaa\xaaF\x07\x00\x00\x80?\x00\x00U\r\n',
        # b'\xaa\xaaF\x08\xbct\x93<\x00\x00U\r\n',
        # b'\xaa\xaaF\t\n',
        # b'\xd7#=\x00\x00U\r\n',
        # b'\xaa\xaaF\n',
        # b'\x00\x00\x00\x00\x00\x00U\r\n',
        # b'\xaa\xaaF\x0b\xcd\xcc\xcc=\x00\x00U\r\n',
        # b'\xaa\xaaF\x0c\x17\xb7\xd18\x00\x00U\r\n',
        # b'\xaa\xaaF\r\x17\xb7\xd18\x00\x00U\r\n',
        # b'\xaa\xaaF\x0e\x00\x00zE\x00\x00U\r\n',
        # b'\xaa\xaaF\x0f\x02\xeb\xb8C\x00\x00U\r\n',
        # b'\xaa\xaaF\x10\xf4\t\x02G\x00\x00U\r\n',
        # b'\xaa\xaaF\x11\x00\x00 @\x00\x00U\r\n',
        # b'\xaa\xaaF\x12\x00\x00\x80?\x00\x00U\r\n',
        # b'\xaa\xaaF\x13\xbct\x93<\x00\x00U\r\n',
        # b'\xaa\xaaF\x14\n',
        # b'\xd7#=\x00\x00U\r\n',
        # b'\xaa\xaaF\x15\x00\x00\x00\x00\x00\x00U\r\n',
        # b'\xaa\xaaF\x16\xcd\xcc\xcc=\x00\x00U\r\n',
        # b'\xaa\xaaF\x17\x17\xb7\xd18\x00\x00U\r\n',
        # b'\xaa\xaaF\x18\x00\x00\x00\x00\x00\x00U\r\n',
        # b'\xaa\xaaF\x19\x00\x00zE\x00\x00U\r\n',
        # b'\xaa\xaaF\x1a\x02\xeb\xb8C\x00\x00U\r\n',
        # b'\xaa\xaaF\x1b\xf4\t\x02G\x00\x00U\r\n',
        # b'\xaa\xaaF\x1c\x00\x00 @\x00\x00U\r\n',
        # b'\xaa\xaaF\x1d\x00\x00\x80?\x00\x00U\r\n',
        # b'\xaa\xaaF\x1e\xbct\x93<\x00\x00U\r\n',
        # b'\xaa\xaaF\x1f\n',
        # b'\xd7#=\x00\x00U\r\n',
        # b'\xaa\xaaF \x00\x00\x7fC\x00\x00U\r\n',
        # b'\xaa\xaaF!\xcd\xcc\xcc=\x00\x00U\r\n',
        # b'\xaa\xaaF"\x17\xb7\xd18\x00\x00U\r\n',
        # b'\xaa\xaaF#o\x12\x83:\x00\x00U\r\n',
        # b'\xaa\xaaF$\x00\x00zE\x00\x00U\r\n',
        # b'\xaa\xaaF%\x02\xeb\xb8C\x00\x00U\r\n',
        # b'\xaa\xaaF&\xf4\t\x02G\x00\x00U\r\n',
        # b"\xaa\xaaF'\x00\x00 @\x00\x00U\r\n",
        # b'\xaa\xaaF(\x00\x00\x80?\x00\x00U\r\n',
        # b'\xaa\xaaF)\xbct\x93<\x00\x00U\r\n',
        # b'\xaa\xaaF*\n',
        # b'\xd7#=\x00\x00U\r\n',
        # b'\xaa\xaaF+\x00\x00\x00\x00\x00\x00U\r\n',
        # b'\xaa\xaaF,\xcd\xcc\xcc=\x00\x00U\r\n',
        # b'\xaa\xaaF-\x17\xb7\xd18\x00\x00U\r\n',
        # b'\xaa\xaaF.o\x12\x83:\x00\x00U\r\n',
        # b'\xaa\xaaF/\x00\x00zE\x00\x00U\r\n',
        # b'\xaa\xaaF0\x02\xeb\xb8C\x00\x00U\r\n',
        # b'\xaa\xaaF1\xf4\t\x02G\x00\x00U\r\n',
        # b'\xaa\xaaF2\x00\x00 @\x00\x00U\r\n',
        # b'\xaa\xaaF3\x00\x00\x80?\x00\x00U\r\n',
        # b'\xaa\xaaF4\xbct\x93<\x00\x00U\r\n',
        # b'\xaa\xaaF5\n',
        # b'\xd7#=\x00\x00U\r\n',
        # b'\xaa\xaaF6\x00\x00\x00\x00\x00\x00U\r\n']
        self.hex_codes ={
            "getPosition" : b'\x42',
            "getSpeed" : b'\x43',
            "getPressure" : b'\x44'}


# tetser message: b'\xaa\xaaB\x05\x00\x00\x00\x00\xa6\x9cU' 42
# tetser message: b'\xaa\xaaC\x05\x00\x00\x00\x00\xac\x9dU'43
# tetser message: b'\xaa\xaaD\x05\x00\x00\x00\x00\xb2\x9eU'44

        
    def inWaiting(self):
        return(len(self.buffer))
    def readline(self):
        return self.buffer.pop(0)
    def write(self, message):
        hcode = message[2]
        if hcode == self.hex_codes["getPosition"][0]:
            self.buffer.append(b'\xaa\xaaB\x00\xf4\xb3\x11G\x00\x00U\r\n')
            self.buffer.append(b'\xaa\xaaB\x01\xdd\t\x82F\x00\x00U\r\n')
            self.buffer.append(b'\xaa\xaaB\x02\xdd\t\x82F\x00\x00U\r\n')
            self.buffer.append(b'\xaa\xaaB\x03\xdd\t\x82F\x00\x00U\r\n')
            self.buffer.append(b'\xaa\xaaB\x04\xdd\t\x82F\x00\x00U\r\n')
        elif hcode == self.hex_codes["getSpeed"][0]:
            self.buffer.append(b'\xaa\xaaC\x00\x00\x00\x00\x80\x00\x00U\r\n')
            self.buffer.append(b'\xaa\xaaC\x01\x00\x00\x00\x80\x00\x00U\r\n')
            self.buffer.append(b'\xaa\xaaC\x02\x00\x00\x00\x80\x00\x00U\r\n')
            self.buffer.append(b'\xaa\xaaC\x03\x00\x00\x00\x80\x00\x00U\r\n')
            self.buffer.append(b'\xaa\xaaC\x04\x00\x00\x00\x80\x00\x00U\r\n')
        elif hcode == self.hex_codes["getPressure"][0]:
            self.buffer.append(b'\xaa\xaaD\x00*\x18UB\x00\x00U\r\n')
            self.buffer.append(b'\xaa\xaaD\x01*\x18UB\x00\x00U\r\n')
            self.buffer.append(b'\xaa\xaaD\x02\xba\x1dUB\x00\x00U\r\n')
            self.buffer.append(b'\xaa\xaaD\x03\xba\x1dUB\x00\x00U\r\n')
            self.buffer.append(b'\xaa\xaaD\x04\xba\x1dUB\x00\x00U\r\n')
        #print ("tetser message: %s"%message)


class pump():
    def __init__(self, master, number):  
        self.id = number
        self.master = master   
        self.position = 0
        self.target = 0
        self.speed = 0
        self.time = 0
        self.volume = 0
        self.max_pos = 0
        self.p_history = []
