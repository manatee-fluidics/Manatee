import sys
from PyQt5.QtGui import QIcon, QDoubleValidator
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QLabel, QGridLayout, \
    QDesktopWidget, QLineEdit, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5 import QtGui, QtCore


class MainWindow(QMainWindow):  # inherits all properties from QMainWindow class
    """Creates Main Window with all functions."""
    def __init__(self, controller_settings):  # this will run whenever we create an instance of the MainWindow class
        super(MainWindow, self).__init__()  # parent constructor

        # QMainWindow has a central widget that is a container for widgets, it has its own layout
        # create cw, set layout and alignment
        self.setCentralWidget(QWidget(self))
        self.cw_layout = QGridLayout()
        self.cw_layout.setAlignment(Qt.AlignLeft)
        self.centralWidget().setLayout(self.cw_layout)

        self.settings = controller_settings

        self.text = Text()
        self.buttons = Buttons()

        self.n_pumps = 5
        pumps = []
        for i in range(1, self.n_pumps + 1):
            pumps.append("pump"+str(i))

        i = 1
        for pump in pumps:
            # pump = Pump(i, self.settings)
            pump = Pump(i, self.process_settings(self.settings, i - 1))
            self.cw_layout.addWidget(pump, 0, i, 11, 1, Qt.AlignLeft)
            i += 1

        # name, starting row, starting col, rowspan, colspan (till the end is -1), alignment
        self.cw_layout.addWidget(self.text, 0, 0, 11, 1, Qt.AlignRight)
        self.cw_layout.addWidget(self.buttons, 12, 0, 1, -1, Qt.AlignCenter)

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

    def process_settings(self, dict, column_number):
        """This function processes the contents of the machine settings dictionary. It makes a list for each pump with
        the corresponding values for all 11 textboxes, which later will be handed to the pump initializer script and
        be dealt with in the Pump class to distribute the values into the corresponding textboxes."""
        settings_values = []
        for key, value in dict.items():
            settings_values.append(value[column_number])

        return settings_values


class Text(QWidget):
    def __init__(self):
        super(Text, self).__init__()

        self.text_layout = QVBoxLayout(self)

        self.empty = QLabel(self)
        self.empty.setText("")
        self.empty.setAlignment(Qt.AlignRight)

        self.kp = QLabel(self)
        self.kp.setText("Kp")
        self.kp.setAlignment(Qt.AlignRight)

        self.ki = QLabel(self)
        self.ki.setText("Ki")
        self.ki.setAlignment(Qt.AlignRight)

        self.kd = QLabel(self)
        self.kd.setText("Kd")
        self.kd.setAlignment(Qt.AlignRight)

        self.motor = QLabel(self)
        self.motor.setText("Motor cal (steps/mm)")
        self.motor.setAlignment(Qt.AlignRight)

        self.sc = QLabel(self)
        self.sc.setText("Syringe cal (μl/mm)")
        self.sc.setAlignment(Qt.AlignRight)

        self.sv = QLabel(self)
        self.sv.setText("Syringe volume (μl)")
        self.sv.setAlignment(Qt.AlignRight)

        self.ms = QLabel(self)
        self.ms.setText("Max speed (mm/sec)")
        self.ms.setAlignment(Qt.AlignRight)

        self.chl = QLabel(self)
        self.chl.setText("Active")
        self.chl.setAlignment(Qt.AlignRight)

        self.prca = QLabel(self)
        self.prca.setText("Pressure cal A")
        self.prca.setAlignment(Qt.AlignRight)

        self.prcb = QLabel(self)
        self.prcb.setText("Pressure cal B")
        self.prcb.setAlignment(Qt.AlignRight)

            #later use
        # self.su = QLabel(self)
        # self.su.setText("Sensor unit")
        # self.su.setAlignment(Qt.AlignRight)

        self.text_layout.addWidget(self.empty)
        self.text_layout.addWidget(self.kp)
        self.text_layout.addWidget(self.ki)
        self.text_layout.addWidget(self.kd)
        self.text_layout.addWidget(self.motor)
        self.text_layout.addWidget(self.sc)
        self.text_layout.addWidget(self.sv)
        self.text_layout.addWidget(self.ms)
        self.text_layout.addWidget(self.chl)
        self.text_layout.addWidget(self.prca)
        self.text_layout.addWidget(self.prcb)
        #self.text_layout.addWidget(self.su)


