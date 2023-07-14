from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import (
    QWidget, 
    QPushButton, 
    QLabel, 
    QGridLayout, 
    QLineEdit, 
    QHBoxLayout, 
    QCheckBox, 
    QGroupBox
)
from PyQt5.QtCore import Qt

class Controls(QWidget):
    def __init__(self, gui_settings, terminal, GUI_queues):
        super().__init__()
        self.setLayout(QGridLayout())
        self.controls_box = self._create_controls_box(gui_settings, terminal, GUI_queues)
        self.layout().addWidget(self.controls_box)

    def _create_controls_box(self, gui_settings, terminal, GUI_queues):
        box = QGroupBox("Controls")
        layout = QHBoxLayout()
        box.setLayout(layout)
        layout.addWidget(Switches(terminal, GUI_queues))
        layout.addWidget(Slaves(terminal, GUI_queues))
        layout.addWidget(Programming(gui_settings, terminal, GUI_queues))
        return box


class Switches(QGroupBox):
    def __init__(self, terminal, GUI_queues):
        super().__init__("Switches")
        self.GUI_queues = GUI_queues
        self.terminal = terminal
        self.setLayout(QHBoxLayout())
        solenoid_names = ["Solenoid 1", "Solenoid 2", "Solenoid 3"]
        
        for name in solenoid_names:
            self.layout().addWidget(self._create_checkbox(name))

    def _create_checkbox(self, name):
        box = QCheckBox(name)
        box.setChecked(False)

        # Connect the stateChanged event to a function
        box.stateChanged.connect(lambda state, x=name[-1]: self.solenoid_state_changed(x, state))
        return box

    def solenoid_state_changed(self, solenoid_number, state):
        """Function to run when the state of a checkbox is changed."""
        # Convert Qt checkbox state to 0 or 1
        state = 1 if state == Qt.Checked else 0

        # Send message to GUI queue
        self.GUI_queues[1].put(["FromGUI_Solenoid", [int(solenoid_number)-1, state]])
        self.terminal.print_text ("Solenoid %d %d"%(int(solenoid_number)-1, state))

class Slaves(QGroupBox):
    def __init__(self, terminal, GUI_queues):
        super().__init__("Slaves")
        self.terminal = terminal
        self.setLayout(QHBoxLayout())
        self.layout().addWidget(self._create_button("Switch slave"))
        self.layout().addWidget(self._create_button("TTL slave"))
        self.layout().addWidget(self._create_button("Multipinch slave"))

    def _create_button(self, text):
        button = QPushButton(text)
        button.setEnabled(False)
        return button


class Programming(QGroupBox):
    def __init__(self, gui_settings, terminal, GUI_queues):
        super().__init__("Programming")
        self.GUI_queues = GUI_queues
        self.terminal = terminal  # Store the terminal instance
        self.setLayout(QHBoxLayout())
        self.layout().addWidget(self._create_label("Wait time (s):"))
        self.waittime_textbox = self._create_textbox(gui_settings)  # Store the textbox instance
        self.layout().addWidget(self.waittime_textbox)
        self.layout().addWidget(self._create_button("Send"))

    def _create_label(self, text):
        label = QLabel(self)
        label.setText(text)
        label.setAlignment(Qt.AlignLeft)
        return label

    def _create_textbox(self, gui_settings):
        validator = QDoubleValidator(self)
        validator.setNotation(QDoubleValidator.ScientificNotation)
        textbox = QLineEdit()
        textbox.setValidator(validator)
        textbox.setText(gui_settings['waittime'])
        return textbox

    def _create_button(self, text):
        button = QPushButton(text)
        button.clicked.connect(self.send_click)  # Connect the button click to the send_click function
        return button

    def send_click(self):
        """Function to run when the Send button is clicked."""
        # Get the current value of the waittime textbox
        waittime = self.waittime_textbox.text()

        # Send the waittime to the terminal
        self.terminal.print_text(f"WaitTime {waittime}")