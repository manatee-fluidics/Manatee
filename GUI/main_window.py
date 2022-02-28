import sys
from PyQt5.QtGui import QIcon, QDoubleValidator
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLabel, QGridLayout, QDesktopWidget, \
    QLineEdit, QHBoxLayout, QGroupBox
from PyQt5.QtCore import Qt
from PyQt5 import QtGui, QtCore

# import settings_panel
import main_window_controls


class MainWindow(QMainWindow):  # inherits all properties from QMainWindow class
    """Creates Main Window with all functions."""
    def __init__(self, n_pumps):  # this will run whenever we create an instance of the MainWindow class
        super(MainWindow, self).__init__()  # parent constructor

        # QMainWindow has a central widget that is a container for widgets, it has its own layout
        # create cw, set layout and alignment
        self.setCentralWidget(QWidget(self))
        self.cw_layout = QGridLayout()
        self.cw_layout.setAlignment(Qt.AlignCenter)
        self.centralWidget().setLayout(self.cw_layout)

        self.buttonbar = ButtonBar()
        self.controls = main_window_controls.Controls()
        self.graph = Graph()
        self.terminal = Terminal()

        # name, starting row, starting col, rowspan, colspan (till the end is -1), alignment
        self.cw_layout.addWidget(self.buttonbar, 0, 0, 1, 20, Qt.AlignLeft)
        self.cw_layout.addWidget(self.controls, 1, 0, 1, 20, Qt.AlignLeft)
        self.cw_layout.addWidget(self.graph, 10, 0, 8, 14, Qt.AlignLeft)
        self.cw_layout.addWidget(self.terminal, 10, 3, 8, 6, Qt.AlignLeft)

        self.n_pumps = n_pumps
        starting_columns = [0, 4, 8, 12, 16]
        for i in range(1, self.n_pumps + 1):
            pump = Pump(i)
            self.cw_layout.addWidget(pump, 2, starting_columns[i-1], 8, 4, Qt.AlignCenter)
            i += 1

        self.initUI()

    def initUI(self):
        """Initializes the Main window with all the attributes specified below."""

        self.setWindowTitle("Manatee Fluidics")
        self.setWindowIcon(QIcon("manatee_icon_square.png"))

        # open window in full size
        self.showMaximized()

        # self.setGeometry(1300, 200, 1000, 1500)
        # xpos, ypos, width, height (in pixels)
        # if xpos and ypos are 0, win shows up on the top-left corner;
        # 100, 100 moves the top-left corner of the window to the right and down

        # open not maximized, center of screen
        # self.center()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


class ButtonBar(QWidget):
    def __init__(self):
        super(ButtonBar, self).__init__()

        self.buttons_layout = QHBoxLayout(self)

        self.button_disconnect = QPushButton()
        self.button_disconnect.setText("Disconnect")
        # self.button_disconnect.clicked.connect()

        self.button_settings = QPushButton()
        self.button_settings.setText("Settings")
        # self.button_settings.clicked.connect(settings_panel.window) - error!!!

        self.button_loadprot = QPushButton()
        self.button_loadprot.setText("Load Protocol")
        # self.button_loadprot.clicked.connect()

        self.button_runprot = QPushButton()
        self.button_runprot.setText("Run Protocol")
        # self.button_runprot.clicked.connect()

        self.button_uploadprot = QPushButton()
        self.button_uploadprot.setText("Upload Protocol")
        # self.button_uploadprot.clicked.connect()

        self.buttons_layout.addWidget(self.button_disconnect)
        self.buttons_layout.addWidget(self.button_settings)
        self.buttons_layout.addWidget(self.button_loadprot)
        self.buttons_layout.addWidget(self.button_runprot)
        self.buttons_layout.addWidget(self.button_uploadprot)


