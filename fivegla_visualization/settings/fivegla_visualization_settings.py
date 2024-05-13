import json

from .fivegla_visualization_settings_dialog import FiveGLaVisualizationSettingsDialog
from ..constants import Constants
from ..database_manager import DatabaseConnection
from ..ui_elements import MessageBox


class FiveGLaVisualizationSettings:
    """ Creates, reads and updates the credentials to the database
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
        self.config_file = Constants.DATABASE_CREDENTIALS_FILE
        self.database_connection = DatabaseConnection()

    def run(self):
        """ Create the dialog with elements (after translation) and keep reference
        Only create GUI ONCE in callback, so that it will only load when the plugin is started

        :return: None
        """

        if self.first_start:
            self.callback_first_start()
            self.dlg = FiveGLaVisualizationSettingsDialog()
            self.dlg.btnSaveDbCredentials.clicked.connect(self.test_connection)
            self.first_start = False

        self.load_credentials()
        self.dlg.show()
        result = self.dlg.exec_()
        if result:
            pass

    def load_credentials(self):
        """ Loads the credentials from the config file and displays them in a QT Dialog

        :return: None
        """
        config = self.database_connection.get_config()
        self.dlg.textlineHost.setText(config['host'])
        self.dlg.textlineDatabase.setText(config['dbname'])
        self.dlg.textlineSchema.setText(config['schema'])
        self.dlg.textlinePort.setText(config['port'])
        self.dlg.textlineUsername.setText(config['user'])
        self.dlg.passwordline.setText(config['password'])

    def save_credentials(self):
        """ Updates the credentials

        :return: None
        """
        config = {"dbname": "{}".format(self.dlg.textlineDatabase.text()),
                  "user": "{}".format(self.dlg.textlineUsername.text()),
                  "password": "{}".format(self.dlg.passwordline.text()),
                  "host": "{}".format(self.dlg.textlineHost.text()),
                  "port": "{}".format(self.dlg.textlinePort.text()),
                  "schema": "{}".format(self.dlg.textlineSchema.text())
                  }
        with open(self.config_file, 'w') as json_file:
            json.dump(config, json_file, indent=4)

    def test_connection(self):
        """ Tests the Connection

        :return: None
        """
        self.save_credentials()
        msg_box = MessageBox()
        is_connected = self.database_connection.test_connection()
        msg_box.show_conditional_box(is_connected, "Connected to Database", "Error connecting to Database.")
