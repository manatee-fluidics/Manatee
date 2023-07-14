import multiprocessing as mp
import pandas as pd
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QGridLayout, QDesktopWidget, \
    QHBoxLayout, QGroupBox, QApplication, QPlainTextEdit, QLineEdit, QFileDialog, QSizePolicy
from PyQt5.QtCore import Qt
import sys

import settings_panel
import main_window_controls
import main_window_pumps
import main_window_graph


class MainWindow(QMainWindow):  # inherits all properties from QMainWindow class
    """Creates Main Window with all functions."""
    def __init__(self, controller_settings, gui_settings, GUI_queues):
        super(MainWindow, self).__init__()  # parent constructor
        self.GUI_queues = GUI_queues
        # QMainWindow has a central widget that is a container for widgets, it has its own layout
        # create cw, set layout and alignment
        self.setCentralWidget(QWidget(self))
        self.cw_layout = QGridLayout()
        self.cw_layout.setAlignment(Qt.AlignTop)
        self.centralWidget().setLayout(self.cw_layout)
        self.controller_settings = controller_settings
        self.gui_settings = gui_settings
        self.n_pumps = len([x for x in controller_settings["Active"] if x==1])
        self.protocol = None
        # defining widgets
        # ButtonBar gets self because later a button will close the window
        self.terminal = Terminal(self.GUI_queues)
        self.buttonbar = ButtonBar(self, self.n_pumps, self.controller_settings, self.GUI_queues)
        self.controls = main_window_controls.Controls(self.gui_settings, self.terminal, self.GUI_queues)
        self.pump_area = main_window_pumps.PumpArea(self.n_pumps, self.controller_settings, self.gui_settings, self.terminal, self.GUI_queues)
        self.graph = main_window_graph.Graph(self.n_pumps, self.gui_settings, self.GUI_queues)


        # add widgets to main window
        # name, starting row, starting col, rowspan, colspan (till the end is -1), alignment
        # self.cw_layout.addWidget(self.buttonbar, 0, 0, 1, 12)
        # self.cw_layout.addWidget(self.controls, 0, 12, 1, -1)
        # self.cw_layout.addWidget(self.pump_area, 1, 0, 2, -1)
        # self.cw_layout.addWidget(self.graph, 3, 0, 2, 20)
        # self.cw_layout.addWidget(self.terminal, 3, 20, 2, -1)
        self.pump_area.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.cw_layout.addWidget(self.buttonbar, 0, 0, 1, 2)
        self.cw_layout.addWidget(self.controls, 0, 2, 1, -1)
        self.cw_layout.addWidget(self.pump_area, 1, 0, 2, -1)
        self.cw_layout.addWidget(self.graph, 3, 0, 1, 4)
        self.cw_layout.addWidget(self.terminal, 3, 4, 1, -1)
        
        self.initUI()

    def initUI(self):
        """Initializes the Main window with all the attributes specified below."""

        self.setWindowTitle("Manatee Fluidics")
        self.setWindowIcon(QIcon("manatee_icon_square.png"))

        # open window in full size
        #self.showMaximized()

        # self.setGeometry(1300, 200, 1000, 1500)
        # xpos, ypos, width, height (in pixels)
        # if xpos and ypos are 0, win shows up on the top-left corner;
        # 100, 100 moves the top-left corner of the window to the right and down

        
        # Get the current geometry of the window
        #geometry = self.geometry()
        
        # Set the new geometry, keeping the same x, y, and width, but changing the height
        #self.setGeometry(geometry.x(), geometry.y(), geometry.width(), 1500)

        # open not maximized, center of screen
        #self.center()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def closeEvent(self, event):
        self.GUI_queues[1].put(["FromGUI_Exit", []])
        self.GUI_queues[1].put(["FromGUI_SerialDisconnect", []])
        event.accept()  # let the window close

