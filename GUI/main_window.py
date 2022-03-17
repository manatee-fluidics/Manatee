import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLabel, QGridLayout, QDesktopWidget, \
    QHBoxLayout, QGroupBox, QScrollArea
from PyQt5.QtCore import Qt

import settings_panel
import main_window_controls
import main_window_pumps


class MainWindow(QMainWindow):  # inherits all properties from QMainWindow class
    """Creates Main Window with all functions."""
    def __init__(self, n_pumps, controller_settings, pump_settings):  # will run when an instance of the MainWindow class is created
        super(MainWindow, self).__init__()  # parent constructor

        # QMainWindow has a central widget that is a container for widgets, it has its own layout
        # create cw, set layout and alignment
        self.setCentralWidget(QWidget(self))
        self.cw_layout = QGridLayout()
        self.cw_layout.setAlignment(Qt.AlignTop)
        self.centralWidget().setLayout(self.cw_layout)

        self.n_pumps = n_pumps

        # defining widgets
        self.buttonbar = ButtonBar(self.n_pumps, controller_settings)
        self.controls = main_window_controls.Controls(pump_settings)
        self.pump_area = main_window_pumps.PumpArea(self.n_pumps, pump_settings)
        self.graph = Graph()
        self.terminal = Terminal()

        # add widgets to main window
        # name, starting row, starting col, rowspan, colspan (till the end is -1), alignment
        self.cw_layout.addWidget(self.buttonbar, 0, 0, 2, 6, Qt.AlignAbsolute)
        self.cw_layout.addWidget(self.controls, 0, 6, 2, 14, Qt.AlignAbsolute)
        self.cw_layout.addWidget(self.pump_area, 2, 0, 15, -1)
        self.cw_layout.addWidget(self.graph, 17, 0, -1, 15, Qt.AlignAbsolute)
        self.cw_layout.addWidget(self.terminal, 17, 15, -1, 5, Qt.AlignAbsolute)

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
    """This class defines the layout and buttons which belong to the button bar"""
    def __init__(self, n_pumps, controller_settings):
        super(ButtonBar, self).__init__()

        # define and set QWidget layout
        layout = QGridLayout()
        self.setLayout(layout)

        # define and add QGroupBox to QWidget's layout
        self.button_box = QGroupBox("Connection properties")
        layout.addWidget(self.button_box)

        # define and set the layout of the QGroupBox
        self.buttons_layout = QGridLayout(self)
        self.button_box.setLayout(self.buttons_layout)

        self.button_disconnect = QPushButton()
        self.button_disconnect.setText("Disconnect")
        # self.button_disconnect.clicked.connect()

        self.button_settings = QPushButton()
        self.button_settings.setText("Settings")
        self.button_settings.clicked.connect(lambda: self.open_settings_panel(n_pumps, controller_settings))

        self.button_loadprot = QPushButton()
        self.button_loadprot.setText("Load Protocol")
        # self.button_loadprot.clicked.connect()

        self.button_runprot = QPushButton()
        self.button_runprot.setText("Run Protocol")
        # self.button_runprot.clicked.connect()

        self.button_uploadprot = QPushButton()
        self.button_uploadprot.setText("Upload Protocol")
        # self.button_uploadprot.clicked.connect()

        # add all above defined buttons to the class layout
        self.buttons_layout.addWidget(self.button_disconnect, 0, 0, 1, 1)
        self.buttons_layout.addWidget(self.button_settings, 0, 1, 1, 1)
        self.buttons_layout.addWidget(self.button_loadprot, 1, 0, 1, 1)
        self.buttons_layout.addWidget(self.button_runprot, 1, 1, 1, 1)
        self.buttons_layout.addWidget(self.button_uploadprot, 1, 2, 1, 1)

    def open_settings_panel(self, n_pumps, controller_settings):
        self.ui = settings_panel.SettingsPanel(n_pumps, controller_settings)
        self.ui.show()


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

        label = QLabel("GRAPH")
        self.graph_layout.addWidget(label)


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

    app = QApplication(sys.argv)
    win = MainWindow(n_pumps, controller_settings, pump_settings)
    win.show()  # shows window
    sys.exit(app.exec_())  # clean exit when we close the window


window()
