import sys
import time
import multiprocessing as mp
import glob
import serial

from PyQt5.QtGui import QIcon, QPixmap, QGuiApplication, QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QLabel, \
    QComboBox, QGridLayout, QDesktopWidget
from PyQt5.QtCore import Qt, QSize, QTimer

import main_window


class ConnectionWindow(QMainWindow):
    """Main Window class for managing serial port connections."""

    def __init__(self, controller_settings, gui_settings, GUI_queues):
        super().__init__()

        self.GUI_queues = GUI_queues
        self.controller_settings = controller_settings
        self.gui_settings = gui_settings

        self.initUI()

        # Poll the queue every 1000 ms
        self.timer = QTimer()
        self.timer.timeout.connect(self.process_queue)
        self.timer.start(100)
        
    def initUI(self):
        """Initialize the main window UI."""

        # Set window properties
        self.setWindowTitle("Manatee Fluidics")
        self.setWindowIcon(QIcon("manatee_icon_square.png"))
        self.center()

        # Set central widget and layout
        central_widget = QWidget(self)
        central_layout = QVBoxLayout(central_widget)
        central_layout.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(central_widget)

        # Add widgets to layout
        central_layout.addWidget(Logo())
        self.connection_panel = ConnectionPanel(self, self.controller_settings, self.gui_settings, self.GUI_queues)
        central_layout.addWidget(self.connection_panel)


    def center(self):
        """Center the window on the screen."""

        frame = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        frame.moveCenter(center_point)
        self.move(frame.topLeft())

    def process_queue(self):
        """Process To_GUI_queue and update widgets if new data is present."""
    
        ln = self.GUI_queues[0].qsize()
        for i in range(ln):
            msg = self.GUI_queues[0].get()
    
            # Check if the queue data is for the graph
            if msg[0] == "ToGUI_SerialConnected":
                self.controller_settings = msg[1]
                self.connection_panel.controller_settings = msg[1]
                self.connection_panel.start_mainwindow()
                
            else:
                self.GUI_queues[0].put(msg) #message is for someone else
                
class Logo(QLabel):
    """Class to display Manatee logo."""

    def __init__(self):
        super().__init__()

        self.setAlignment(Qt.AlignCenter)
        pixmap = QPixmap("manatee_logo_big.png")
        resized_pixmap = pixmap.scaledToHeight(400)
        self.setPixmap(resized_pixmap)


class ConnectionPanel(QWidget):
    """Class to manage the connection panel UI."""

    def __init__(self, connection_window, controller_settings, gui_settings, GUI_queues):
        super().__init__()

        self.GUI_queues = GUI_queues
        self.controller_settings = controller_settings
        self.gui_settings = gui_settings
        self.connection_window = connection_window

        # Create UI elements
        self.refresh_button = QPushButton(icon=QIcon("refresh_icon.png"))
        self.port_dropdown = QComboBox()
        self.connect_button = QPushButton(text="Connect")
        self.status_label = QLabel(text="Welcome")

        self.initUI()

    def initUI(self):
        """Initialize the connection panel UI."""

        # Configure refresh button
        self.refresh_button.setIconSize(QSize(30, 30))
        self.refresh_button.setToolTip("Refresh port list")
        self.refresh_button.clicked.connect(self.refresh_ports)

        # Configure port dropdown
        self.port_dropdown.setEditable(True)
        self.port_dropdown.lineEdit().setReadOnly(True)
        self.port_dropdown.lineEdit().setAlignment(Qt.AlignCenter)
        self.port_dropdown.setFixedSize(100, 36)  # width, height
        self.refresh_ports()

        # Configure connect button
        self.connect_button.setFixedSize(100, 38)
        self.connect_button.clicked.connect(self.connect)

        # Configure status label
        self.status_label.setAlignment(Qt.AlignCenter)

        # Set grid layout and add widgets
        layout = QGridLayout(self)
        layout.addWidget(self.refresh_button, 0, 0, Qt.AlignLeft)
        layout.addWidget(self.port_dropdown, 0, 1, Qt.AlignCenter)
        layout.addWidget(self.connect_button, 0, 2, Qt.AlignRight)
        layout.addWidget(self.status_label, 1, 0, 1, 3, Qt.AlignCenter)

    def refresh_ports(self):
        """Refresh the list of available ports."""

        self.port_dropdown.clear()
        self.port_dropdown.addItems(self.get_serial_ports())
        self.status_label.setText("List refreshed")

    def connect(self):
        """Connect to the selected port."""

        # if self.port_dropdown.currentIndex() == 0:
        #     self.status_label.setText("Please choose a port from the dropdown menu")
        #     return
        
        self.GUI_queues[1].put(["FromGUI_SerialConnect", [self.port_dropdown.currentText(), 250000]])
        self.status_label.setText("Connecting...")
        self.connect_button.setEnabled(False)

    def start_mainwindow(self):
        try:
            self.connection_window.close()
            self.main_window = main_window.MainWindow(self.controller_settings, self.gui_settings, self.GUI_queues)
            self.main_window.show()
        except Exception as e:
            self.status_label.setText("Connection failed\nPlease try again or try another port")
            print(e)


    @staticmethod
    def get_serial_ports():
        """Return a list of available serial ports."""

        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        available_ports = [port for port in ports if is_port_available(port)]
        available_ports = available_ports + ['Test']
        return available_ports


def is_port_available(port):
    """Check if a port is available."""

    try:
        s = serial.Serial(port)
        s.close()
        return True
    except (OSError, serial.SerialException):
        return False


if __name__ == "__main__":
    def window():
        controller_settings = { 'Kp': [0.1, 0.1, 0.1, 0.1, 0.1],
                                'Ki': [1e-04, 1e-04, 1e-04, 1e-04, 1e-04],
                                'Kd': [1e-04, 1e-04, 0.0, 0.001, 0.001],
                                'Motor cal (steps/mm)': [4000.0, 4000.0, 4000.0, 4000.0, 4000.0],
                                'Syringe cal (μl/mm)': [642.42426, 369.836, 369.836, 369.836, 369.836],
                                'Syringe volume (μl)': [74599.91, 33289.953, 33289.953, 33289.953, 33289.953],
                                'Max speed (mm/sec)': [2.75, 2.5, 2.5, 2.5, 2.5],
                                'Active': [1.0, 1.0, 1.0, 0, 0],
                                'Pressure cal A': [0.018, 0.018, 0.018, 0.018, 0.018],
                                'Pressure cal B': [0.04, 0.04, 0.04, 0.04, 0.04],
                                'Sensor unit': [0.0, 0.0, 255.0, 0.0, 0.0]}

        GUI_queues = [mp.Queue(), mp.Queue()] #To_Gui and From_GUI
        app = QApplication(sys.argv)
        win = ConnectionWindow(controller_settings, GUI_queues)
        win.show()
        sys.exit(app.exec_())
    window()