import pandas as pd
from PyQt5.QtWidgets import QGroupBox, QVBoxLayout
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtCore import QThread, QTimer
import pyqtgraph as pg

class Graph(QGroupBox):
    """Graph widget for displaying data plots."""

    def __init__(self, n_pumps, gui_settings, GUI_queues):
        super().__init__()

        # GUI Queue
        self.GUI_queues = GUI_queues
        self.n_pumps = n_pumps
        self.gui_settings = gui_settings

        # Set title
        self.setTitle("Graph")

        # Create pyqtgraph plot widget
        self.plot_widget = pg.PlotWidget(background='w')
        self.plot_widget.showGrid(x=True, y=True)  # Show axes
        self.plot_widget.setLabel('left', 'Pressure (kPa)')  # Y-axis label
        self.plot_widget.setLabel('bottom', 'Time (s)')  # X-axis label
        self.plot_widget.setXRange(0, self.gui_settings['Graph_limits'][0], padding=0)  # X-axis range
        self.plot_widget.setYRange(0, self.gui_settings['Graph_limits'][1], padding=0)  # Y-axis range
        self.plot_widget.getViewBox().setMouseEnabled(x=False, y=False)

        # Create layout and add plot widget
        plot_layout = QVBoxLayout()
        plot_layout.addWidget(self.plot_widget)

        # Initialize data
        self.data = pd.DataFrame(columns=["time"] + ["Pump %d" % x for x in range(self.n_pumps)])

        # Add canvas to layout and set layout
        self.setLayout(plot_layout)

        # Poll the queue every 1000 ms
        self.timer = QTimer()
        self.timer.timeout.connect(self.process_queue)
        self.timer.start(100)

    def update_graph(self):
        """Update the graph with new data."""
        # Check if range was modified
        x_range, y_range = self.plot_widget.viewRange()
        x_range = int(x_range[1]-x_range[0])
        y_range = int(y_range[1]-y_range[0])
        if x_range != self.gui_settings['Graph_limits'][0] or y_range != self.gui_settings['Graph_limits'][1]:
            self.gui_settings['Graph_limits'] = [x_range, y_range]
            self. GUI_queues[1].put(["FromGUI_GUISettings", self.gui_settings])
        
        # Clear plot
        self.plot_widget.clear()

        # Define colors for the traces
        colors = [QColor(32,178,170), QColor(54,117,136), QColor(0,128,128), QColor(49,145,119), QColor(102,221,170)]
        font = QFont()
        font.setPixelSize(24)   
        pg.setConfigOptions(antialias=True)
        
        # Plot data
        mtail = int(self.gui_settings['Graph_limits'][0])
        plotdata = self.data.tail(mtail)
        plotdata = plotdata.reset_index(drop=True)
        for i, column in enumerate(plotdata.columns[1:]):  # Skip the "time" column
            color = colors[i % len(colors)]  # Choose color
            self.plot_widget.plot(plotdata["time"], plotdata[column], pen=pg.mkPen(color, width=2))
    
            # Add labels to the last point of each trace
            last_time = self.data["time"].iloc[-1]
            last_value = self.data[column].iloc[-1]
            label = pg.TextItem(text=column, color='black', anchor=(1, 1), angle=45)
            label.setFont(font)
            self.plot_widget.addItem(label)
            label.setPos(last_time, last_value)
            if plotdata["time"].max() > self.gui_settings['Graph_limits'][0]:
                self.plot_widget.setXRange(plotdata["time"].max() - self.gui_settings['Graph_limits'][0], plotdata["time"].max(), padding=0)

    def process_queue(self):
        """Process To_GUI_queue and update graph if new data is present."""

        ln = self.GUI_queues[0].qsize() #process To_GUI
        need_to_draw = False #flag to remember to draw after we processed all incoming
        for i in range(ln):
            msg = self.GUI_queues[0].get()

            # Check if the queue data is for the graph
            if msg[0] == "ToGUI_GraphData":
                # Convert incoming data to floats
                numeric_data = [float(item) for item in msg[1]]

                # Append new data to the existing DataFrame
                new_data = pd.DataFrame([numeric_data], columns=self.data.columns)
                self.data = pd.concat([self.data, new_data], ignore_index=True)
                need_to_draw = True
            else:
                self.GUI_queues[0].put(msg) #message is for someone else
        if need_to_draw:
            # Update the graph
            self.update_graph()
