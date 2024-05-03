from .fivegla_visualization_settings_dialog import FiveGLaVisualizationSettingsDialog
from qgis.PyQt.QtWidgets import QMessageBox
import json
import os.path
from ..database_manager import DatabaseConnection
from ..constants import Constants


class FiveGLaVisualizationSettings:
    """ Creates,reads and updates the crendentials.json file
    """

    def __init__(self, iface, callbackFirstStart):
        """

        :param iface: A reference to the QGIS Interface
        :param callbackFirstStart: A callback to a method which must run before the first start
        """
        self.dlg = None
        self.iface = iface
        self.first_start = True
        self.callbackFirstStart = callbackFirstStart
        self.config_file = None

    def run(self):
        """ Create the dialog with elements (after translation) and keep reference
        Only create GUI ONCE in callback, so that it will only load when the plugin is started

        :return:
        """

        if self.first_start:
            self.callbackFirstStart()
            self.dlg = FiveGLaVisualizationSettingsDialog()
            self.dlg.btnSaveDbCredentials.clicked.connect(self.testConnection)
            self.first_start = False

        # show the dialog
        self.loadCredentials()
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            pass

    def loadCredentials(self):
        """ Loads the credentitals from the credentilas.json and displays them in a QT Dialog

        :return:
        """
        self.config_file = Constants.PLUGIN_DIR + "/database_manager/credentials.json"
        if not os.path.exists(self.config_file):
            config = {"dbname": "",
                      "user": "",
                      "password": "",
                      "host": "",
                      "port": "",
                      "schema": ""}
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=4)
        elif os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                config = json.load(f)
            self.dlg.textlineHost.setText(config['host'])
            self.dlg.textlineDatabase.setText(config['dbname'])
            self.dlg.textlineSchema.setText(config['schema'])
            self.dlg.textlinePort.setText(config['port'])
            self.dlg.textlineUsername.setText(config['user'])
            self.dlg.passwordline.setText(config['password'])

    def saveCredentials(self):
        """ Updates the credentials

        :return:
        """
        with open(self.config_file, 'r') as f:
            config = json.load(f)
        config['host'] = self.dlg.textlineHost.text()
        config['dbname'] = self.dlg.textlineDatabase.text()
        config['schema'] = self.dlg.textlineSchema.text()
        config['port'] = self.dlg.textlinePort.text()
        config['user'] = self.dlg.textlineUsername.text()
        config['password'] = self.dlg.passwordline.text()
        with open(self.config_file, 'w') as json_file:
            json.dump(config, json_file, indent=4)

    def testConnection(self):
        """ Tests the Connection

        :return:
        """
        self.saveCredentials()
        msg_box = QMessageBox()
        connection = DatabaseConnection(self.config_file)
        isConnected = connection.connect()

        if isConnected:
            msg = "Connected to Database"
            msg_box.setWindowTitle("Information")
            msg_box.setIcon(QMessageBox.Information)
        else:
            msg = "Error connecting to Database."
            msg_box.setWindowTitle("Error")
            msg_box.setIcon(QMessageBox.Critical)

        msg_box.setText(msg)
        ok_button = msg_box.addButton(QMessageBox.Ok)
        ok_button.setDefault(True)
        msg_box.exec_()
