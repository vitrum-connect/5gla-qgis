from qgis.PyQt.QtWidgets import QPushButton

from .fivegla_visualization_device_position_dialog import FiveGLaVisualizationDevicePositionDialog
from ..database_manager import DevicePositionGateway
from ..layer_manager import LayerManager
from ..ui_elements import MessageBox
from ..ui_elements import UiHelper


class FiveGLaVisualizationDevicePosition:
    """This class enables the user to visualize the device position on the map
    """

    def __init__(self, iface, callback_first_start):
        """

        :param iface: A reference to the QGIS Interface
        :param callback_first_start: A callback to a method which must run before the first start
        """
        self.dlg = None
        self.iface = iface
        self.first_start = True
        self.layer_manager = LayerManager(self.iface)
        self.callback_first_start = callback_first_start

    def run(self):
        """ Create the dialog with elements (after translation) and keep reference
        Only create GUI ONCE in callback, so that it will only load when the plugin is started

        :return: None
        """

        if self.first_start:
            self.callback_first_start()
            self.dlg = FiveGLaVisualizationDevicePositionDialog()
            self.dlg.btnDatabaseTest = self.dlg.findChild(QPushButton, "btnShowDevicePosition")
            self.dlg.btnDatabaseTest.clicked.connect(self.show_device_position)
            self.dlg.cmbDeviceId.currentIndexChanged.connect(self.fill_combo_box_transaction_ids)
            self.first_start = False

        self.fill_combo_box_device_ids()
        self.dlg.show()
        result = self.dlg.exec_()
        self.clear_form()
        if result:
            pass

    def fill_combo_box_device_ids(self):
        """Fills the combo box with the device ids

        :return: None
        """
        device_position_gateway = DevicePositionGateway()
        device_ids = device_position_gateway.get_device_ids()

        if device_ids is None:
            MessageBox.show_error_box("No connection to the database, the table does not exist or is empty!")
            return

        UiHelper.combo_box_filler(device_ids, self.dlg.cmbDeviceId)

    def fill_combo_box_transaction_ids(self):
        """Fills the combo box with the transaction ids

        :return: None
        """
        device_position_gateway = DevicePositionGateway()
        transaction_ids = device_position_gateway.get_transaction_ids(self.dlg.cmbDeviceId.currentText())

        if transaction_ids is None:
            MessageBox.show_error_box("No connection to the database, the table does not exist or is empty!")
            return

        UiHelper.combo_box_filler(transaction_ids, self.dlg.cmbTransactionId)
        self.dlg.btnShowDevicePosition.setEnabled(
            self.dlg.cmbTransactionId.count() > 0 and self.dlg.cmbDeviceId.count() > 0)

    def clear_form(self):
        """Clears the form

        :return: None
        """
        self.dlg.cmbDeviceId.clear()
        self.dlg.cmbTransactionId.clear()
        self.dlg.btnShowDevicePosition.setEnabled(False)

    def show_device_position(self):
        """Shows the device position on the map

        :return: None
        """
        device_position_gateway = DevicePositionGateway()
        entity_id = device_position_gateway.get_latest_device_position(self.dlg.cmbDeviceId.currentText(),
                                                                       self.dlg.cmbTransactionId.currentText())
        if entity_id is None:
            MessageBox.show_error_box("No connection to the database!")
            return
        entity_exists = self.layer_manager.show_device_position(entity_id)
        if not entity_exists:
            MessageBox.show_error_box("The entity does not exist!")
            return
