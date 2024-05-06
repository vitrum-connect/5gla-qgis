from fivegla_visualization.custom_logger import CustomLogger
from qgis.core import QgsVectorLayer, QgsDataSourceUri, QgsProject

from fivegla_visualization.database_manager import DatabaseConnection


class LayerManager:
    def __init__(self):
        self.custom_logger = CustomLogger()
        self.layer = None
        config = DatabaseConnection().get_config()
        self.uri = QgsDataSourceUri()
        self.uri.setConnection(config['host'],
                               config['port'],
                               config['dbname'],
                               config['user'],
                               config['password'])

    def add_postgis_layer(self, table_name, geometry_column):
        """ Adds a PostGis Table as QGIS Layer to the MapCanvas

        :param table_name: The name of a PostGis Table
        :param geometry_column: The column which has the geometry information
        :return: A boolean that indicates whether the layer was added successful
        """
        self.uri.setTable(table_name)
        self.uri.setGeometryColumn(geometry_column)
        layer = QgsVectorLayer(self.uri.uri(False), table_name, "postgres")
        if not layer.isValid():
            self.custom_logger.log_warning("Layer is invalid!")
            return False
        QgsProject.instance().addMapLayer(layer)
        self.custom_logger.log_warning("Layer added successfully!")
        return True