class Pump(QWidget):
    def __init__(self, pump_number):
        super(Pump, self).__init__()

        # define and set QWidget layout
        layout = QGridLayout()
        self.setLayout(layout)

        # define and add QGroupBox to QWidget's layout
        self.pump_box = QGroupBox("Pump " + str(pump_number))  # Pump and number !!!!!!!!!!
        layout.addWidget(self.pump_box)

        # define and set the layout of the QGroupBox
        self.pump_layout = QGridLayout(self)
        self.pump_box.setLayout(self.pump_layout)

        self.validator = QDoubleValidator(self)
        self.validator.setNotation(QDoubleValidator.ScientificNotation)

        self.pressure_label = QLabel(self)
        self.pressure_label.setText("Pressure (kPa)")
        self.pressure_label.setAlignment(Qt.AlignLeft)

        self.pressure_box = QLineEdit()
        self.pressure_box.setValidator(self.validator)
        self.pressure_box.setText("")

        self.pressure_button = QPushButton()
        self.pressure_button.setText("Set")
        # self.button.clicked.connect()

        self.speed_label = QLabel(self)
        self.speed_label.setText("Speed (μl/sec)")
        self.speed_label.setAlignment(Qt.AlignLeft)

        self.speed_box = QLineEdit()
        self.speed_box.setValidator(self.validator)
        self.speed_box.setText("")

        self.speed_button = QPushButton()
        self.speed_button.setText("Set")
        # self.button.clicked.connect()

        self.volume_label = QLabel(self)
        self.volume_label.setText("Volume (μl)")
        self.volume_label.setAlignment(Qt.AlignLeft)

        self.volume_box = QLineEdit()
        self.volume_box.setValidator(self.validator)
        self.volume_box.setText("")

        self.hmin_button = QPushButton()
        self.hmin_button.setText("Home min")
        # self.button.clicked.connect()

        self.hmax_button = QPushButton()
        self.hmax_button.setText("Home max")
        # self.button.clicked.connect()

        self.mr_button = QPushButton()
        self.mr_button.setText("Move relative")
        # self.button.clicked.connect()

        self.ma_button = QPushButton()
        self.ma_button.setText("Move absolute")
        # self.button.clicked.connect()

        self.regulate_button = QPushButton()
        self.regulate_button.setText("Regulate")
        # self.button.clicked.connect()

        self.speed_display = QLabel(self)
        self.speed_display.setText("Speed\n(μl/sec)")
        self.speed_display.setAlignment(Qt.AlignCenter)

        # name, starting row, starting col, rowspan, colspan (till the end is -1), alignment
        self.pump_layout.addWidget(self.pressure_label, 0, 0, 1, 1, Qt.AlignLeft)
        self.pump_layout.addWidget(self.pressure_box, 0, 1, 1, 1, Qt.AlignLeft)
        self.pump_layout.addWidget(self.pressure_button, 0, 2, 1, 1, Qt.AlignLeft)

        self.pump_layout.addWidget(self.speed_label, 1, 0, 1, 1, Qt.AlignLeft)
        self.pump_layout.addWidget(self.speed_box, 1, 1, 1, 1, Qt.AlignLeft)
        self.pump_layout.addWidget(self.speed_button, 1, 2, 1, 1, Qt.AlignLeft)

        self.pump_layout.addWidget(self.volume_label, 2, 0, 1, 1, Qt.AlignLeft)
        self.pump_layout.addWidget(self.volume_box, 2, 1, 1, 1, Qt.AlignLeft)

        self.pump_layout.addWidget(self.hmin_button, 3, 0, 1, 1, Qt.AlignLeft)
        self.pump_layout.addWidget(self.hmax_button, 4, 0, 1, 1, Qt.AlignLeft)
        self.pump_layout.addWidget(self.mr_button, 5, 0, 1, 1, Qt.AlignLeft)
        self.pump_layout.addWidget(self.ma_button, 6, 0, 1, 1, Qt.AlignLeft)
        self.pump_layout.addWidget(self.regulate_button, 7, 0, 1, 1, Qt.AlignLeft)

        self.pump_layout.addWidget(self.speed_display, 3, 1, 5, 1, Qt.AlignCenter)


class Graph(QWidget):
    def __init__(self):
        super(Graph, self).__init__()

        # define and set QWidget layout
        layout = QGridLayout()
        self.setLayout(layout)

        # define and add QGroupBox to QWidget's layout
        self.graph_box = QGroupBox("Graph")
        layout.addWidget(self.graph_box)

        # define and set the layout of the QGroupBox
        self.graph_layout = QHBoxLayout(self)
        self.graph_box.setLayout(self.graph_layout)


class Terminal(QWidget):
    def __init__(self):
        super(Terminal, self).__init__()

        # define and set QWidget layout
        layout = QGridLayout()
        self.setLayout(layout)

        # define and add QGroupBox to QWidget's layout
        self.terminal_box = QGroupBox("Terminal")
        layout.addWidget(self.terminal_box)

        # define and set the layout of the QGroupBox
        self.terminal_layout = QHBoxLayout(self)
        self.terminal_box.setLayout(self.terminal_layout)


def window():
    n_pumps = 5
    app = QApplication(sys.argv)
    win = MainWindow(n_pumps)
    win.show()  # shows window
    sys.exit(app.exec_())  # clean exit when we close the window


window()
