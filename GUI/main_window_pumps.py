from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import (QWidget, QPushButton, QLabel, QGridLayout, QLineEdit, QGroupBox, QScrollArea, QRadioButton,
                             QSlider)

class PumpArea(QScrollArea):
    """Scroll area containing pump widgets."""

    def __init__(self, pump_number, controller_settings, gui_settings, terminal, GUI_queues):
        super().__init__()

        # Queue and settings
        self.GUI_queues = GUI_queues
        self.terminal = terminal
        self.setWidgetResizable(True)
        self.horizontalScrollBar().setEnabled(True)
        self.verticalScrollBar().setEnabled(False)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Create layout
        pump = QWidget()
        self.setWidget(pump)
        pump_layout = QGridLayout()
        pump_layout.setAlignment(Qt.AlignLeft)
        pump.setLayout(pump_layout)

        self.n_pumps = pump_number
        self.controller_settings = controller_settings

        # Add Pump widgets
        self.Pumps = []
        starting_columns = [0, 4, 8, 12, 16, 20, 24, 28]
        for i in range(1, self.n_pumps + 1):
            self.Pumps.append(Pump(i, self.process_gui_settings(gui_settings, i-1), terminal, GUI_queues))
            pump_layout.addWidget(self.Pumps[-1], 0, starting_columns[i - 1], -1, 4)
            
        # Poll the queue every 1000 ms
        self.timer = QTimer()
        self.timer.timeout.connect(self.process_queue)
        self.timer.start(100)

    def process_gui_settings(self, gui_settings, pump_number):
        """Process gui_settings and returns values for a specific pump."""
        pump_values = []
        keys = ["pressure", "speed", "volume"]
        for key, value in gui_settings.items():
            if key in keys:
                pump_values.append(value[pump_number])
        pump_values.append(self.controller_settings['Syringe volume (μl)'][pump_number])

        return pump_values

    def process_queue(self):
        """Process To_GUI_queue and update widgets if new data is present."""
    
        ln = self.GUI_queues[0].qsize()
        need_to_update = False
        for i in range(ln):
            msg = self.GUI_queues[0].get()
    
            # Check if the queue data is for the graph
            if msg[0] == "ToGUI_PumpSpeeds":
                need_to_update = True
                # Convert incoming data to floats
                pump_speeds = [float(item) for item in msg[1]]
                for i, pump_speed in enumerate(pump_speeds):
                    self.Pumps[i].Speed = pump_speed

            elif msg[0] == "ToGUI_PumpPositions":
                need_to_update = True
                # Convert incoming data to floats
                pump_positions = [float(item) for item in msg[1]]
                for i, pump_position in enumerate(pump_positions):
                    self.Pumps[i].Position = pump_position

            else:
                self.GUI_queues[0].put(msg) #message is for someone else
                
            if need_to_update:
                for p_i in  self.Pumps:
                    p_i.update()

