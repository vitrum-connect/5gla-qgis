from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from .fivegla_visualization_device_measurement_dialog import FiveGLaVisualizationDeviceMeasurementDialog
from qgis.PyQt.QtWidgets import QPushButton, QGraphicsScene, QGraphicsView

import datetime
import numpy as np


class FiveGLaVisualizationDeviceMeasurement:
    """This class enables the user to visualize the device measurements on the graph
    """

    def __init__(self, iface, callback_first_start):
        """

        :param iface: A reference to the QGIS Interface
        :param callback_first_start: A callback to a method which must run before the first start
        """
        self.dlg = None
        self.iface = iface
        self.first_start = True
        self.callback_first_start = callback_first_start

    def run(self):
        """ Create the dialog with elements (after translation) and keep reference
        Only create GUI ONCE in callback, so that it will only load when the plugin is started

        :return: None
        """

        if self.first_start:
            self.callback_first_start()
            self.dlg = FiveGLaVisualizationDeviceMeasurementDialog()
            self.dlg.btnDraw = self.dlg.findChild(QPushButton, "btnDraw")
            self.dlg.btnClear = self.dlg.findChild(QPushButton, "btnClear")
            self.dlg.plotView = self.dlg.findChild(QGraphicsView, "plotView")
            self.dlg.btnDraw.clicked.connect(self.draw)
            self.dlg.btnClear.clicked.connect(self.clear)
            self.first_start = False
            self.dlg.scene = QGraphicsScene()

        self.dlg.show()
        result = self.dlg.exec_()
        if result:
            pass

    def draw(self):
        """Draws the graph on the plot view

        :return: None
        """
        figure = Figure()
        axes = figure.gca()
        axes.set_title('Title')
        # Create a two-dimensional double array with 10 numbers
        # Assume data is an array of tuples, where each tuple is (date, y)
        data = np.array([
            (datetime.datetime(2022, 1, 1), 1),
            (datetime.datetime(2022, 1, 2), 2),
            (datetime.datetime(2022, 1, 3), 3),
            (datetime.datetime(2022, 1, 4), 4),
            (datetime.datetime(2022, 1, 5), 5),
            (datetime.datetime(2022, 1, 6), 6),
            (datetime.datetime(2022, 1, 7), 7),
            (datetime.datetime(2022, 1, 8), 8),
            (datetime.datetime(2022, 1, 9), 9),
            (datetime.datetime(2022, 1, 10), 10)
        ])

        x, y = zip(*data)

        axes.legend()
        axes.grid()
        axes.plot(x, y, "-k", label="test")

        canvas = FigureCanvas(figure)
        proxy_widget = self.dlg.scene.addWidget(canvas)
        self.dlg.plotView.setScene(self.dlg.scene)
        self.dlg.plotView.fitInView(proxy_widget)
        self.dlg.plotView.show()

    def clear(self):
        """Clears the plot view

        :return: None
        """
        self.dlg.scene.clear()
        self.dlg.plotView.viewport().update()
