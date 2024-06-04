import os

from qgis.PyQt import QtWidgets
from qgis.PyQt import uic
from qgis.PyQt.QtCore import Qt

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'fivegla_visualization_device_position_dialog_base.ui'))


class FiveGLaVisualizationDevicePositionDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None, flags=Qt.Dialog | Qt.WindowStaysOnTopHint):
        """Constructor."""
        super(FiveGLaVisualizationDevicePositionDialog, self).__init__(parent, flags)
        # Set up the user interface from Designer through FORM_CLASS.
        # After self.setupUi() you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
