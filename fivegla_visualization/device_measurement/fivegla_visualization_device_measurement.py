from datetime import date, timedelta
import json
import os

# provisional logging changes
import logging
import logging.config

from PyQt5.QtCore import QDate, QTime, QDateTime
from PyQt5.QtWidgets import QPushButton, QGraphicsScene, QGraphicsView, QDateEdit
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from .fivegla_visualization_device_measurement_dialog import FiveGLaVisualizationDeviceMeasurementDialog
from ..constants import Constants
from ..database_manager import SoilMoistureSensorGateway
from ..layer_manager import LayerManager
from ..ui_elements import MessageBox, UiHelper, SoilMoistureFigure


def load_config():
    current_dir = os.path.dirname(__file__)
    config_path = os.path.join(current_dir, '..', 'config.json')
    with open(config_path) as config_file:
        config = json.load(config_file)

    return config


class FiveGLaVisualizationDeviceMeasurement:
    """This class enables the user to visualize the device measurements on the graph
    """

    def __init__(self, iface, callback_first_start):
        self.dlg = None
        self.first_start = True
        self.iface = iface
        self.callback_first_start = callback_first_start
        self.agvolution_sensor_gateway = SoilMoistureSensorGateway(Constants.AGVOLUTION_SENSOR_TABLE_NAME)
        self.sentek_sensor_gateway = SoilMoistureSensorGateway(Constants.SENTEK_SENSOR_TABLE_NAME)
        self.layer_manager = LayerManager(self.iface)
        logging.config.fileConfig('logging.conf')
        self.logger = logging.getLogger('app')

    def run(self):
        """ Create the dialog with elements (after translation) and keep reference
        Only create GUI ONCE, so that it will only be created when the plugin is started

        :return: None
        """

        if self.first_start:
            self.callback_first_start()
            self.dlg = FiveGLaVisualizationDeviceMeasurementDialog()
            self.dlg.btnDraw = self.dlg.findChild(QPushButton, "btnDraw")
            self.dlg.btnClear = self.dlg.findChild(QPushButton, "btnClear")
            self.dlg.plotView = self.dlg.findChild(QGraphicsView, "plotView")

            # initialization dialog boxes for start-/end-date
            self.dlg.dateEditStart = self.dlg.findChild(QDateEdit, "dateEditStart")
            self.dlg.dateEditEnd = self.dlg.findChild(QDateEdit, "dateEditEnd")

            # determine the current month, year and last day of month
            config = load_config()
            previous_period = config['previous_days_from_today']
            two_weeks_ago = date.today() - timedelta(days=previous_period)
            starting_day = two_weeks_ago.day
            starting_month = two_weeks_ago.month
            starting_year = two_weeks_ago.year

            # set default values for date-dialog-boxes
            default_start_date = QDate(starting_year, starting_month, starting_day)
            default_end_date = QDate(QDate.currentDate())
            self.dlg.dateEditStart.setDate(default_start_date)
            self.dlg.dateEditEnd.setDate(default_end_date)

            self.dlg.btnDraw.clicked.connect(self.draw)
            self.dlg.btnClear.clicked.connect(self.clear)
            self.first_start = False
            self.dlg.scene = QGraphicsScene()

        # Ensures the Sensor Table is added to the QGIS project as a layer
        layer = self.layer_manager.select_layer_from_qgis_project(Constants.SENTEK_SENSOR_TABLE_NAME)
        if not layer:
            if not self.layer_manager.add_layer(Constants.SENTEK_SENSOR_TABLE_NAME, 'location'):
                self.logger.warning("Layer could not be added!")
                MessageBox.show_error_box("Layer could not be added!")
                return None
            self.logger.info("Layer was added successfully!")
        self.fill_combo_box_entity_ids()
        self.dlg.show()
        result = self.dlg.exec_()
        self.clear()
        if result:
            pass

    def fill_combo_box_entity_ids(self):
        """Fills the combo box with the entity ids

        :return: None
        """
        sentek_entity_ids = self.sentek_sensor_gateway.get_entity_ids()
        agvolution_entity_ids = self.agvolution_sensor_gateway.get_entity_ids()
        if sentek_entity_ids is None and agvolution_entity_ids is None:
            MessageBox.show_error_box("No connection to the database, the table does not exist or is empty!")
            return
        entity_ids = sentek_entity_ids + agvolution_entity_ids
        UiHelper.combo_box_filler(entity_ids, self.dlg.cmbEntityId)

    def convert_date_to_str(self):
        """Convert date_time_objects into date-strings

        :return: start- and end-date strings
        """

        start_date = self.dlg.dateEditStart.date()
        end_date = self.dlg.dateEditEnd.date()

        start_date_time = QDateTime(start_date, QTime(0, 0, 0, 0))
        end_date_time = QDateTime(end_date, QTime(23, 59, 59, 999))
        start_date_formatted = start_date_time.toString("yyyy-MM-ddTHH:mm:ss.zzzZ")
        end_date_formatted = end_date_time.toString("yyyy-MM-ddTHH:mm:ss.zzzZ")

        return start_date_formatted, end_date_formatted

    def draw(self):
        """Draws the soil moisture measurements as figure on the canvas

        :return: None
        """
        selected_entity_id = self.dlg.cmbEntityId.currentText()

        # call method to provide string formatted date
        start_date, end_date = self.convert_date_to_str()

        if start_date > end_date:
            MessageBox.show_error_box("No valid date range!")
            return

        measurements = []
        names_for_plot = []
        group_size = 1
        is_sentek_sensor = False
        is_agvolution_sensor = False
        sentek_entity_ids = self.sentek_sensor_gateway.get_entity_ids()
        agvolution_entity_ids = self.agvolution_sensor_gateway.get_entity_ids()
        if selected_entity_id in sentek_entity_ids and selected_entity_id in agvolution_entity_ids:
            self.logger.info("The selected entity id is in both manufacture Tables and therefore not unique")
            MessageBox.show_info_box("The selected entity id is in both manufacture Tables and therefore not unique")
            return None
        if selected_entity_id in sentek_entity_ids:
            is_sentek_sensor = True
        elif selected_entity_id in agvolution_entity_ids:
            is_agvolution_sensor = True
        if is_sentek_sensor:
            names_for_plot = ["A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9"]
            measurements = self.sentek_sensor_gateway.get_soil_moisture_measurements(selected_entity_id, names_for_plot,
                                                                                     start_date, end_date)
            group_size = 3
        if is_agvolution_sensor:
            names_for_plot = ["-10|ENV__SOIL__VWC", "-30|ENV__SOIL__VWC", "-45|ENV__SOIL__VWC"]
            measurements = self.agvolution_sensor_gateway.get_soil_moisture_measurements(selected_entity_id,
                                                                                         names_for_plot, start_date,
                                                                                         end_date)
            group_size = 3
        if not all(measurement for measurement in measurements):
            self.logger.info("No measurements for the selected entity id!")
            MessageBox.show_info_box("No measurements for the selected entity id!")
            return
        figure = SoilMoistureFigure.create_figure(values=measurements, labels=names_for_plot, group_size=group_size)
        if figure is None:
            self.logger.warning("The figure could not be created!")
            MessageBox.show_error_box("The figure could not be created!")
            return
        canvas = FigureCanvas(figure)
        proxy_widget = self.dlg.scene.addWidget(canvas)
        self.dlg.plotView.setScene(self.dlg.scene)
        self.dlg.plotView.fitInView(proxy_widget)
        self.dlg.plotView.show()
        return

    def clear(self):
        """Clears the graph

        :return: None
        """
        self.dlg.scene.clear()
        self.dlg.plotView.setScene(self.dlg.scene)
        self.dlg.plotView.show()
