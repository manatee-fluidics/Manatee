from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QGridLayout, QLineEdit, QHBoxLayout, QCheckBox, QGroupBox
from PyQt5.QtCore import Qt


class Controls(QWidget):
    """Creates and defines the Controls box and adds widgets"""
    def __init__(self):
        super(Controls, self).__init__()

        # define and set QWidget layout
        layout = QGridLayout()
        self.setLayout(layout)

        # define and add QGroupBox to QWidget's layout
        self.controls_box = QGroupBox("Controls")
        layout.addWidget(self.controls_box)

        # define and set the layout of the QGroupBox
        controls_layout = QHBoxLayout(self)
        self.controls_box.setLayout(controls_layout)

        # defining widgets
        self.switches = Switches()
        self.slaves = Slaves()
        self.programming = Programming()

        # adding the widgets to the layout
        controls_layout.addWidget(self.switches)
        controls_layout.addWidget(self.slaves)
        controls_layout.addWidget(self.programming)


class Switches(QWidget):
    """Creates and defines the Switches box and its widgets"""
    def __init__(self):
        super(Switches, self).__init__()

        # define and set QWidget layout
        layout = QGridLayout()
        self.setLayout(layout)

        # define and add QGroupBox to QWidget's layout
        self.switches_box = QGroupBox("Switches")
        layout.addWidget(self.switches_box)

        # define and set the layout of the QGroupBox
        self.switches_layout = QHBoxLayout(self)
        self.switches_box.setLayout(self.switches_layout)

        self.box1 = QCheckBox("Solenoid 1")
        self.box1.setChecked(False)

        self.box2 = QCheckBox("Solenoid 2")
        self.box2.setChecked(False)

        self.box3 = QCheckBox("Solenoid 3")
        self.box3.setChecked(False)
        # self.box1.stateChanged.connect(lambda: self.btnstate(self.b1))
        # self.b2.toggled.connect(lambda: self.btnstate(self.b2))

        self.switches_layout.addWidget(self.box1)
        self.switches_layout.addWidget(self.box2)
        self.switches_layout.addWidget(self.box3)


class Slaves(QWidget):
    """Creates and defines the Slaves box and its widgets"""
    def __init__(self):
        super(Slaves, self).__init__()

        # define and set QWidget layout
        layout = QGridLayout()
        self.setLayout(layout)

        # define and add QGroupBox to QWidget's layout
        self.slaves_box = QGroupBox("Slaves")
        layout.addWidget(self.slaves_box)

        # define and set the layout of the QGroupBox
        self.slaves_layout = QHBoxLayout(self)
        self.slaves_box.setLayout(self.slaves_layout)

        self.button_switch = QPushButton()
        self.button_switch.setText("Switch slave")
        # self.button_switch.clicked.connect()

        self.button_ttl = QPushButton()
        self.button_ttl.setText("TTL slave")
        # self.button_ttl.clicked.connect()

        self.button_multipinch = QPushButton()
        self.button_multipinch.setText("Multipinch slave")
        # self.button_multipinch.clicked.connect()

        self.slaves_layout.addWidget(self.button_switch)
        self.slaves_layout.addWidget(self.button_ttl)
        self.slaves_layout.addWidget(self.button_multipinch)


class Programming(QWidget):
    """Creates and defines the Programming box and its widgets"""
    def __init__(self):
        super(Programming, self).__init__()

        # define and set QWidget layout
        layout = QGridLayout()
        self.setLayout(layout)

        # define and add QGroupBox to QWidget's layout
        self.programming_box = QGroupBox("Programming")
        layout.addWidget(self.programming_box)

        # define and set the layout of the QGroupBox
        self.programming_layout = QHBoxLayout(self)
        self.programming_box.setLayout(self.programming_layout)

        self.label = QLabel(self)
        self.label.setText("Wait time (s):")
        self.label.setAlignment(Qt.AlignLeft)

        self.validator = QDoubleValidator(self)
        self.validator.setNotation(QDoubleValidator.ScientificNotation)
        self.textbox = QLineEdit()
        self.textbox.setValidator(self.validator)
        self.textbox.setText("")

        self.button = QPushButton()
        self.button.setText("Send")
        # self.button.clicked.connect()

        self.programming_layout.addWidget(self.label)
        self.programming_layout.addWidget(self.textbox)
        self.programming_layout.addWidget(self.button)
