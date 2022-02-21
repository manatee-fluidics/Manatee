# -*- coding: utf-8 -*-
"""
Created on Tue Feb 07 20:57:35 2017

@author: User
"""
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


"""
overwrite settings:

settings = {}
pumps = [{"pos" : 0,
          "target" : 200,
          "speed" : 1.0,
          "time" : 60,
          "volume" : 1.0,
          "max_pos" : 9000,
          "enabled" : True},
          
          {"pos" : 0,
          "target" : 200,
          "speed" : 1.0,
          "time" : 60,
          "volume" : 1.0,
          "max_pos" : 9000,
          "enabled" : True},
          
          {"pos" : 0,
          "target" : 200,
          "speed" : 1.0,
          "time" : 60,
          "volume" : 1.0,
          "max_pos" : 9000,
          "enabled" : True},
          
          
          {"pos" : 0,
          "target" : 200,
          "speed" : 1.0,
          "time" : 60,
          "volume" : 1.0,
          "max_pos" : 9000,
          "enabled" : True},
          
          
          {"pos" : 0,
          "target" : 200,
          "speed" : 1.0,
          "time" : 60,
          "volume" : 1.0,
          "max_pos" : 9000,
          "enabled" : True}
          ]
          
settings["pumps"] = pumps
settings["port"] = "COM9"
settings["baud"] = "250000"


pickle.dump( settings, open( "save.p", "wb" ) )





queue_in =  mp.Queue()
queue_out =  mp.Queue()

M_serial = M_serial(queue_in, queue_out)
M_serial.connect("COM10", 250000)

M_serial.disconnect()


M_serial.set_alarm_value(0, 1, 5)

M_serial.activate_alarm(0,1,1)

M_serial.sound_alarm (0, 1)
M_serial.sound_alarm (0, 0)

M_serial.home(0)
M_serial.set_speed(0,2.5)
M_serial.set_position_rel(0,20)
M_serial.set_position_abs(0,30)
M_serial.set_target(0,10)
M_serial.regulate(0,1)
M_serial.wait_volume(0,5000)
M_serial.regulate(0,0)
M_serial.wait_time(0,50)
M_serial.regulate(0,0)
M_serial.send_to_slave(0,8,0x21,[0b00000000,0b000011111,0b000000001])              #channel adress (sensor program), slave address, payload
M_serial.send_to_slave(0,8,0x21,[0,0,0])              #channel adress (sensor program), slave address, payload


M_serial.send_to_slave(0,8,[0,0,0b01000001])


M_serial.get_pressure(0)
M_serial.get_position(0)
M_serial.get_speed(0)
M_serial.commands_buffered(0)



M_serial.online(1)
M_serial.set_target(0, 50)
M_serial.start_cycle(0, 0)
M_serial.home(0)
M_serial.regulate(0,1)
M_serial.wait_time(0, 3)
M_serial.send_to_slave(0,8,0x21,[0b00000000,0b000000000,0b0000010000])
M_serial.wait_time(0, 3)
M_serial.send_to_slave(0,8,0x21,[0b00000000,0b000000000,0b0000000000])
M_serial.regulate(0,0)
M_serial.wait_time(0, 3600)
M_serial.stop_cycle(0)
M_serial.online(0)

M_serial.get_position(0)

M_serial.commands_buffered(0)




fixing (1-pfa 2-triton 5-pbs)

M_serial.upload(1)
M_serial.set_target(0, 50)
M_serial.home(0)
M_serial.regulate(0,1)
M_serial.wait_time(0, 60)
M_serial.send_to_slave(0,8,0x21,[0b00000000,0b000000000,0b0000010000])
M_serial.wait_time(0, 120) #60
M_serial.send_to_slave(0,8,0x21,[0b00000000,0b000000000,0b0000000001])
M_serial.wait_time(0, 120) #60
M_serial.send_to_slave(0,8,0x21,[0b00000000,0b000000000,0b0000000000])
M_serial.home(0)
M_serial.wait_time(0, 30*60) #30*60
M_serial.regulate(0,1)
M_serial.wait_time(0, 60)
M_serial.send_to_slave(0,8,0x21,[0b00000000,0b000000000,0b0000010000])
M_serial.wait_time(0, 120) #60
M_serial.send_to_slave(0,8,0x21,[0b00000000,0b000000000,0b0000000010])
M_serial.wait_time(0, 120) #60
M_serial.send_to_slave(0,8,0x21,[0b00000000,0b000000000,0b0000000000])
M_serial.home(0)
M_serial.wait_time(0, 15*60) #15*60
M_serial.regulate(0,1)
M_serial.wait_time(0, 60)
M_serial.send_to_slave(0,8,0x21,[0b00000000,0b000000000,0b0000010000])
M_serial.wait_time(0, 120) #60
M_serial.send_to_slave(0,8,0x21,[0b00000000,0b000000000,0b0000000000])
M_serial.home(0)
M_serial.upload(0)











M_serial.upload(0)
M_serial.home(0)
M_serial.set_target(0, 50)
M_serial.regulate(0,1)
M_serial.wait_time(0, 30)
M_serial.start_cycle(0, 0)

M_serial.send_to_slave(0,8,0x21,[0b00000000,0b000011111,0b000000001])              #channel adress (sensor program), slave address, payload
M_serial.wait_time(0, 30)


M_serial.send_to_slave(0,8,0x21,[0b00000000,0b000000010,0b0000000010])
M_serial.wait_time(0, 10)
M_serial.send_to_slave(0,8,0x21,[0b00000000,0b000000001,0b0000000001])
M_serial.wait_time(0, 10)

M_serial.send_to_slave(0,8,0x21,[0b00000000,0b000000100,0b0000000100])
M_serial.wait_time(0, 10)
M_serial.send_to_slave(0,8,0x21,[0b00000000,0b000000001,0b0000000001])
M_serial.wait_time(0, 10)

M_serial.send_to_slave(0,8,0x21,[0b00000000,0b000001000,0b0000001000])
M_serial.wait_time(0, 10)
M_serial.send_to_slave(0,8,0x21,[0b00000000,0b000000001,0b0000000001])
M_serial.wait_time(0, 10)

M_serial.send_to_slave(0,8,0x21,[0b00000000,0b000010000,0b0000000010])
M_serial.wait_time(0, 10)
M_serial.send_to_slave(0,8,0x21,[0b00000000,0b000000001,0b0000000001])
M_serial.wait_time(0, 10)

M_serial.send_to_slave(0,8,0x21,[0b00000000,0b000000010,0b0000000100])
M_serial.wait_time(0, 10)
M_serial.send_to_slave(0,8,0x21,[0b00000000,0b000000001,0b0000000001])
M_serial.wait_time(0, 10)

M_serial.send_to_slave(0,8,0x21,[0b00000000,0b000000100,0b0000001000])
M_serial.wait_time(0, 10)
M_serial.send_to_slave(0,8,0x21,[0b00000000,0b000000001,0b0000000001])
M_serial.wait_time(0, 10)

M_serial.send_to_slave(0,8,0x21,[0b00000000,0b000001000,0b0000000010])
M_serial.wait_time(0, 10)
M_serial.send_to_slave(0,8,0x21,[0b00000000,0b000000001,0b0000000001])
M_serial.wait_time(0, 10)

M_serial.send_to_slave(0,8,0x21,[0b00000000,0b000010000,0b0000000100])
M_serial.wait_time(0, 1)
M_serial.send_to_slave(0,8,0x21,[0b00000000,0b000000001,0b0000000001])
M_serial.wait_time(0, 30)

M_serial.stop_cycle(0)
M_serial.upload(1)
M_serial.upload(0)
M_serial.eeprom(1)


M_serial.send_to_slave(0,8,0x21,[0b00000000,0b000000000,0b0000000001])
M_serial.send_to_slave(0,8,0x21,[0b00000000,0b000000000,0b0000000010])
M_serial.send_to_slave(0,8,0x21,[0b00000000,0b000000000,0b0000000100])
M_serial.send_to_slave(0,8,0x21,[0b00000000,0b000000000,0b0000001000])
M_serial.send_to_slave(0,8,0x21,[0b00000000,0b000000000,0b0000010000])

M_serial.send_to_slave(0,8,0x21,[0b00000000,0b000000000,0b0000000000])

M_serial.send_to_slave(0,8,0x21,[0b00000000,0b000000000,0b0000011111])

M_serial.set_target(0, 50)
M_serial.regulate(0,1)
M_serial.regulate(0,0)
M_serial.home(0)


M_serial.get_position(0)



M_serial.upload(1)
M_serial.home(0)
M_serial.set_target(0, 10)
M_serial.regulate(0,1)
M_serial.wait_time(0, 3)
M_serial.start_cycle(0, 3)

M_serial.send_to_slave(0,8,[0,0,0b01000001])
M_serial.wait_time(0, 10)
M_serial.send_to_slave(0,8,[0,0,0b01110001])
M_serial.wait_time(0, 10)
M_serial.send_to_slave(0,8,[0,0,0b01110000])
M_serial.wait_time(0, 3)
M_serial.send_to_slave(0,8,[0,0,0b00000000])
M_serial.wait_time(0, 4)


M_serial.send_to_slave(0,8,[0,0,0b00010010])
M_serial.wait_time(0, 10)
M_serial.send_to_slave(0,8,[0,0,0b00010000])
M_serial.wait_time(0, 3)
M_serial.send_to_slave(0,8,[0,0,0b01000001])
M_serial.wait_time(0, 10)
M_serial.send_to_slave(0,8,[0,0,0b00000000])
M_serial.wait_time(0, 3)

M_serial.send_to_slave(0,8,[0,0,0b00100100])
M_serial.wait_time(0, 10)
M_serial.send_to_slave(0,8,[0,0,0b00100000])
M_serial.wait_time(0, 3)
M_serial.send_to_slave(0,8,[0,0,0b01000001])
M_serial.wait_time(0, 10)
M_serial.send_to_slave(0,8,[0,0,0b00000000])
M_serial.wait_time(0, 3)

M_serial.stop_cycle(0)
M_serial.upload(0)
















M_serial.send_to_slave(0,8,0x21,[0,0,0b01110001])





M_serial.change_setting(0, 0, 0.1)
M_serial.change_setting(0, 1, 0.0001)
M_serial.change_setting(0, 2, 0.0001)
M_serial.change_setting(0, 3, 4000)
M_serial.change_setting(0, 4, 1)
M_serial.change_setting(0, 4, 0.369836)
M_serial.change_setting(0, 5, 33.28524)
M_serial.change_setting(0, 6, 2.5)
M_serial.change_setting(4, 7, 6)      #linking
M_serial.change_setting(4, 8, 0.018)
M_serial.change_setting(4, 9, 0.04)
M_serial.change_setting(4, 10, 0)

M_serial.change_setting(0, 7, 1)
M_serial.change_setting(1, 7, 0)
M_serial.change_setting(2, 7, 0)
M_serial.change_setting(3, 7, 0)
M_serial.change_setting(4, 7, 0)









M_serial.get_position(0)
M_serial.regulate(0,1)
M_serial.regulate(0)
M_serial.set_position(2, 70000)
M_serial.home()
M_serial.set_target(0,10)
M_serial.set_valve(1,1)
M_serial.set_valve(1,0)
M_serial.wait(10)
M_serial.get_pressure(0b00000001)

M_serial.clear_buffer()



M_serial.upload(0)
M_serial.set_target(0, 32.14532452462)
M_serial.start_cycle(24)
M_serial.home()
M_serial.regulate(1)
M_serial.wait(60)
M_serial.set_valve(2,1)
M_serial.wait(30)
M_serial.set_valve(2,0)
M_serial.regulate(0)
M_serial.wait(60*60*4)
M_serial.stop_cycle()
M_serial.upload(1)
M_serial.eeprom(1)


M_serial.eeprom(1)
M_serial.eeprom(0)


M_serial.upload(0)
M_serial.upload(1)

M_serial.clear_buffer()




M_serial.upload(0)
M_serial.set_target(0, 10)
M_serial.set_target(1, 20)
M_serial.regulate(1)
M_serial.wait(60)
M_serial.start_cycle(0)
M_serial.set_valve(1,1)
M_serial.wait(30)
M_serial.set_valve(1,0)
M_serial.wait(1)
M_serial.set_valve(2,1)
M_serial.wait(15)
M_serial.set_valve(2,0)
M_serial.wait(1)
M_serial.stop_cycle()
M_serial.upload(1)
M_serial.eeprom(1)



M_serial.upload(0)
M_serial.start_cycle(5)
M_serial.wait(5)
M_serial.set_valve(2,1)
M_serial.wait(5)
M_serial.set_valve(2,0)
M_serial.stop_cycle()
M_serial.upload(1)
M_serial.eeprom(1)


"""