class ButtonBar(QWidget):
    """This class defines the layout and function of the buttons which belong to the button bar"""
    def __init__(self, MainWindow, n_pumps, controller_settings, GUI_queues):
        super(ButtonBar, self).__init__()
        
        self.n_pumps = n_pumps
        self.controller_settings = controller_settings
        self.GUI_queues = GUI_queues
        # variable to store the current instance of the main window
        self.main_window = MainWindow

        # define and set QWidget layout
        layout = QGridLayout()
        self.setLayout(layout)

        # define and add QGroupBox to QWidget's layout
        self.button_box = QGroupBox("Connection properties")
        layout.addWidget(self.button_box)

        # define and set the layout of the QGroupBox
        self.buttons_layout = QGridLayout(self)
        self.button_box.setLayout(self.buttons_layout)

        #self.button_disconnect = QPushButton()
        #self.button_disconnect.setText("Disconnect")
        #self.button_disconnect.clicked.connect(lambda: self.disconnect_click())

        self.button_settings = QPushButton()
        self.button_settings.setText("Settings")
        self.button_settings.clicked.connect(lambda: self.open_settings_panel())

        self.button_loadprot = QPushButton()
        self.button_loadprot.setText("Load Protocol")
        self.button_loadprot.clicked.connect(lambda: self.load_protocol())

        self.button_runprot = QPushButton()
        self.button_runprot.setText("Run Protocol")
        self.button_runprot.clicked.connect(lambda: self.run_protocol())
        self.button_runprot.setEnabled(False)

        self.button_uploadprot = QPushButton()
        self.button_uploadprot.setText("Upload Protocol")
        self.button_uploadprot.clicked.connect(lambda: self.upload_protocol())
        self.button_uploadprot.setEnabled(False)

        # add all above defined buttons to the class layout
        #self.buttons_layout.addWidget(self.button_disconnect, 0, 0, 1, 1)
        self.buttons_layout.addWidget(self.button_settings, 0, 0, 1, 3)
        self.buttons_layout.addWidget(self.button_loadprot, 1, 0, 1, 1)
        self.buttons_layout.addWidget(self.button_runprot, 1, 1, 1, 1)
        self.buttons_layout.addWidget(self.button_uploadprot, 1, 2, 1, 1)

    # def disconnect_click(self):
    #     """Closes the current instance of the main window"""
    #     self.GUI_queues.put(["FromGUI_SerialDisconnect", []])
    #     self.main_window.close()

    def open_settings_panel(self):
        self.ui = settings_panel.SettingsPanel(self.n_pumps, self.controller_settings, self.GUI_queues)
        self.ui.setWindowModality(Qt.ApplicationModal)  # blocks main window while settings window is open
        self.ui.show()

    def load_protocol(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self, "Load Protocol", "", "Text Files (*.txt)", options=options)

        if file_name:
            try:
                self.protocol = pd.read_csv(file_name)
                # Enable the buttons if the file is loaded successfully
                self.button_runprot.setEnabled(True)
                self.button_uploadprot.setEnabled(True)
            except Exception as e:
                # You may want to show an error message here
                print(f"Error loading file: {e}")
            
    def run_protocol(self):
        self.GUI_queues[1].put(["FromGUI_RunProtocol", self.protocol])

    def upload_protocol(self):
        self.GUI_queues[1].put(["FromGUI_UploadProtocol", self.protocol])

