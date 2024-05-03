from qgis.core import QgsVectorLayer, QgsDataSourceUri, QgsProject
import json
import psycopg2
from ..custom_logger import CustomLogger

class DatabaseConnection:
    """ Creates a database connection to a PostGis Database
    """
    def __init__(self, config_file):
        self.config_file = config_file
        self.uri = None
        self.connection = None
        self.custom_logger = CustomLogger()

    def connect(self):
        """ Sets up a connection to the Databse
        :return: A boolean that indicates whether the database connection was successful
        """
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)

            connection = psycopg2.connect(
                host=config['host'],
                port=config['port'],
                dbname=config['dbname'],
                user=config['user'],
                password=config['password'])

            if connection:
                connection.close()
                self.custom_logger.log_info("Connection to database was successful.")
                return True
            else:
                connection.close()
                self.custom_logger.log_info("Connection to database was not successful!")
                return False

        except Exception as e:
            self.custom_logger.log_warning("An Exception trying to connect to the database.")
            return False

    def add_postgis_layer(self, table_name, geometry_column):
        """ Adds a PostGis Table as QGIS Layer to the MapCanvas

        :param table_name: The name of a PostGis Table
        :param geometry_column: The column which has the geometry information
        :return: A boolean that indicates whether the layer was added successful
        """
        if self.uri is None:
            self.connect()
        self.uri.setTable(table_name)
        self.uri.setGeometryColumn(geometry_column)
        layer = QgsVectorLayer(self.uri.uri(False), table_name, "postgres")
        if not layer.isValid():
            self.custom_logger.log_warning("Layer is invalid!")
            return False
        QgsProject.instance().addMapLayer(layer)
        self.custom_logger.log_warning("Layer added successfully!")
        return True