"""
struct {[START_BYTE][START_BYTE][COMMAND][ADDRESS][PAYLOAD3][PAYLOAD2][PAYLOAD1][PAYLOAD0][CHECKSUM1][CHECKSUM0][END_BYTE]}

setTarget(pumpAddress, targetPressure)	       	0x10,			Sets a pump group's desired regulation pressure in sensor value (0-1024). Example: setTarget(2, 512). 
setIO(ioAddress, ioValue)					0x11,			Sets an IO to be an input or output. Alias for input/output can also be 0/1, respectively.	 Example: setIO(2, input). 	
setPosition(pumpAddress, distance)                 0x12,			Sets a pump's desired position in steps.
getPosition(pumpAddress)					0x13,			Returns a pump's current distance from home in steps. A pumpAddress of 5 gets all connected pumps' distances Example: getPosition(2)
startCalibrate(pumpAddress)					0x14,			[Not implemented] Begins calibration process, which allows user to change the maximum distance away from home.
movePump(pumpAddress, distance)		           0x15,			Moves a pump by [distance] steps relative from current position. If the given distance will move the pump more than the maximum allowed distance, the command will not execute. A pumpAddress of 5 moves all connected pumps. Example movePump(3, 1000)
getPressure(pumpAddress)					0x16,			Returns a pump's current pressure in sensor read (0-1024). A pumpAddress of 5 shows all connected pumps' pressures. Example: getPressure(2)
getIO(ioAddress)							0x17,			Returns current state of an IO - whether it is an input or output, and if an output, whether it is triggered or not. An IOAddress of 5 returns all connected IOs' values. Example: getIO(2) 
triggerIO(ioAddress)						0x18,			If the IO at ioAddress is an output, commands that IO to send a 1 ms pulse. An ioAddress of 5 triggers all IO's set as outputs. Example: triggerIO(2) 
homePump(pumpAddress)						0x19,			Homes all pumps.
Regulate(state)				                 0x20,			Start(state=1)/Stop(state=0) regulation of pumps. Example: Regulate(1)
setValve(valveAddress, valveState)			     0x21,			Manually opens or closes a valve. A pumpAddress of 5 opens/closes all valves. If a valve is already at the desired state, the command effectively does nothing. Alias for close/open can also be 0/1, respectively.  Example: setValve(2, open) 
setCoupling(couplingState)					0x22,			[Not implemented] Manually opens or closes the coupling valve. If the valve is already at the desired state, the command effectively does nothing. Alias for close/open can also be 0/1, respectively.  Example: setCoupling(close)
getFlags()								0x23,			Returns current status flags in human-readable format. The flag bits, in order, are [reserved_bit1, reserved_bit2, reserved_bit3, is_busy, is_regulating, is_homing, trigger_sent, error]. Example: getFlags()
getError()								0x24,			[Not implemented] Returns error code.
primePumps()							0x25,			Primes the pumps.
startCycle()							0x26,			Start a cycle
stopCycle()							      0x27,			Primes the pumps.
wait()							      0x28,			Primes the pumps.
eeprom(state)						     0x29,			Write commands to(state =1) or read form (state = 0) EEPROM for stand alone program.
upload(state)						     0x30,			Put controller into upload mode (1), so commands are not executed/(0) finish upload and write to EEPROM
clearBuffer()						     0x31,			Clear command buffer
setSpeed()						           0x32,			set motor speed for channel can be - for home position
moveConstant()						      0x33,			move channel pumps constantly to max or home. set_speed to control speed
readSetting(pumpAddress, settingAddress)		0x34,			
changeSetting(pumpAddress, settingAddress, value)  0x35,			
"""