class Terminal(QWidget):
    """Terminal widget for text display and user input."""

    def __init__(self, GUI_queues):
        super(Terminal, self).__init__()
        self.GUI_queues = GUI_queues

        # Define and set QWidget layout
        layout = QGridLayout()
        self.setLayout(layout)

        # Define and add QGroupBox to QWidget's layout
        self.terminal_box = QGroupBox("Terminal")
        layout.addWidget(self.terminal_box)

        # Define and set the layout of the QGroupBox
        self.terminal_layout = QGridLayout(self)
        self.terminal_box.setLayout(self.terminal_layout)

        # Add a text display box
        # name, starting row, starting col, rowspan, colspan (till the end is -1), alignment
        self.text_display = QPlainTextEdit()
        self.text_display.setReadOnly(True)  # Make it read-only
        self.terminal_layout.addWidget(self.text_display, 0, 0, 1, 4)

        # Add a text input box
        self.text_input = QLineEdit()
        self.terminal_layout.addWidget(self.text_input, 1, 0, 1, 3)

        # Add a send button
        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_text)  # Connect to the send_text method
        self.terminal_layout.addWidget(self.send_button, 1, 3, 1, 1)

    def send_text(self):
        """Handle send button clicks."""
        text = self.text_input.text()
        self.text_input.clear()

        # Do something with the text...
        self.text_display.appendPlainText(f">>> {text}")

    def print_text(self, text):
        """Handle text prints."""
        self.text_display.appendPlainText(f">>> {text}")



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
        gui_settings = {'baud': '250000',
                          'waittime': '3000',
                          'pressure': ['20', '10', '20', '20', '20'],
                          'speed': ['2000', '2000', '120', '120', '240'],
                          'volume': ['6000', '-9000', '30', '30', '30'],
                          'time': ['60', '60', '60', '60', '60'],
                          'port': 'Test',
                          'Graph_limits': [500 ,50]}
        """
        with open('gui_settings.p', 'wb') as f:
            # Use pickle.dump to write the dictionary back to the file
            pickle.dump(gui_settings, f)
        """
        
        
        graphdatas = [  [0, 27, 22, 70, 90, 96],
        [515, 74, 96, 96, 55, 7],
        [1017, 42, 61, 20, 66, 54],
        [1532, 43, 27, 86, 9, 13],
        [2048, 36, 80, 74, 73, 97],
        [2564, 22, 16, 75, 30, 92],
        [3079, 39, 32, 70, 75, 71],
        [3595, 69, 50, 31, 100, 87],
        [4111, 63, 86, 9, 71, 61],
        [4626, 8, 2, 78, 11, 55],
        [5142, 89, 40, 90, 20, 0],
        [5657, 65, 38, 69, 48, 42],
        [6173, 5, 21, 58, 47, 89],
        [6673, 15, 8, 55, 72, 36],
        [7189, 78, 22, 46, 58, 11],
        [7704, 0, 36, 70, 72, 30],
        [8220, 95, 27, 69, 1, 26],
        [8720, 38, 45, 60, 76, 73],
        [9236, 82, 83, 12, 10, 16],
        [9751, 22, 32, 74, 57, 87],
        [10267, 40, 7, 90, 20, 35],
        [10783, 54, 3, 27, 35, 34],
        [11298, 17, 79, 79, 37, 64],
        [11814, 63, 81, 26, 90, 43],
        [12314, 75, 27, 15, 87, 84],
        [12830, 90, 59, 19, 72, 30],
        [13345, 3, 75, 26, 36, 38],
        [13861, 57, 66, 46, 95, 86],
        [14377, 15, 73, 8, 87, 53],
        [14892, 31, 15, 25, 85, 87],
        [15405, 41, 63, 55, 36, 60],
        [15920, 60, 15, 41, 68, 23],
        [16425, 5, 25, 34, 18, 81],
        [16940, 97, 88, 71, 52, 33],
        [17456, 75, 35, 32, 67, 49],
        [17972, 51, 4, 59, 46, 19],
        [18487, 50, 9, 30, 62, 14],
        [19003, 11, 25, 88, 45, 21],
        [19518, 49, 35, 68, 49, 17]]
        
        pump_status = [["ToGUI_PumpSpeeds", [10.1, 5.3, 30.2, 0.6, 7.1]],
                       ["ToGUI_PumpPositions", [50000, 25000, 33289.953, 12000, 0.0]]]
        
        GUI_queues = [mp.Queue(), mp.Queue()] #To_Gui and From_GUI
        for row in graphdatas:
            GUI_queues[0].put(["ToGUI_GraphData", row])
        for row in pump_status:
            GUI_queues[0].put(row)
            
        

        app = QApplication(sys.argv)
        win = MainWindow(controller_settings, gui_settings, GUI_queues)
        win.show()
        sys.exit(app.exec_())    
    
    window()