class Pump(QGroupBox):
    """Individual pump widget."""

    def __init__(self, pump_number, pump_values, terminal, GUI_queues):
        super().__init__()
        
        self.terminal = terminal
        self.GUI_queues = GUI_queues
        self.pump_number = pump_number
        self.Speed = 0.0
        self.Position = 0.0
        self.MaxPosition = pump_values[3]
        self.pres_reg_on = False
        
        # Set title and layout
        self.setTitle("Pump " + str(pump_number))
        self.pump_layout = QGridLayout(self)
        self.setLayout(self.pump_layout)

        # Set validators
        self.validator = QDoubleValidator(self)
        self.validator.setNotation(QDoubleValidator.ScientificNotation)
        self.volume_validator = QDoubleValidator(self)
        self.validator.setNotation(QDoubleValidator.ScientificNotation)
        
        # Create and configure elements
        self.pressure_label = QLabel(self, text="Pressure (kPa)", alignment=Qt.AlignLeft)
        self.pressure_box = QLineEdit(text=pump_values[0])
        self.pressure_box.setValidator(self.validator)
        self.pressure_box.returnPressed.connect(self.on_pressure_entered)
        self.pressure_set = QPushButton(text="Pressure set")
        self.pressure_set.clicked.connect(self.on_pressure_entered)
        self.pressure_regulate = QPushButton(text="Pressure regulate")
        self.pressure_regulate.clicked.connect(self.on_pressure_regulate)

        self.speed_label = QLabel(self, text="Speed (μl/s)")
        self.speed_box = QLineEdit(text=pump_values[1])
        self.speed_box.setValidator(self.validator)
        self.speed_box.returnPressed.connect(self.on_speed_entered)

        self.volume_label = QLabel(self, text="Volume (μl)")
        self.volume_box = QLineEdit(text=pump_values[2])
        self.volume_box.setValidator(self.volume_validator)
        self.volume_box.returnPressed.connect(lambda: self.on_volume_entered(True))

        self.movebk_button = QPushButton(text="Move Back")
        self.movebk_button.clicked.connect(lambda: self.on_volume_entered(False))        
        self.move_button = QPushButton(text="Move")
        self.move_button.clicked.connect(lambda: self.on_volume_entered(True))

        self.move_absolute = QRadioButton("Move absolute")
        self.move_absolute.clicked.connect(self.on_movetype)
        self.move_relative = QRadioButton("Move relative")
        self.move_relative.clicked.connect(self.on_movetype)
        self.move_relative.setChecked(True)

        self.home_box = QGroupBox("Home pump")
        self.home_layout = QGridLayout(self)
        self.home_box.setLayout(self.home_layout)

        self.home_up_button = QPushButton(text="Max")
        self.home_up_button.clicked.connect(lambda: self.on_home(False))
        self.home_down_button = QPushButton(text="Zero")
        self.home_down_button.clicked.connect(lambda: self.on_home(True))

        self.home_layout.addWidget(self.home_up_button, 0, 1, 1, 1)
        self.home_layout.addWidget(self.home_down_button, 0, 0, 1, 1)

        self.speed_display = QLabel(self, text="Speed (μl/s): 0.0")
        self.speed_display.setFixedWidth(125)
        self.position_display = QLabel(self, text="Position (μl): 0.0")
        self.position_display.setFixedWidth(125)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setValue(100)
        self.slider.sliderReleased.connect(self.on_slider_released)

        # Add elements to layout
        self.pump_layout.addWidget(self.pressure_label, 0, 0)
        self.pump_layout.addWidget(self.pressure_box, 0, 1)
        self.pump_layout.addWidget(self.pressure_set, 1, 0)
        self.pump_layout.addWidget(self.pressure_regulate, 1, 1)

        self.pump_layout.addWidget(self.speed_label, 2, 0)
        self.pump_layout.addWidget(self.speed_box, 2, 1)
        self.pump_layout.addWidget(self.volume_label, 3, 0)
        self.pump_layout.addWidget(self.volume_box, 3, 1)
        self.pump_layout.addWidget(self.movebk_button, 4, 1)
        self.pump_layout.addWidget(self.move_button, 4, 0)

        self.pump_layout.addWidget(self.move_absolute, 5, 0)
        self.pump_layout.addWidget(self.move_relative, 5, 1)

        self.pump_layout.addWidget(self.home_box, 6, 0, 1, -1)

        self.pump_layout.addWidget(self.speed_display, 7, 0)
        self.pump_layout.addWidget(self.position_display, 8, 0)
        self.pump_layout.addWidget(self.slider, 8, 1, 1, -1, Qt.AlignCenter)

    def update(self):
        self.speed_display.setText (f"Speed (μl/s): {self.Speed:.2f}")
        self.position_display.setText (f"Position (μl): {self.Position:.0f}")
        value = self.Position/self.MaxPosition*100
        self.slider.setValue(int(round(value)))

    def on_pressure_entered(self):
        # This function is called when the user enters data in pressure_box
        value = float(self.pressure_box.text())
        self.GUI_queues[1].put(["FromGUI_Target", [self.pump_number-1, value]])
        self.terminal.print_text(f"Target {self.pump_number-1} {value}")
        
        
    def on_pressure_regulate(self):
        if self.pres_reg_on:
            self.GUI_queues[1].put(["FromGUI_StopAdjust", [self.pump_number-1]])
            self.terminal.print_text(f"StopAdjust {self.pump_number-1}")
            self.pres_reg_on = False
        
        else:
            self.on_pressure_entered()
            self.GUI_queues[1].put(["FromGUI_StartAdjust", [self.pump_number-1]])
            self.terminal.print_text(f"StartAdjust {self.pump_number-1}")
            self.pres_reg_on = True
            
    def on_speed_entered(self):
        # This function is called when the user enters data in pressure_box
        value = float(self.speed_box.text())
        self.GUI_queues[1].put(["FromGUI_Speed", [self.pump_number-1, value]])
        self.terminal.print_text(f"Speed {self.pump_number-1} {value}")

    def on_volume_entered(self, forward):
        # This function is called when the user enters data in pressure_box
        value = float(self.volume_box.text())
        if not forward:
            value = -value
        self.on_speed_entered()
        if self.move_absolute.isChecked():
            self.GUI_queues[1].put(["FromGUI_MoveAbs", [self.pump_number-1, value]])
            self.terminal.print_text(f"MoveAbs {self.pump_number-1} {value}")
        else:
            self.GUI_queues[1].put(["FromGUI_MoveRel", [self.pump_number-1, value]])
            self.terminal.print_text(f"MoveRel {self.pump_number-1} {value}")
            
    def on_movetype(self):
        if self.move_relative.isChecked():
            self.movebk_button.setEnabled(True)
            self.volume_validator.setBottom(float('-inf'))
        else:
            value = float(self.volume_box.text())
            self.volume_box.setText(str(abs(value)))
            self.movebk_button.setEnabled(False)
            self.volume_validator.setBottom(0.0)
    
    def on_home(self, zero_dir):
        value = 1
        if zero_dir:
            value = 0
        self.GUI_queues[1].put(["FromGUI_Home", [self.pump_number-1, value]])
        self.terminal.print_text(f"Home {self.pump_number-1} {value}")
            
    def on_slider_released(self):
        value = self.slider.value()
        value = value / 100.0 * self.MaxPosition
        self.on_speed_entered()
        self.GUI_queues[1].put(["FromGUI_MoveAbs", [self.pump_number-1, value]])
        self.terminal.print_text(f"MoveAbs {self.pump_number-1} {value}")
        