class M_serial():
    def __init__(self, MT_queue):
        self.hex_codes = {
                  #message bytes
                  "START_BYTE" : b'\xaa',
                  "END_BYTE" : b'\x55',
                  
                  #program commands
                  "setSpeed" : b'\x10',
                  "setTarget" : b'\x11',
                  "setPositionAbs" : b'\x12',
                  "setPositionRel" : b'\x13',
                  "setValve" : b'\x14',
                  "homePump" : b'\x15',
                  "regulate" : b'\x16',
                  "sendToSlave" : b'\x17',                  
                  "waitTime" : b'\x18',
                  "waitVol" : b'\x19',                 
                  "waitSlave" : b'\x20',                 
                  "startCycle" : b'\x21',
                  "stopCycle" : b'\x22',
                  "activateAlarm" : b'\x23',
                  "setAlarmValue" : b'\x24',
                  "setAlarmAction" : b'\x25',
                  "soundAlarm" : b'\x26',

                  

                  #status commands
                  "upload" : b'\x40',
                  "online" : b'\x41',
                  "getPosition" : b'\x42',
                  "getSpeed" : b'\x43',
                  "getPressure" : b'\x44',
                  "clearBuffer" : b'\x45',
                  "readSettings" : b'\x46',
                  "changeSetting" : b'\x47',
                  "commandsBuffered" : b'\x48',
                  "reset" : b'\x49'}     #add codes for responses?

        self.ser = None
        self.MT_queue = MT_queue
        self.flags = [] #need to implement
        self.pumps = []
        self.serial_buffer = b''
        self.machine_setting_link = {  0:"Kps",
                                       1:"Kis",
                                       2:"Kds",
                                       3:"motor_calibs",
                                       4:"volume_factors",
                                       5:"max_steps",
                                       6:"max_speeds",
                                       7:"active",
                                       8:"pressure_coeff_as",
                                       9:"pressure_coeff_bs",
                                       10:"sensor_units"}
        self.settings = {}
        for k in self.machine_setting_link.values():
            self.settings[k] = [0] * 5
        self.I2C = {}
        
        
        for i in range(5):
            self.pumps.append(pump(self, i))
        
        
        #handle queue thread: deals with commands coming from other threads
        self.stop_event_queue = tEvent()        
        self.handleThread = Thread(target = self.handle_queue, args=(self.stop_event_queue, ))
        self.handleThread.start()
        
                
    def connect(self, port, baud):
        self.port = port
        self.baud = baud
        
        if self.port == 'Test':
            self.ser = TestSer()
        else:
            self.ser = serial.Serial(
                port=self.port,
                baudrate=self.baud,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=None)
        
        #self.stop_event_monitor = tEvent()
        #self.monitorThread = Thread(target = self.monitor_thread, args=(self.stop_event_monitor, ))
        #self.monitorThread.start()
        
        
        #question does the firmware send a response?

    def disconnect(self):
        if self.ser != None:
            self.ser.close()
            #self.stop_event_monitor.set()
            self.ser = None
            
    def kill(self):
        self.stop_event_queue.set()

    def checksum(self, message):
        """calculates fletcher checksum from hex string and appends it with the end byte"""
        sum1 = sum2 = 0
        for v in message:
            sum1 = (sum1 + v) % 255
            sum2 = (sum2 + sum1) % 255

        return message + bytes([sum2]) + bytes([sum1]) + self.hex_codes["END_BYTE"]
        
    def send_serial(self, message):
        if self.ser != None:
            #print "sent to firmware: "
            #print message
            #print [bytes([ord(x)) for x in message]
            self.ser.write(message)
            #time.sleep(10)
        else:
            print ("Error, not connected!")
        
    def send_serial_delayed(self, delay, messages):
        if self.ser != None:
            time.sleep(delay)
            for message in messages:
                self.ser.write(message)
        else:
            print ("Error, not connected!")





    #Serial commands
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
        line = self.serial_buffer
        #print(line)
        if len(line) >= 13:
            if line[0] == self.hex_codes["START_BYTE"][0] and line[1] == self.hex_codes["START_BYTE"][0] and line[10] == self.hex_codes["END_BYTE"][0]:
                if line[2] == self.hex_codes["readSettings"][0]:
                    pumpAddress = int(line[3]/11)
                    settingAddress = int(line[3]%11)
                    value = np.float32(struct.unpack("f", line[4:8]))[0]
                    self.settings[self.machine_setting_link[settingAddress]][pumpAddress] = value
                    self.MT_queue.put(["FromController_Settings", self.settings])
                    
                elif line[2] == self.hex_codes["getPosition"][0]:
                    pumpAddress = int(line[3])
                    value = np.float32(struct.unpack("f", line[4:8]))[0]
                    self.MT_queue.put(["FromController_Position", [pumpAddress, value]])

                elif line[2] == self.hex_codes["getSpeed"][0]:
                    pumpAddress = int(line[3])
                    value = np.float32(struct.unpack("f", line[4:8]))[0]
                    self.MT_queue.put(["FromController_Speed", [pumpAddress, value]])

                elif line[2] == self.hex_codes["getPressure"][0]:
                    pumpAddress = int(line[3])
                    value = np.float32(struct.unpack("f", line[4:8]))[0]
                    self.MT_queue.put(["FromController_Pressure", [pumpAddress, value]])
                    
                elif line[2] == self.hex_codes["commandsBuffered"][0]:
                    pumpAddress = int(line[3])
                    value = np.float32(struct.unpack("f", line[4:8]))[0]
                    self.MT_queue.put(["FromController_Buffer", [pumpAddress, value]])

                elif line[2] == self.hex_codes["sendToSlave"][0]:
                    slaveAddress = int(line[3])
                    value = np.float32(struct.unpack("f", line[4:8]))[0]
                    if value == 1:                        
                        device = "24 bit switch board"
                    elif value == 2:
                        device = "12 bit TTL board"
                    elif value == 3:
                        device = "8 bit multipinch board"
                        
                    self.I2C[slaveAddress] = device
                    self.MT_queue.put(["FromController_I2C", self.I2C])

                self.serial_buffer = self.serial_buffer[13:]
            else:
                self.serial_buffer = b''
        
        
    def handle_queue(self, stop_event):
        while (not stop_event.is_set()):
            #handle commands coming from threads
            try:
                while True:
                    command, q_data = self.MT_queue.get_nowait()
                    #print (command, q_data)
                    if "Serial_" in command:
                        print ("Serial processing ")
                        if command == "Serial_Connect":
                            self.connect(q_data[0], int(q_data[1]))
    
                        elif command == "Serial_Disconnect":
                            self.disconnect()
    
                        elif command == "Serial_SendSerial":
                            self.send_serial(q_data)
    
                        if command == "Serial_Target":
                            self.set_target(int(q_data[0]), float(q_data[1]))
                        
                        elif command == "Serial_GetPressure":
                            self.get_pressure(int(q_data))
                        
                        elif command == "Serial_GetPosition":
                            self.get_position(int(q_data))
                        
                        elif command == "Serial_GetSpeed":
                            self.get_speed(int(q_data))
                        
                        elif command == "Serial_Home":
                            self.home(int(q_data[0]), int(q_data[1]))                        
    
                        elif command == "Serial_StartAdjust":
                            self.regulate(int(q_data[0]), 1)
                                
                        elif command == "Serial_StopAdjust":
                            self.regulate(int(q_data[0]), 0)
    
                        elif command == "Serial_StartConstant":
                            self.move_constant(int(q_data[0]), 1)
                                
                        elif command == "Serial_StopConstant":
                            self.move_constant(int(q_data[0]), 0)
                                
                        elif command == "Serial_Solenoid":
                            self.set_valve(int(q_data[0]), int(q_data[1]))                        
    
                        elif command == "Serial_Speed":
                            self.set_speed(int(q_data[0]), float(q_data[1]))                        
                                
                        elif command == "Serial_MoveRel":
                            self.set_position_rel(int(q_data[0]), float(q_data[1]))
    
                        elif command == "Serial_MoveAbs":
                            self.set_position_abs(int(q_data[0]), float(q_data[1]))
    
                        elif command == "Serial_SendSetting":
                            self.change_setting(int(q_data[0]), int(q_data[1]), float(q_data[2]))
    
                        elif command == "Serial_GetSettings":
                            self.read_settings()
    
                        elif command == "Serial_SendSlave":
                            #slaveaddress = int(line.split(" ")[1])
                            #command = int(line.split(" ")[2])
                            #data = [int(x) for x in line.split(" ")[3:6]]
                            self.send_to_slave(int(q_data[0]), int(q_data[1]), q_data[2])
    
                        elif command == "Serial_CommandsBuffered":
                            self.commands_buffered(int(q_data[0]))
    
                        elif command == "Serial_StartCycle":
                            self.start_cycle(int(q_data[0]))
    
                        elif command == "Serial_StopCycle":
                            self.stop_cycle()
    
                        elif command == "Serial_ActivateAlarm":
                            self.activate_alarm(int(q_data[0]), int(q_data[1]), int(q_data[2]))
    
                        elif command == "Serial_SetAlarmValue":
                            self.set_alarm_value(int(q_data[0]), int(q_data[1]), float(q_data[2]))
    
                        elif command == "Serial_SetAlarmAction":
                            self.set_alarm_action(int(q_data[0]), int(q_data[1]), int(q_data[2]))
    
                        elif command == "Serial_SoundAlarm":
                            self.sound_alarm(int(q_data[0]))
    
                        elif command == "Serial_Upload":
                            self.upload(int(q_data[0]))
    
                        elif command == "Serial_Online":
                            self.online(int(q_data[0]))
                            #print("online")
    
                        elif command == "Serial_WaitTime":
                            self.wait_time(float(q_data[0]))
    
                        elif command == "Serial_WaitSlave":
                            self.wait_slave(int(q_data[0]), int(q_data[1]))
    
                        elif command == "Serial_WaitVolume":
                            self.wait_volume(int(q_data[0]), float(q_data[1]))

                    else:                                                   #if it's stuff we don't handle put it back
                        self.MT_queue.put([command, q_data])
            except:
                pass
            
            #if connected handle serial coming from firmware
            if self.ser != None:
                while self.ser.inWaiting() > 0:
                    line = self.ser.readline()
                    self.serial_buffer = self.serial_buffer+line
                    self.process_serial()
                    #print(line)
                    
                    """
                    if line.split(" ")[0]=="START":
                        self.serial_buffer = []
                    if 'END\r\n' in line:
                        self.serial_buffer.append(line)
                        self.process_serial()
                                               
                    self.serial_buffer.append(line)
                    """
                    

            
            
            #time.sleep(0.01)
