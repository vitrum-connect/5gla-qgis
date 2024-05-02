# -*- coding: utf-8 -*-


import os

from qgis.PyQt import uic
from qgis.PyQt import QtWidgets

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'fivegla_visualization_settings_dialog_base.ui'))


class FiveGLaVisualizationSettingsDialog(QtWidgets.QDialog, FORM_CLASS):
    """
        Set up the user interface from Designer through FORM_CLASS.
    """
    def __init__(self, parent=None):
        super(FiveGLaVisualizationSettingsDialog, self).__init__(parent)
        self.setupUi(self)
