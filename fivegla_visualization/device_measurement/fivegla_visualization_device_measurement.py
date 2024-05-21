from matplotlib.figure import Figure

# felix
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

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
            self.dlg.btnDraw.clicked.connect(self.draw2)
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
        figure = Figure(figsize=(9, 6.5))
        axes = figure.gca()
        axes.set_title('Title')
        # Create a two-dimensional double array with 10 numbers
        # Assume data is an array of tuples, where each tuple is (date, y)
        data = np.array([
            (datetime.datetime.fromisoformat('2022-01-01T12:00:00'), 1),
            (datetime.datetime.fromisoformat('2022-01-02T13:00:00'), 2),
            (datetime.datetime.fromisoformat('2022-01-03T14:00:00'), 3),
            (datetime.datetime.fromisoformat('2022-01-04T15:00:00'), 4),
            (datetime.datetime.fromisoformat('2022-01-05T16:00:00'), 5),
            (datetime.datetime.fromisoformat('2022-01-06T17:00:00'), 6),
            (datetime.datetime.fromisoformat('2022-01-07T18:00:00'), 7),
            (datetime.datetime.fromisoformat('2022-01-08T19:00:00'), 8),
            (datetime.datetime.fromisoformat('2022-01-09T20:00:00'), 9),
            (datetime.datetime.fromisoformat('2022-01-10T21:00:00'), 10)
        ])

        x, y = zip(*data)

        axes.legend()
        axes.grid()
        axes.plot(x, y, "-k", label="test")

        # Set the limits of x-axis
        axes.set_xlim([datetime.datetime.fromisoformat('2022-01-01T12:00:00'),
                       datetime.datetime.fromisoformat('2022-01-15T21:00:00')])

        # Set the x-ticks interval
        axes.set_xticks(x[::2])

        for label in axes.get_xticklabels():
            label.set_rotation(90)

        canvas = FigureCanvas(figure)
        proxy_widget = self.dlg.scene.addWidget(canvas)
        self.dlg.plotView.setScene(self.dlg.scene)

        # self.dlg.plotView.fitInView(proxy_widget)
        self.dlg.plotView.show()

    def draw2(self):
        # Spaltennamen für die Messwerte
        messwert_spalten = ['A1(5)', 'A2(15)', 'A3(25)', 'A4(35)', 'A5(45)', 'A6(55)', 'A7(65)', 'A8(75)', 'A9(85)']
        # Beschriftungen für die Legende
        legende_beschriftungen = ['5-25 cm', '35-55 cm', '65-85 cm']
        data = np.random.rand(10, 9) * 100
        # Startdatum als numpy datetime64 Objekt
        start_date = np.datetime64('2022-01-01')

        # Erstellen Sie ein Array von aufeinanderfolgenden Tagen
        dates = np.arange(start_date, start_date + np.timedelta64(10, 'D'))

        # Mindest- und Maximalwerte über alle Daten ermitteln
        min_y = np.min(data)
        max_y = np.max(data)

        num_plots = data.shape[1] // 3
        fontsize = 20
        # Subplots erstellen
        fig, axs = plt.subplots(num_plots, 1, figsize=(15, 20), dpi=400, sharex=True)

        # Prüfen, ob nur eine Achse vorhanden ist, und in eine Liste umwandeln
        if num_plots == 1:
            axs = [axs]

        # Gemeinsame beschriftete X-Achse hinzufügen
        fig.text(0.5, 0.04, 'Datum', ha='center', va='center', fontsize=20)
        fig.text(0.06, 0.5, 'Bodenfeuchte (%)', ha='center', va='center', rotation='vertical', fontsize=fontsize)

        # Liniendiagramm für jeden Durchschnitt erstellen
        for i, (start_index, end_index) in enumerate([(0, 3), (3, 6), (6, 9)]):
            ax = axs[i]
            depths = data[:, start_index:end_index]
            avg_depth = np.mean(depths, axis=1)
            ax.plot(dates, avg_depth, linestyle='-', label=legende_beschriftungen[i])
            ax.legend(loc='upper left', fontsize=fontsize)
            ax.grid(True)
            ax.set_ylim(0, 100)
            ax.tick_params(axis='y', labelsize=fontsize)

        # X-Achse formatieren
        axs[-1].xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%Y'))
        axs[-1].tick_params(axis='x', rotation=45, labelsize=fontsize)

        canvas = FigureCanvas(fig)
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