class Pump(QWidget):
    def __init__(self, pump_number, settings_list):
        super(Pump, self).__init__()

        # specify widget layout, settings dict and validators (only accept numbers)
        self.pump_layout = QVBoxLayout(self)
        self.settings = settings_list  # deal with list element distribution to setText
        self.validator = QDoubleValidator(self)
        self.validator.setNotation(QDoubleValidator.ScientificNotation)

        self.pump = QLabel(self)
        self.pump.setText("Pump " + str(pump_number))
        self.pump.setAlignment(Qt.AlignLeft)

        self.kp_value = QLineEdit()
        self.kp_value.setToolTip("Kp")
        self.kp_value.setValidator(self.validator)
        self.kp_value.setText(str(self.settings[0]))

        self.ki_value = QLineEdit()
        self.ki_value.setToolTip("Ki")
        self.ki_value.setValidator(self.validator)
        self.ki_value.setText(str(self.settings[1]))

        self.kd_value = QLineEdit()
        self.kd_value.setToolTip("Kd")
        self.kd_value.setValidator(self.validator)
        self.kd_value.setText(str(self.settings[2]))

        self.motor_value = QLineEdit()
        self.motor_value.setToolTip("Motor cal (steps/mm)")
        self.motor_value.setValidator(self.validator)
        self.motor_value.setText(str(self.settings[3]))

        self.sc_value = QLineEdit()
        self.sc_value.setToolTip("Syringe cal (μl/mm)")
        self.sc_value.setValidator(self.validator)
        self.sc_value.setText(str(self.settings[4]))

        self.sv_value = QLineEdit()
        self.sv_value.setToolTip("Syringe volume (μl)")
        self.sv_value.setValidator(self.validator)
        self.sv_value.setText(str(self.settings[5]))

        self.ms_value = QLineEdit()
        self.ms_value.setToolTip("Max speed (mm/sec)")
        self.ms_value.setValidator(self.validator)
        self.ms_value.setText(str(self.settings[6]))

        self.chl_value = QLineEdit()
        self.chl_value.setToolTip("Active")
        self.chl_value.setValidator(self.validator)
        self.chl_value.setText(str(self.settings[7]))

        self.prca_value = QLineEdit()
        self.prca_value.setToolTip("Pressure cal A")
        self.prca_value.setValidator(self.validator)
        self.prca_value.setText(str(self.settings[8]))

        self.prcb_value = QLineEdit()
        self.prcb_value.setToolTip("Pressure cal B")
        self.prcb_value.setValidator(self.validator)
        self.prcb_value.setText(str(self.settings[9]))

        # later use
        # self.su_value = QLineEdit()
        # self.su_value.setToolTip("Sensor unit")
        # self.su_value.setValidator(self.validator)
        # self.su_value.setText(str(self.settings[10]))

        self.pump_layout.addWidget(self.pump)
        self.pump_layout.addWidget(self.kp_value)
        self.pump_layout.addWidget(self.ki_value)
        self.pump_layout.addWidget(self.kd_value)
        self.pump_layout.addWidget(self.motor_value)
        self.pump_layout.addWidget(self.sc_value)
        self.pump_layout.addWidget(self.sv_value)
        self.pump_layout.addWidget(self.ms_value)
        self.pump_layout.addWidget(self.chl_value)
        self.pump_layout.addWidget(self.prca_value)
        self.pump_layout.addWidget(self.prcb_value)
        # self.pump_layout.addWidget(self.su_value)


class Buttons(QWidget):
    def __init__(self):
        super(Buttons, self).__init__()

        self.buttons_layout = QHBoxLayout(self)

        self.button_save = QPushButton()
        self.button_save.setText("Upload settings")
        self.button_save.setFixedSize(100, 38)  # width, height
        # self.button_save.clicked.connect()

        self.buttons_layout.addWidget(self.button_save)


# if __name__ == "__main__":
def window():
    controller_settings = {  'Kps': [0.1, 0.1, 0.1, 0.1, 0.1],
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

    app = QApplication(sys.argv)
    win = MainWindow(controller_settings)
    win.show()  # shows window
    sys.exit(app.exec_())  # clean exit when we close the window


window()
