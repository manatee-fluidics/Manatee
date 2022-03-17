import multiprocessing as mp
import sys
import serial
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QLabel, \
    QComboBox, QGridLayout, QDesktopWidget
from PyQt5.QtCore import Qt
from PyQt5 import QtGui, QtCore
import glob

import main_window


class MainWindow(QMainWindow):  # inherits all properties from QMainWindow class
    """Creates Main Window with all functions."""
    def __init__(self, MT_queue):  # this will run whenever we create an instance of the MainWindow class
        super(MainWindow, self).__init__()  # parent constructor

        # QMainWindow has a central widget that is a container for widgets, it has its own layout
        # create cw, set layout and alignment
        self.setCentralWidget(QWidget(self))
        cw_layout = QVBoxLayout()
        cw_layout.setAlignment(Qt.AlignCenter)
        self.centralWidget().setLayout(cw_layout)

        self.MT_queue = MT_queue

        # call layout elements
        self.logo = Logo()
        self.connections = Connections(self, MT_queue)

        # add layout elements to cw - name, alignment
        cw_layout.addWidget(self.logo, Qt.AlignCenter)
        cw_layout.addWidget(self.connections, Qt.AlignCenter)

        self.initUI()

    def initUI(self):
        """Initializes the Main window with all the attributes specified below."""

        self.setWindowTitle("Manatee Fluidics")
        self.setWindowIcon(QIcon("manatee_icon_square.png"))
        # self.setGeometry(1300, 200, 1000, 1500)
        # xpos, ypos, width, height (in pixels)
        # if xpos and ypos are 0, win shows up on the top-left corner;
        # 100, 100 moves the top-left corner of the window to the right and down
        self.center()  # open window in the center of the screen

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


class Logo(QLabel):
    """Displays Manatee logo in Main Window, over connection panel"""
    def __init__(self):
        super(Logo, self).__init__()
        self.setAlignment(Qt.AlignCenter)
        self.pixmap = QPixmap("manatee_logo_big.png")
        self.pixmap_resized = self.pixmap.scaledToHeight(400)
        self.setPixmap(self.pixmap_resized)


class Connections(QWidget):
    """Connection panel. Displays refresh button, available ports in dropdown menu, connect button
    and textbox which let's the user know about what the program is doing."""
    def __init__(self, cp_window, MT_queue):
        super(Connections, self).__init__()

        self.MT_queue = MT_queue
        self.connection_panel_window = cp_window
        self.conn_layout = QGridLayout(self)

        # define refresh button
        self.button_refresh = QPushButton()
        self.button_refresh.setIcon(QtGui.QIcon("refresh_icon.png"))
        self.button_refresh.setIconSize(QtCore.QSize(30, 30))
        self.button_refresh.setToolTip("Refresh port list")
        self.button_refresh.clicked.connect(lambda: self.refresh_click())  # or self.refresh_click

        # define dropdown menu
        self.dropdown = QComboBox(self)
        self.dropdown.setEditable(True)
        self.dropdown.lineEdit().setReadOnly(True)
        self.dropdown.lineEdit().setAlignment(Qt.AlignCenter)
        self.dropdown.setFixedSize(100, 36)  # width, height

        # assemble connection list from serial ports and add elements to dropdown menu
        for port in self.serial_ports():
            self.dropdown.addItem(port)

        # define connection button
        self.button_connect = QPushButton()
        self.button_connect.setText("Connect")
        self.button_connect.setFixedSize(100, 38)
        self.button_connect.clicked.connect(lambda: self.connect_click())

        # define message display
        self.textbox = QLabel(self)
        self.textbox.setText("Welcome")
        self.textbox.setAlignment(Qt.AlignCenter)

        # add all above defines elements to Connections bar
        # (name, starting row, starting col, rowspan, colspan (till the end is -1), alignment)
        self.conn_layout.addWidget(self.button_refresh, 0, 0, 1, 1, Qt.AlignLeft)
        self.conn_layout.addWidget(self.dropdown, 0, 1, 1, 1, Qt.AlignCenter)
        self.conn_layout.addWidget(self.button_connect, 0, 2, 1, 1, Qt.AlignRight)
        self.conn_layout.addWidget(self.textbox, 1, 0, 1, 3, Qt.AlignCenter)

    # define what happens when refresh button is clicked
    def refresh_click(self):
        self.dropdown.clear()  # clears port list from dropdown menu
        for port in self.serial_ports():
            self.dropdown.addItem(port)
        self.textbox.setText("List refreshed")

    # define what happens when connect button is clicked
    def connect_click(self):
        if self.dropdown.currentIndex() == 0:
            self.textbox.setText("Please choose a port from the dropdown menu")

        # if connection is successful open main window and close current window
        if self.dropdown.currentIndex() != 0:
            try:
                controller_settings = {'Kps': [0.1, 0.1, 0.1, 0.1, 0.1],
                                       'Kis': [1e-04, 1e-04, 1e-04, 1e-04, 1e-04],
                                       'Kds': [1e-04, 1e-04, 0.0, 0.001, 0.001],
                                       'motor_calibs': [4000.0, 4000.0, 4000.0, 4000.0, 4000.0],
                                       'volume_factors': [642.42426, 369.836, 369.836, 369.836, 369.836],
                                       'max_steps': [74599.91, 33289.953, 33289.953, 33289.953, 33289.953],
                                       'max_speeds': [2.75, 2.5, 2.5, 2.5, 2.5],
                                       'active': [1.0, 1.0, 1.0, 1.0, 1.0],
                                       'pressure_coeff_as': [0.018, 0.018, 0.018, 0.018, 0.018],
                                       'pressure_coeff_bs': [0.04, 0.04, 0.04, 0.04, 0.04],
                                       'sensor_units': [0.0, 0.0, 255.0, 0.0, 0.0]}
                n_pumps = len(controller_settings['Kps'])
                pump_settings = {'baud': '250000',
                                 'waittime': '3000',
                                 'pressure': ['20', '10', '20', '20', '20'],
                                 'speed': ['2000', '2000', '120', '120', '240'],
                                 'volume': ['6000', '-9000', '30', '30', '30'],
                                 'times': ['60', '60', '60', '60', '60'],
                                 'port': 'Test'}

                self.ui = main_window.MainWindow(n_pumps, controller_settings, pump_settings)
                self.ui.show()
                self.connection_panel_window.close()

                self.MT_queue.put(["FromGUI_ConnectSerial", [self.dropdown.currentText(), 250000]])
                # pass arguments
                # self.ManateeBackend.connect(self.dropdown.currentText(), 250000)

            # if the connection fails for some reason, the program displays the following message
            except Exception as e:
                self.textbox.setText("Connection failed\nPlease try again or try another port")
                print(e)

        # Csabi: try with multiple ports connected - if it really refreshes the port list?
        # threading can be added later to prevent freezing of the program during port collection

    def serial_ports(self):
        """ Lists serial port names
            :raises EnvironmentError:
                On unsupported or unknown platforms
            :returns:
                A list of the serial ports available on the system"""
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')
    
        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        if len(result) == 0:
            result = ["None"]
        result.append('Test')
        return result  # result = ["None", 'Test']


def window(MT_queue):
    app = QApplication(sys.argv)
    win = MainWindow(MT_queue)
    win.show()  # shows window
    sys.exit(app.exec_())  # clean exit when we close the window
    

if __name__ == "__main__":
    MT_queue = mp.Queue()
    window(MT_queue)
