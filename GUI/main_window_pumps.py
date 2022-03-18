from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QGridLayout, QLineEdit, QGroupBox, QSlider, QRadioButton, \
    QScrollArea
from PyQt5.QtCore import Qt


class PumpArea(QScrollArea):
    def __init__(self, pump_number, pump_settings):
        super(PumpArea, self).__init__()

        self.setWidgetResizable(True)
        self.horizontalScrollBar().setEnabled(True)
        self.verticalScrollBar().setEnabled(False)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # making qwidget object
        pump = QWidget()
        self.setWidget(pump)
        pump_layout = QGridLayout()
        pump.setLayout(pump_layout)

        self.n_pumps = pump_number

        # add as many Pump widgets as it is defined upon calling the program
        starting_columns = [0, 4, 8, 12, 16]
        for i in range(1, self.n_pumps + 1):
            pump = Pump(i, self.process_pump_settings(pump_settings, i-1))
            pump_layout.addWidget(pump, 0, starting_columns[i - 1], -1, 4)
            i += 1

    def process_pump_settings(self, dict, pump_number):
        """This function processes the contents of the pump_settings dictionary. It makes a list for each pump with
        the corresponding values for all 4 pump values, which later will be handed to the pump initializer for loop
        (above) and be dealt with in the Pump class to distribute the values into the corresponding textboxes."""
        pump_values = []
        keys = ["pressure", "speed", "volume"]
        for key, value in dict.items():
            if key in keys:
                pump_values.append(value[pump_number])

        return pump_values


class Pump(QGroupBox):
    def __init__(self, pump_number, pump_values):  # pump_values is a list
        super(Pump, self).__init__()

        # define and set the layout of the QGroupBox
        self.setTitle("Pump " + str(pump_number))
        self.pump_layout = QGridLayout(self)
        self.setLayout(self.pump_layout)

        self.validator = QDoubleValidator(self)
        self.validator.setNotation(QDoubleValidator.ScientificNotation)

        # pressure settings
        self.pressure_label = QLabel(self)
        self.pressure_label.setText("Pressure (kPa)")
        self.pressure_label.setAlignment(Qt.AlignLeft)

        self.pressure_box = QLineEdit()
        self.pressure_box.setValidator(self.validator)
        self.pressure_box.setText(pump_values[0])

        self.pressure_set = QPushButton()
        self.pressure_set.setText("Pressure set")
        # self.button.clicked.connect()

        self.pressure_regulate = QPushButton()
        self.pressure_regulate.setText("Pressure regulate")
        # self.button.clicked.connect()

        # speed and volume settings
        self.speed_label = QLabel(self)
        self.speed_label.setText("Speed (μl/sec)")
        self.speed_label.setAlignment(Qt.AlignLeft)

        self.speed_box = QLineEdit()
        self.speed_box.setValidator(self.validator)
        self.speed_box.setText(pump_values[1])

        self.volume_label = QLabel(self)
        self.volume_label.setText("Volume (μl)")
        self.volume_label.setAlignment(Qt.AlignLeft)

        self.volume_box = QLineEdit()
        self.volume_box.setValidator(self.validator)
        self.volume_box.setText(pump_values[2])

        self.sv_set = QPushButton()
        self.sv_set.setText("Set")
        # self.button.clicked.connect()

        # radio button - move abs & relative
        self.move_absolute = QRadioButton("Move absolute")
        # self.move_absolute.toggled.connect()

        self.move_relative = QRadioButton("Move relative")
        # self.move_relative.toggled.connect()

        self.move_box = QGroupBox("Move pump")
        self.move_layout = QGridLayout(self)
        self.move_box.setLayout(self.move_layout)

        self.move_up_button = QPushButton()
        self.move_up_button.setText("+")
        # self.button.clicked.connect()

        self.move_down_button = QPushButton()
        self.move_down_button.setText("-")
        # self.button.clicked.connect()

        self.move_layout.addWidget(self.move_up_button, 0, 0, 1, 1)
        self.move_layout.addWidget(self.move_down_button, 1, 0, 1, 1)

        self.speed_display = QLabel(self)
        self.speed_display.setText("Speed (μl/sec): 0.0")
        self.speed_display.setAlignment(Qt.AlignLeft)

        self.position_display = QLabel(self)
        self.position_display.setText("Pump position: 0.0")
        self.position_display.setAlignment(Qt.AlignLeft)

        self.slider = QSlider(Qt.Vertical)
        self.slider.setValue(100)

        # name, starting row, starting col, rowspan, colspan (till the end is -1), alignment
        self.pump_layout.addWidget(self.pressure_label, 0, 0, 1, 1)
        self.pump_layout.addWidget(self.pressure_box, 0, 1, 1, 1)
        self.pump_layout.addWidget(self.pressure_set, 1, 0, 1, 1)
        self.pump_layout.addWidget(self.pressure_regulate, 1, 1, 1, 1)

        self.pump_layout.addWidget(self.speed_label, 2, 0, 1, 1)
        self.pump_layout.addWidget(self.speed_box, 2, 1, 1, 1)
        self.pump_layout.addWidget(self.volume_label, 3, 0, 1, 1)
        self.pump_layout.addWidget(self.volume_box, 3, 1, 1, 1)
        self.pump_layout.addWidget(self.sv_set, 4, 0, 1, 1)
        self.pump_layout.addWidget(self.move_absolute, 5, 0, 1, 1)
        self.pump_layout.addWidget(self.move_relative, 5, 1, 1, 1)

        self.pump_layout.addWidget(self.move_box, 6, 0, 3, 1)

        self.pump_layout.addWidget(self.speed_display, 9, 0, 1, 1)
        self.pump_layout.addWidget(self.position_display, 10, 0, 1, 1)
        self.pump_layout.addWidget(self.slider, 6, 1, -1, 1, Qt.AlignAbsolute)
