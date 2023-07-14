import sys
import multiprocessing as mp
from PyQt5.QtGui import QIcon, QDoubleValidator
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QLabel, QGridLayout, QDesktopWidget, QLineEdit, QHBoxLayout
from PyQt5.QtCore import Qt


class SettingsPanel(QMainWindow):
    def __init__(self, n_pumps, controller_settings, GUI_queues):
        super(SettingsPanel, self).__init__()

        self.setCentralWidget(QWidget(self))
        self.cw_layout = QGridLayout()
        self.cw_layout.setAlignment(Qt.AlignLeft)
        self.centralWidget().setLayout(self.cw_layout)

        self.settings = controller_settings
        self.text = Text()

        self.n_pumps = n_pumps
        self.pump_list = []
        for i in range(1, 6):
            pump = Pump(i, self.process_settings(self.settings, i - 1))
            self.cw_layout.addWidget(pump, 0, i, 11, 1, Qt.AlignLeft)
            self.pump_list.append(pump)
            
        self.GUI_queues = GUI_queues

        self.buttons = Buttons(self, self.settings, self.pump_list, self.GUI_queues)

        self.cw_layout.addWidget(self.text, 0, 0, 11, 1, Qt.AlignRight)
        self.cw_layout.addWidget(self.buttons, 12, 0, 1, -1, Qt.AlignCenter)

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Settings")
        self.setWindowIcon(QIcon("manatee_icon_square.png"))
        self.center()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def process_settings(self, dict, column_number):
        settings_values = []
        for key, value in dict.items():
            settings_values.append(value[column_number])
        return settings_values


class Text(QWidget):
    def __init__(self):
        super(Text, self).__init__()

        self.text_layout = QVBoxLayout(self)
        self.labels = ["Kp", "Ki", "Kd", "Motor cal (steps/mm)", "Syringe cal (μl/mm)", "Syringe volume (μl)", 
                       "Max speed (mm/sec)", "Active", "Pressure cal A", "Pressure cal B", "Sensor unit"]

        for label in [""] + self.labels:
            lbl = QLabel(self)
            lbl.setText(label)
            lbl.setAlignment(Qt.AlignRight)
            self.text_layout.addWidget(lbl)


class Pump(QWidget):
    def __init__(self, pump_number, settings_list):
        super(Pump, self).__init__()

        self.edited_values = []
        self.pump_number = pump_number
        self.pump_layout = QVBoxLayout(self)
        self.settings = settings_list
        self.validator = QDoubleValidator(self)
        self.validator.setNotation(QDoubleValidator.ScientificNotation)

        self.pump = QLabel(self)
        self.pump.setText("Pump " + str(self.pump_number))
        self.pump.setAlignment(Qt.AlignLeft)
        self.pump_layout.addWidget(self.pump)

        for i, setting in enumerate(self.settings):
            field = QLineEdit()
            field.setToolTip(Text().labels[i])
            field.setValidator(self.validator)
            field.setText(str(setting))
            self.pump_layout.addWidget(field)


class Buttons(QWidget):
    def __init__(self, settings_window, controller_settings, pump_list, GUI_queues):
        super(Buttons, self).__init__()

        self.settings_window = settings_window
        self.controller_settings = controller_settings
        self.pump_list = pump_list
        self.GUI_queues = GUI_queues
        self.buttons_layout = QHBoxLayout(self)
        self.button_save = QPushButton("Save", self)
        self.button_cancel = QPushButton("Cancel", self)

        self.button_save.clicked.connect(self.save_settings)
        self.button_cancel.clicked.connect(self.settings_window.close)

        self.buttons_layout.addWidget(self.button_save)
        self.buttons_layout.addWidget(self.button_cancel)

    def save_settings(self):
        for i, pump in enumerate(self.pump_list):
            for j, field in enumerate(pump.findChildren(QLineEdit)):
                self.controller_settings[Text().labels[j]][i] = float(field.text())

        self.GUI_queues[1].put(["FromGUI_ControllerSettings", self.controller_settings])

        self.settings_window.close()
        
if __name__ == "__main__":
    def window():
        controller_settings = { 'Kp': [0.1, 0.1, 0.1, 0.1, 0.1],
                                'Ki': [1e-04, 1e-04, 1e-04, 1e-04, 1e-04],
                                'Kd': [1e-04, 1e-04, 0.0, 0.001, 0.001],
                                'Motor cal (steps/mm)': [4000.0, 4000.0, 4000.0, 4000.0, 4000.0],
                                'Syringe cal (μl/mm)': [642.42426, 369.836, 369.836, 369.836, 369.836],
                                'Syringe volume (μl)': [74599.91, 33289.953, 33289.953, 33289.953, 33289.953],
                                'Max speed (mm/sec)': [2.75, 2.5, 2.5, 2.5, 2.5],
                                'Active': [1.0, 1.0, 1.0, 1.0, 1.0],
                                'Pressure cal A': [0.018, 0.018, 0.018, 0.018, 0.018],
                                'Pressure cal B': [0.04, 0.04, 0.04, 0.04, 0.04],
                                'Sensor unit': [0.0, 0.0, 255.0, 0.0, 0.0]}
        n_pumps = len(controller_settings['Kp'])
        GUI_queues = [mp.Queue(), mp.Queue()]
        app = QApplication(sys.argv)
        win = SettingsPanel(n_pumps, controller_settings, GUI_queues)
        win.show()  # shows window
        sys.exit(app.exec_())  # clean exit when we close the window
    
    
    window()
