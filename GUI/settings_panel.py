import sys
from PyQt5.QtGui import QIcon, QDoubleValidator
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QLabel, QGridLayout, \
    QDesktopWidget, QLineEdit, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5 import QtGui, QtCore


class SettingsPanel(QMainWindow):  # inherits all properties from QMainWindow class
    """Creates Setting Panel with all functions, textboxes, etc."""
    def __init__(self, n_pumps, controller_settings):  # will run when an instance of the class is created
        super(SettingsPanel, self).__init__()  # parent constructor

        # QMainWindow has a central widget that is a container for widgets, it has its own layout
        # create cw, set layout and alignment
        self.setCentralWidget(QWidget(self))
        self.cw_layout = QGridLayout()
        self.cw_layout.setAlignment(Qt.AlignLeft)
        self.centralWidget().setLayout(self.cw_layout)

        # dict where all the data is
        self.settings = controller_settings

        self.text = Text()

        self.n_pumps = n_pumps
        self.pump_list = []
        for i in range(1, self.n_pumps + 1):
            pump = Pump(i, self.process_settings(self.settings, i - 1))
            self.cw_layout.addWidget(pump, 0, i, 11, 1, Qt.AlignLeft)
            self.pump_list.append(pump)
            i += 1

        self.buttons = Buttons(self, self.settings, self.pump_list)

        # name, starting row, starting col, rowspan, colspan (till the end is -1), alignment
        self.cw_layout.addWidget(self.text, 0, 0, 11, 1, Qt.AlignRight)
        self.cw_layout.addWidget(self.buttons, 12, 0, 1, -1, Qt.AlignCenter)

        self.initUI()

    def initUI(self):
        """Initializes the Main window with all the attributes specified below."""

        self.setWindowTitle("Settings")
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

        self.active = QLabel(self)
        self.active.setText("Active")
        self.active.setAlignment(Qt.AlignRight)

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
        self.text_layout.addWidget(self.active)
        self.text_layout.addWidget(self.prca)
        self.text_layout.addWidget(self.prcb)
        #self.text_layout.addWidget(self.su)


class Pump(QWidget):
    def __init__(self, pump_number, settings_list):
        super(Pump, self).__init__()

        # initialize list to later store edited values in
        # first value is the pump number so all pumps will have a list

        # or one list before initializing the pumps
        # that list will collect all data ad use that list in Button class
        self.edited_values = []
        self.pump_number = pump_number

        # specify widget layout, settings dict and validators (only accept numbers)
        self.pump_layout = QVBoxLayout(self)
        self.settings = settings_list  # deal with list element distribution to setText
        self.validator = QDoubleValidator(self)
        self.validator.setNotation(QDoubleValidator.ScientificNotation)

        self.pump = QLabel(self)
        self.pump.setText("Pump " + str(self.pump_number))
        self.pump.setAlignment(Qt.AlignLeft)

        self.kp_value = QLineEdit()
        self.kp_value.setToolTip("Kp")
        self.kp_value.setValidator(self.validator)
        self.kp_value.setText(str(self.settings[0]))
        # self.kp_value.textChanged[str].connect(lambda: self.record_text_change(self.edited_values, str(45),
        #                                                                        "Kp", self.pump_number))

        self.ki_value = QLineEdit()
        self.ki_value.setToolTip("Ki")
        self.ki_value.setValidator(self.validator)
        self.ki_value.setText(str(self.settings[1]))

        self.kd_value = QLineEdit()
        self.kd_value.setToolTip("Kd")
        self.kd_value.setValidator(self.validator)
        self.kd_value.setText(str(self.settings[2]))

        self.motor_cal_value = QLineEdit()
        self.motor_cal_value.setToolTip("Motor cal (steps/mm)")
        self.motor_cal_value.setValidator(self.validator)
        self.motor_cal_value.setText(str(self.settings[3]))

        self.syringe_cal_value = QLineEdit()
        self.syringe_cal_value.setToolTip("Syringe cal (μl/mm)")
        self.syringe_cal_value.setValidator(self.validator)
        self.syringe_cal_value.setText(str(self.settings[4]))

        self.syringe_volume_value = QLineEdit()
        self.syringe_volume_value.setToolTip("Syringe volume (μl)")
        self.syringe_volume_value.setValidator(self.validator)
        self.syringe_volume_value.setText(str(self.settings[5]))

        self.max_speed_value = QLineEdit()
        self.max_speed_value.setToolTip("Max speed (mm/sec)")
        self.max_speed_value.setValidator(self.validator)
        self.max_speed_value.setText(str(self.settings[6]))

        self.active_value = QLineEdit()
        self.active_value.setToolTip("Active")
        self.active_value.setValidator(self.validator)
        self.active_value.setText(str(self.settings[7]))

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
        self.pump_layout.addWidget(self.motor_cal_value)
        self.pump_layout.addWidget(self.syringe_cal_value)
        self.pump_layout.addWidget(self.syringe_volume_value)
        self.pump_layout.addWidget(self.max_speed_value)
        self.pump_layout.addWidget(self.active_value)
        self.pump_layout.addWidget(self.prca_value)
        self.pump_layout.addWidget(self.prcb_value)
        # self.pump_layout.addWidget(self.su_value)


    # def record_text_change(self, edited_values, new_text, row, pump_number):
    #     """Gets the new value in the textbox and row the textbox belongs to,
    #     puts all this data into a list and appends that list to the edited_values list earlier defined in the class"""
    #     change = [new_text, row, pump_number]
    #     edited_values.append(change)
    #     print(edited_values)


class Buttons(QWidget):
    def __init__(self, settings_window, controller_settings, pump_list):
        super(Buttons, self).__init__()

        self.buttons_layout = QHBoxLayout(self)

        self.button_save = QPushButton()
        self.button_save.setText("Save settings")
        self.button_save.setFixedSize(100, 38)  # width, height
        self.button_save.clicked.connect(lambda: self.save_settings())

        self.buttons_layout.addWidget(self.button_save)

        self.settings_panel_window = settings_window
        self.settings = controller_settings
        self.pump_list = pump_list

    def save_settings(self):
        # get all values from all pumps and all textboxes and put them in a new dict
        # from now on, that will be the dict in use

        # list = ["kp", "ki", "kd", "motor_cal", "syringe_cal", "syringe_volume", "max_speed", "active", "prca", "prcb"]

        # initialize new dict
        dict = {}
        for key, value in self.settings.items():
            dict[key] = []

        for i in range(len(self.pump_list)):
            dict["kp"].append(self.pump_list[i].kp_value.text())
            dict["ki"].append(self.pump_list[i].ki_value.text())
            dict["kd"].append(self.pump_list[i].kd_value.text())
            dict["motor_cal"].append(self.pump_list[i].motor_cal_value.text())
            dict["syringe_cal"].append(self.pump_list[i].syringe_cal_value.text())
            dict["syringe_volume"].append(self.pump_list[i].syringe_volume_value.text())
            dict["max_speed"].append(self.pump_list[i].max_speed_value.text())
            dict["active"].append(self.pump_list[i].active_value.text())
            dict["prca"].append(self.pump_list[i].prca_value.text())
            dict["prcb"].append(self.pump_list[i].prcb_value.text())

        # add pickle here to store dict

        self.settings_panel_window.close()

        print(self.pump_list)


# if __name__ == "__main__":
# def window():
#     app = QApplication(sys.argv)
#     win = SettingsPanel(dict)
#     win.show()  # shows window
#     sys.exit(app.exec_())  # clean exit when we close the window


# window()
