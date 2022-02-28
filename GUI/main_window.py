import sys
from PyQt5.QtGui import QIcon, QDoubleValidator
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QLabel, QGridLayout, \
    QDesktopWidget, QLineEdit, QHBoxLayout, QCheckBox, QGroupBox
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
        self.cw_layout.addWidget(self.buttonbar, 0, 0, 1, -1, Qt.AlignLeft)
        self.cw_layout.addWidget(self.controls, 1, 0, 1, -1, Qt.AlignLeft)
        self.cw_layout.addWidget(self.graph, 10, 0, 8, 3, Qt.AlignLeft)
        self.cw_layout.addWidget(self.terminal, 10, 3, 8, 2, Qt.AlignLeft)

        self.n_pumps = n_pumps
        for i in range(1, self.n_pumps + 1):
            pump = Pump(i)
            self.cw_layout.addWidget(pump, 2, i - 1, 8, -1, Qt.AlignLeft)
            i += 1

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
        self.pump_layout = QHBoxLayout(self)
        self.pump_box.setLayout(self.pump_layout)


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
    n_pumps = 2
    app = QApplication(sys.argv)
    win = MainWindow(n_pumps)
    win.show()  # shows window
    sys.exit(app.exec_())  # clean exit when we close the window


window()
