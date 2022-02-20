import multiprocessing as mp
import sys
import serial
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QLabel, \
    QComboBox, QGridLayout, QDesktopWidget
from PyQt5.QtCore import Qt
from PyQt5 import QtGui, QtCore

import Manatee_main


class MainWindow(QMainWindow):  # inherits all properties from QMainWindow class
    """Creates Main Window with all functions."""
    def __init__(self, queue_send):  # this will run whenever we create an instance of the MainWindow class
        super(MainWindow, self).__init__()  # parent constructor

        self.queue_send = queue_send
        # QMainWindow has a central widget that is a container for widgets, it has its own layout
        # create cw, set layout and alignment
        self.setCentralWidget(QWidget(self))
        cw_layout = QVBoxLayout()
        cw_layout.setAlignment(Qt.AlignCenter)
        self.centralWidget().setLayout(cw_layout)

        # call layout elements
        self.logo = Logo()
        self.connections = Connections(self, queue_send)

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
        self.center()

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
    def __init__(self, main_window2, queue_send):
        super(Connections, self).__init__()

        self.queue_send = queue_send
        self.main_window = main_window2
        self.conn_layout = QGridLayout(self)

        self.button_refresh = QPushButton()
        self.button_refresh.setIcon(QtGui.QIcon("refresh_icon.png"))
        self.button_refresh.setIconSize(QtCore.QSize(30, 30))
        self.button_refresh.setToolTip("Refresh port list")
        self.button_refresh.clicked.connect(lambda: self.refresh_click())  # or self.refresh_click

        self.textbox = QLabel(self)
        self.textbox.setText("Welcome")

        self.dropdown = QComboBox(self)
        self.dropdown.setEditable(True)
        self.dropdown.lineEdit().setReadOnly(True)
        self.dropdown.lineEdit().setAlignment(Qt.AlignCenter)
        self.dropdown.setFixedSize(100, 36)  # width, height
        connection_list = self.serial_ports()
        for port in connection_list:
            self.dropdown.addItem(port)

        self.button_connect = QPushButton()
        self.button_connect.setText("Connect")
        self.button_connect.setFixedSize(100, 38)
        self.button_connect.clicked.connect(lambda: self.connect_click())

        # name, starting row, starting col, rowspan, colspan (till the end is -1), alignment
        self.conn_layout.addWidget(self.button_refresh, 0, 0, 1, 1, Qt.AlignLeft)
        self.conn_layout.addWidget(self.dropdown, 0, 1, 1, 1, Qt.AlignCenter)
        self.conn_layout.addWidget(self.button_connect, 0, 2, 1, 1, Qt.AlignRight)
        self.conn_layout.addWidget(self.textbox, 1, 0, 1, 3, Qt.AlignCenter)

    # Csabi: try with multiple ports connected - if it really refreshes the port list!!!
    # threading can be added later to prevent freezing of the program during port collection
    def refresh_click(self):
        self.dropdown.clear()  # clears port list from dropdown menu
        connection_list = self.serial_ports()
        for port in connection_list:
            self.dropdown.addItem(port)
            print(port)  # just to check when list refreshes, otherwise can be commented out
        self.textbox.setText("List refreshed")

    def connect_click(self):
        self.textbox.setText("Connecting to port...")
        #pass arguments
        #self.ManateeBackend.connect(self.dropdown.currentText(), 250000)
        
        #Gica close window upon successful connect
    # widgets are defined inside function - should be defined inside class but outside function?

    def serial_ports(self):
        """ Lists serial port names
    
            :raises EnvironmentError:
                On unsupported or unknown platforms
            :returns:
                A list of the serial ports available on the system
        """
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
        return result


def window(queue_send):
    app = QApplication(sys.argv)
    win = MainWindow(queue_send)
    win.show()  # shows window
    sys.exit(app.exec_())  # clean exit when we close the window

if __name__ == "__main__":
    queue_send = mp.Queue()
    window(queue_send)
