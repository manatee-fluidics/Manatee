import os
import multiprocessing as mp
import Mserial
import sys
import time
import threading
import queue
import pickle
from PyQt5.QtWidgets import QApplication
from threading import Thread

import serial #install w pip install pyserial
import glob
from threading import Event as tEvent

#import main_window
import connection_panel

class ManateeBackend:
    def __init__(self):
        self.GUI_queues = [mp.Queue(), mp.Queue()] #To_GUI and From_GUI
        self.SER_queues = [mp.Queue(), mp.Queue()] #To_Serial and From_Serial
        self.M_serial = Mserial.M_serial(self.SER_queues)
        self.connected = False
        self.connect_time = None
        self.n_pumps = 0
        self.controller_settings = {}
        self.controller_state_variables = {"Pressures" : [0,0,0,0,0], "Positions": [0,0,0,0,0], "Speeds": [0,0,0,0,0]}
        # Open the pickle file in read-binary ("rb") mode
        try:
            with open('gui_settings.p', 'rb') as f:
                # Use pickle.load to load the dictionary
                self.gui_settings = pickle.load(f)
        except:
            self.gui_settings = {'baud': '250000',
                              'waittime': '3000',
                              'pressure': ['20', '10', '20', '20', '20'],
                              'speed': ['2000', '2000', '120', '120', '240'],
                              'volume': ['6000', '-9000', '30', '30', '30'],
                              'time': ['60', '60', '60', '60', '60'],
                              'port': 'Test',
                              'Graph_limits': [500,55]}
            
            with open('gui_settings.p', 'wb') as f:
                # Use pickle.dump to write the dictionary back to the file
                pickle.dump(self.gui_settings, f)
            
        self.poll_pressure_time = 0.5
        self.stop_event_queue_SER = tEvent()
        self.stop_event_queue_GUI = tEvent()
        self.handleThreadSER = Thread(target=self.handle_SER_queues, args=(self.stop_event_queue_SER,))
        self.handleThreadSER.start()
        self.handleThreadGUI = Thread(target=self.handle_GUI_queues, args=(self.stop_event_queue_GUI,))
        self.handleThreadGUI.start()
        
        self.app = QApplication(sys.argv)
        self.startconn = connection_panel.ConnectionWindow(self.controller_settings, self.gui_settings, self.GUI_queues)
        self.startconn.show()
        sys.exit(self.app.exec_())
        #self.poll_controller_states()
        self.connection_panel = connection_panel.ConnectionWindow(self.GUI_queues)
        

    def stop_threads(self):
        with open('gui_settings.p', 'wb') as f:
            # Use pickle.dump to write the dictionary back to the file
            pickle.dump(self.gui_settings, f)
            f.flush()
            os.fsync(f.fileno())
        self.stop_event_queue_SER.set()
        self.stop_event_queue_GUI.set()
        self.M_serial.stop_event_queue.set()
        time.sleep(1)

    def handle_GUI_queues(self, stop_event):
        while not stop_event.is_set():
            try:
                qsize = self.GUI_queues[1].qsize() #Messages From_GUI
                #print(f"From_GUI_queue length is {qsize}  To_GUI_queue length is {self.GUI_queues[0].qsize()}  ")
                for i in range(qsize):
                    command, q_data = self.GUI_queues[1].get_nowait()
                    #print(command)
                    #print (self.controller_settings)
                    #print (self.GUI_queues[1].qsize())
                    if command == "FromGUI_SerialConnect":
                        self.SER_queues[0].put(["Serial_Connect", q_data])
                    elif command == "FromGUI_SerialDisconnect":
                        self.SER_queues[0].put(["Serial_Disconnect", q_data])
                    elif command == "FromGUI_Exit":
                        self.stop_threads()
                    elif command == "FromGUI_GUISettings":
                        self.gui_settings = q_data
                        #print(self.gui_settings)
                        #self.connection_panel.
                    elif command == "FromGUI_ControllerSettings":
                        self.controller_settings = q_data
                        #print(self.gui_settings)
                        #self.connection_panel.
                        self.SER_queues[0].put(["Serial_SendSettings", [self.controller_settings]])
                    elif command == "FromGUI_RunProtocol":
                        pass
                    elif command == "FromGUI_UploadProtocol":
                        pass
                    elif command == "FromGUI_Solenoid":
                        self.SER_queues[0].put(["Serial_Solenoid", q_data])
                    elif command == "FromGUI_Target":
                        self.SER_queues[0].put(["Serial_Target", q_data])
                    elif command == "FromGUI_StopAdjust":
                        self.SER_queues[0].put(["Serial_StopAdjust", q_data])
                    elif command == "FromGUI_StartAdjust":
                        self.SER_queues[0].put(["Serial_StartAdjust", q_data])
                    elif command == "FromGUI_Speed":
                        self.SER_queues[0].put(["Serial_Speed", q_data])
                    elif command == "FromGUI_MoveAbs":
                        self.SER_queues[0].put(["Serial_MoveAbs", q_data])
                    elif command == "FromGUI_MoveRel":
                        self.SER_queues[0].put(["Serial_MoveRel", q_data])
                    elif command == "FromGUI_Home":
                        self.SER_queues[0].put(["Serial_Home", q_data])
                        
                time.sleep(0.1)
            except queue.Empty:
                time.sleep(0.1)  # Wait for 1 second  

    def handle_SER_queues(self, stop_event):
        while not stop_event.is_set():
            #print("running")
            try:
                qsize = self.SER_queues[1].qsize()  #Messages From_Serial
                send_GUI = False #flag for sending messages once we processed everything in From_Serial
                #print(f"FromSER_queue length is {qsize}  ToSER_queue length is {self.SER_queues[0].qsize()}  ")
                for i in range(qsize):
                    command, q_data = self.SER_queues[1].get_nowait()
                    #print([command, q_data])
                    if command == "FromSerial_Settings":
                        #just connected to the controller
                        if len(self.controller_settings) == 0:
                            self.controller_settings = q_data
                            self.n_pumps = len([x for x in q_data["Active"] if x==1])
                            self.GUI_queues[0].put(["ToGUI_SerialConnected", q_data])
                            time.sleep(1)
                            self.poll_controller_states()
                            self.connected = True
                            self.connect_time = time.time()
                        else:
                            self.controller_settings = q_data
                            
                    elif command == "FromSerial_I2C":
                        self.I2C = q_data
                        if "24 bit switch board" in self.I2C.values():
                            # self.widgets["SwitchSlaves"].config(state = NORMAL)
                            pass

                        if "12 bit TTL board" in self.I2C.values():
                            # self.widgets["TTLSlaves"].config(state = NORMAL)
                            pass

                        if "8 bit multipinch board" in self.I2C.values():
                            # self.widgets["PinchSlaves"].config(state = NORMAL)
                            pass

                    elif command == "FromSerial_Pressure":
                        send_GUI = True
                        # self.pressureDict [q_data[0]] = q_data[1]
                        # print (len(self.pressureDict), active_ch)
                        # if len( self.pressureDict) == self.nPumpsActive:
                        #     self.queue_graph.put([time.time()-self.connect_time, self.pressureDict])
                        #     self.pressureDict = {}
                        self.controller_state_variables["Pressures"][q_data[0]] = q_data[1]

                    elif command == "FromSerial_Position":
                        send_GUI = True
                        # self.widgets["slider"+str(q_data[0])].set(q_data[1])
                        self.controller_state_variables["Positions"][q_data[0]] = q_data[1]

                    elif command == "FromSerial_Speed":
                        send_GUI = True
                        self.controller_state_variables["Speeds"][q_data[0]] = q_data[1]
                        # speeds[q_data[0]].append(q_data[1])
                        # spd_mean = 0
                        # if len(speeds[q_data[0]])>4:
                        #     for s in speeds[q_data[0]]:
                        #         spd_mean += s
                        #     spd_mean = spd_mean/len(speeds[q_data[0]])
                        #     self.widgets["speedMeasure"+str(q_data[0])].set(round(spd_mean,6))

                        # if len(speeds[q_data[0]])> 10:
                        #     speeds[q_data[0]].pop(0)
                    #elif command == "FromSerial_ConnectSerial":
                        #self.main_window = threading.Timer(5, self.delayed_mainwindow).start()

                        
                    
                    #elif command == "FromGUI_DisconnectSerial":
                        #self.stop_threads()

                if send_GUI:
                    #print (self.controller_state_variables)
                    mytime = time.time() - self.connect_time
                    #print(["ToGUI_GraphData", [mytime] + self.controller_state_variables["Pressures"][:self.n_pumps]])
                    self.GUI_queues[0].put(["ToGUI_GraphData", [mytime] + self.controller_state_variables["Pressures"][:self.n_pumps]])
                    self.GUI_queues[0].put(["ToGUI_PumpSpeeds", self.controller_state_variables["Speeds"][:self.n_pumps]])
                    self.GUI_queues[0].put(["ToGUI_PumpPositions", self.controller_state_variables["Positions"][:self.n_pumps]])
                    
                time.sleep(0.1)
            except queue.Empty:
                time.sleep(0.1)  # Wait for 1 second  
             

    def poll_controller_states(self):
        self.SER_queues[0].put(["Serial_GetPressure", [5]])
        self.SER_queues[0].put(["Serial_GetPosition", [5]])
        self.SER_queues[0].put(["Serial_GetSpeed", [5]])
        self.poll_controller = threading.Timer(self.poll_pressure_time, self.poll_controller_states).start()
        


if __name__ == "__main__":
    MB = ManateeBackend()

