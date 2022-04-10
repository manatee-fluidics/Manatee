from PyQt5.QtWidgets import QGroupBox, QVBoxLayout
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


# class Graph(QWidget):
#     def __init__(self):
#         super(Graph, self).__init__()
#
#         # define and set QWidget layout
#         layout = QGridLayout()
#         self.setLayout(layout)
#
#         # define and add QGroupBox to QWidget's layout
#         self.graph_box = QGroupBox("Graph")
#         layout.addWidget(self.graph_box)
#
#         # define and set the layout of the QGroupBox
#         self.graph_layout = QHBoxLayout(self)
#         self.graph_box.setLayout(self.graph_layout)
#
#         label = QLabel("GRAPH")
#         self.graph_layout.addWidget(label)

class Graph(QGroupBox):
    def __init__(self):
        super(Graph, self).__init__()

        # define and set the layout of the QGroupBox
        self.setTitle("Graph")
        # self.graph_layout = QGridLayout(self)
        # self.setLayout(self.graph_layout)

        # a figure instance to plot on
        self.figure = plt.figure(figsize=(4, 2), dpi=75)

        # this is the Canvas Widget that displays the 'figure'
        # it takes the 'figure' instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        # creating a Vertical Box layout
        plot_layout = QVBoxLayout()

        # adding tool bar to the layout
        plot_layout.addWidget(self.toolbar)

        # data for the graph
        data = [60, 59, 49, 51, 49, 52, 53]
        # clearing old figure
        self.figure.clear()
        # create an axis
        ax = self.figure.add_subplot(111)

        # set labels
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Pressure (kPa)')

        # plot data
        ax.plot(data, '*-')

        # refresh canvas
        self.canvas.draw()

        # adding canvas to the layout
        plot_layout.addWidget(self.canvas)

        # setting layout to the main window
        self.setLayout(plot_layout)

        # # clearing old figure
        # self.figure.clear()

        # # create the figure and axis objects
        # fig, ax = plt.subplots()

        # # save and show the plot
        # fig.savefig('static_plot.png')
        # plt.show()
