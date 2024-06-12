from PyQt5.QtWidgets import QPushButton, QGraphicsScene, QGraphicsView
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from .fivegla_visualization_device_measurement_dialog import FiveGLaVisualizationDeviceMeasurementDialog
from ..constants import Constants
from ..custom_logger import CustomLogger
from ..database_manager import SoilMoistureSensorGateway
from ..layer_manager import LayerManager
from ..ui_elements import MessageBox, UiHelper, SoilMoistureFigure


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
        self.custom_logger = CustomLogger()

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
            self.dlg.btnDraw.clicked.connect(self.draw)
            self.dlg.btnClear.clicked.connect(self.clear)
            self.first_start = False
            self.dlg.scene = QGraphicsScene()

        # Ensures the Sensor Table is added to the QGIS project as a layer
        layer = self.layer_manager.select_layer_from_qgis_project(Constants.SENTEK_SENSOR_TABLE_NAME)
        if not layer:
            if not self.layer_manager.add_layer(Constants.SENTEK_SENSOR_TABLE_NAME, 'location'):
                self.custom_logger.log_warning("Layer could not be added!")
                MessageBox.show_error_box("Layer could not be added!")
                return None
            self.custom_logger.log_info("Layer was added successfully!")

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

    def draw(self):
        """Draws the soil moisture measurements as figure on the canvas

        :return: None
        """
        selected_entity_id = self.dlg.cmbEntityId.currentText()
        measurements = []
        names_for_plot = []
        group_size = 1
        is_sentek_sensor = False
        is_agvolution_sensor = False
        sentek_entity_ids = self.sentek_sensor_gateway.get_entity_ids()
        agvolution_entity_ids = self.agvolution_sensor_gateway.get_entity_ids()
        if selected_entity_id in sentek_entity_ids and selected_entity_id in agvolution_entity_ids:
            self.custom_logger.log_info("The selected entity id is in both manufacture Tables and therefore not unique")
            MessageBox.show_info_box("The selected entity id is in both manufacture Tables and therefore not unique")
            return None
        if selected_entity_id in sentek_entity_ids:
            is_sentek_sensor = True
        elif selected_entity_id in agvolution_entity_ids:
            is_agvolution_sensor = True
        if is_sentek_sensor:
            names_for_plot = ["A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9"]
            measurements = self.sentek_sensor_gateway.get_soil_moisture_measurements(selected_entity_id, names_for_plot)
            group_size = 3
        if is_agvolution_sensor:
            names_for_plot = ["-10|ENV__SOIL__VWC", "-30|ENV__SOIL__VWC", "-45|ENV__SOIL__VWC"]
            measurements = self.agvolution_sensor_gateway.get_soil_moisture_measurements(selected_entity_id,
                                                                                         names_for_plot)
            group_size = 3
        if not all(measurement for measurement in measurements):
            self.custom_logger.log_info("No measurements for the selected entity id!")
            MessageBox.show_info_box("No measurements for the selected entity id!")
            return
        figure = SoilMoistureFigure.create_figure(values=measurements, labels=names_for_plot, group_size=group_size)
        if figure is None:
            self.custom_logger.log_warning("The figure could not be created!")
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