class TestSer():
    def __init__(self):
        self.buffer = [
        b'START Manatee connected!\r\n',
        b'END\r\n',
        b'\xaa\xaaF\x00\xcd\xcc\xcc=\x00\x00U\r\n',
        b'\xaa\xaaF\x01\x17\xb7\xd18\x00\x00U\r\n',
        b'\xaa\xaaF\x02\x17\xb7\xd18\x00\x00U\r\n',
        b'\xaa\xaaF\x03\x00\x00zE\x00\x00U\r\n',
        b"\xaa\xaaF\x04'\x9b D\x00\x00U\r\n",
        b'\xaa\xaaF\x05\xf4\xb3\x91G\x00\x00U\r\n',
        b'\xaa\xaaF\x06\x00\x000@\x00\x00U\r\n',
        b'\xaa\xaaF\x07\x00\x00\x80?\x00\x00U\r\n',
        b'\xaa\xaaF\x08\xbct\x93<\x00\x00U\r\n',
        b'\xaa\xaaF\t\n',
        b'\xd7#=\x00\x00U\r\n',
        b'\xaa\xaaF\n',
        b'\x00\x00\x00\x00\x00\x00U\r\n',
        b'\xaa\xaaF\x0b\xcd\xcc\xcc=\x00\x00U\r\n',
        b'\xaa\xaaF\x0c\x17\xb7\xd18\x00\x00U\r\n',
        b'\xaa\xaaF\r\x17\xb7\xd18\x00\x00U\r\n',
        b'\xaa\xaaF\x0e\x00\x00zE\x00\x00U\r\n',
        b'\xaa\xaaF\x0f\x02\xeb\xb8C\x00\x00U\r\n',
        b'\xaa\xaaF\x10\xf4\t\x02G\x00\x00U\r\n',
        b'\xaa\xaaF\x11\x00\x00 @\x00\x00U\r\n',
        b'\xaa\xaaF\x12\x00\x00\x80?\x00\x00U\r\n',
        b'\xaa\xaaF\x13\xbct\x93<\x00\x00U\r\n',
        b'\xaa\xaaF\x14\n',
        b'\xd7#=\x00\x00U\r\n',
        b'\xaa\xaaF\x15\x00\x00\x00\x00\x00\x00U\r\n',
        b'\xaa\xaaF\x16\xcd\xcc\xcc=\x00\x00U\r\n',
        b'\xaa\xaaF\x17\x17\xb7\xd18\x00\x00U\r\n',
        b'\xaa\xaaF\x18\x00\x00\x00\x00\x00\x00U\r\n',
        b'\xaa\xaaF\x19\x00\x00zE\x00\x00U\r\n',
        b'\xaa\xaaF\x1a\x02\xeb\xb8C\x00\x00U\r\n',
        b'\xaa\xaaF\x1b\xf4\t\x02G\x00\x00U\r\n',
        b'\xaa\xaaF\x1c\x00\x00 @\x00\x00U\r\n',
        b'\xaa\xaaF\x1d\x00\x00\x80?\x00\x00U\r\n',
        b'\xaa\xaaF\x1e\xbct\x93<\x00\x00U\r\n',
        b'\xaa\xaaF\x1f\n',
        b'\xd7#=\x00\x00U\r\n',
        b'\xaa\xaaF \x00\x00\x7fC\x00\x00U\r\n',
        b'\xaa\xaaF!\xcd\xcc\xcc=\x00\x00U\r\n',
        b'\xaa\xaaF"\x17\xb7\xd18\x00\x00U\r\n',
        b'\xaa\xaaF#o\x12\x83:\x00\x00U\r\n',
        b'\xaa\xaaF$\x00\x00zE\x00\x00U\r\n',
        b'\xaa\xaaF%\x02\xeb\xb8C\x00\x00U\r\n',
        b'\xaa\xaaF&\xf4\t\x02G\x00\x00U\r\n',
        b"\xaa\xaaF'\x00\x00 @\x00\x00U\r\n",
        b'\xaa\xaaF(\x00\x00\x80?\x00\x00U\r\n',
        b'\xaa\xaaF)\xbct\x93<\x00\x00U\r\n',
        b'\xaa\xaaF*\n',
        b'\xd7#=\x00\x00U\r\n',
        b'\xaa\xaaF+\x00\x00\x00\x00\x00\x00U\r\n',
        b'\xaa\xaaF,\xcd\xcc\xcc=\x00\x00U\r\n',
        b'\xaa\xaaF-\x17\xb7\xd18\x00\x00U\r\n',
        b'\xaa\xaaF.o\x12\x83:\x00\x00U\r\n',
        b'\xaa\xaaF/\x00\x00zE\x00\x00U\r\n',
        b'\xaa\xaaF0\x02\xeb\xb8C\x00\x00U\r\n',
        b'\xaa\xaaF1\xf4\t\x02G\x00\x00U\r\n',
        b'\xaa\xaaF2\x00\x00 @\x00\x00U\r\n',
        b'\xaa\xaaF3\x00\x00\x80?\x00\x00U\r\n',
        b'\xaa\xaaF4\xbct\x93<\x00\x00U\r\n',
        b'\xaa\xaaF5\n',
        b'\xd7#=\x00\x00U\r\n',
        b'\xaa\xaaF6\x00\x00\x00\x00\x00\x00U\r\n']
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
