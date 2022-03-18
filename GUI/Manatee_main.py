import multiprocessing as mp
import Mserial
import sys
import time
import threading
import queue
import start_connection
from PyQt5.QtWidgets import QApplication
from threading import Thread

from threading import Event as tEvent


class ManateeBackend:
    def __init__(self):
        self.MT_queue = mp.Queue()
        self.M_serial = Mserial.M_serial(self.MT_queue)
        # work on sequencer later
        # self.M_sequencer = Msequencer.sequencer(MT_queue)
        self.connected = False
        self.connect_time = None
        self.controller_settings = {}
        self.controller_state_variables = {"Pressures": [0, 0, 0, 0, 0],
                                           "Positions": [0, 0, 0, 0, 0],
                                           "Speeds": [0, 0, 0, 0, 0],
                                           "Regulation_on": [False, False, False, False, False],
                                           "nPumps": 0}
        self.poll_pressure_time = 5
        # self.poll_queue_get()
        self.stop_event_queue = tEvent()
        self.handleThread = Thread(target=self.handle_queue, args=(self.stop_event_queue,))
        self.handleThread.start()
        self.startconn = start_connection.window(self.MT_queue)
        self.QT_app = QApplication(sys.argv)
        self.start_connection = start_connection.MainWindow(self.MT_queue)
        self.start_connection.show()  # shows window
        sys.exit(self.QT_app.exec_())  # clean exit when we close the window

    def connect(self, port, baud):  # connects to a serial port
        global pressures, pres_time, active_ch
        pressures = [[], [], [], [], []]
        pres_time = []
        self.connected = True
        self.connect_time = time.time()
        self.last_pressure_time = time.time()
        self.MT_queue.put(["Serial_Connect", [port, int(baud)]])
        self.poll_controller_states()
        self.serial_connected = False

    def disconnect(self):
        # if self.running_sequence:
        #    self.trig_sequence()
        # self.queue_send.put("SaveSettings")
        self.MT_queue.put(["Serial_Disconnect", None])
        for i in range(self.controller_state_variables["nPumps"]):
            if self.controller_state_variables["Regulation_on"][i]:
                self.trigger_reg(i, True)

    def trigger_reg(self, i, send):
        if self.controller_state_variables["Regulation_on"][i]:
            if send:
                self.putQueueAndSendTerminal("StopAdjust %d" % i)
            self.controller_state_variables["Regulation_on"][i] = False
        else:
            self.setTarget(i)
            self.putQueueAndSendTerminal("StartAdjust %d" % i)
            self.controller_state_variables["Regulation_on"][i] = True

    def stop_threads(self):
        self.stop_event_queue.set()
        self.M_serial.stop_event_queue.set()
        # self.M_sequencer.stop_event_queue.set()

    def handle_queue(self, stop_event):
        # global positions, pos_time, pres_time, active_ch, active_pump, historylength, graphlims, queue_graph
        # print(self.controller_settings)
        while not stop_event.is_set():
            try:
                while True:
                    command, q_data = self.MT_queue.get_nowait()
                    # print (command, q_data)
                    if "FromController_" or "FromGUI_" in command:
                        print("main processing ")
                        if command == "FromController_Settings":
                            self.controller_settings = q_data

                        elif command == "FromController_I2C":
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

                        elif command == "FromController_Pressure":
                            # self.pressureDict [q_data[0]] = q_data[1]
                            # #print (len(self.pressureDict), active_ch)
                            # if len( self.pressureDict) == self.nPumpsActive:
                            #     self.queue_graph.put([time.time()-self.connect_time, self.pressureDict])
                            #     self.pressureDict = {}
                            self.controller_state_variables["Pressures"][q_data[0]] = q_data[1]

                        elif command == "FromController_Position":
                            # self.widgets["slider"+str(q_data[0])].set(q_data[1])
                            self.controller_state_variables["Positions"][q_data[0]] = q_data[1]

                        elif command == "FromController_Speed":
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
                        elif command == "FromGUI_ConnectSerial":
                            self.stop_threads()

                        elif command == "FromGUI_stopThreads":
                            self.connect(q_data[0], q_data[1])

                    else:  # if it's stuff we don't handle put it back
                        self.MT_queue.put([command, q_data])

            except queue.Empty:
                pass

        # poll_queue_get every pressure_time
        # if time.time() > (self.last_pressure_time+self.poll_pressure_time):
        #     self.last_pressure_time = time.time()
        #     self.poll_controller_states()
        # self.master.after(5, self.poll_queue_get)
        # self.poll_queue = threading.Timer(0, self.poll_queue_get).start()

    def poll_controller_states(self):
        self.MT_queue.put(["Serial_GetPressure", 5])
        self.MT_queue.put(["Serial_GetPosition", 5])
        self.MT_queue.put(["Serial_GetSpeed", 5])
        self.poll_controller = threading.Timer(self.poll_pressure_time, self.poll_controller_states).start()


if __name__ == "__main__":
    MB = ManateeBackend()
    # MB.stop_event_queue.set()
    # MB.M_serial.stop_event_queue.set()
