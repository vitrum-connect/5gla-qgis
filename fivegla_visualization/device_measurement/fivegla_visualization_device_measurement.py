from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from .fivegla_visualization_device_measurement_dialog import FiveGLaVisualizationDeviceMeasurementDialog
from qgis.PyQt.QtWidgets import QPushButton, QGraphicsScene, QGraphicsView

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
        x = np.random.normal(size=50)
        y = np.random.normal(size=(3, 50))
        axes.legend()
        axes.grid()
        for i in range(3):
            axes.plot(x, y[i], "-k", label="test-{}".format(i))

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
