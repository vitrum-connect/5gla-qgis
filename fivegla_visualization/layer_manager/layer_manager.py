from qgis.core import QgsVectorLayer, QgsDataSourceUri, QgsProject
from qgis.gui import QgsLayerTreeView
from fivegla_visualization.custom_logger import CustomLogger
from fivegla_visualization.database_manager import DatabaseConnection


class LayerManager:
    def __init__(self, iface):
        self.custom_logger = CustomLogger()
        config = DatabaseConnection().get_config()
        self.uri = QgsDataSourceUri()
        self.schema = config['schema']
        self.uri.setConnection(config['host'],
                               config['port'],
                               config['dbname'],
                               config['user'],
                               config['password'])
        self.iface = iface

    def select_layer(self, table_name, geometry_column):
        """ Selects a PostGis Table as QGIS Layer to the MapCanvas

        :param table_name: The name of a PostGis Table
        :param geometry_column: The column which has the geometry information
        :return: A boolean that indicates whether the layer was selected successful
        """
        self.uri.setTable(table_name)
        self.uri.setGeometryColumn(geometry_column)
        self.uri.setSchema(self.schema)
        layer = QgsVectorLayer(self.uri.uri(False), table_name, "postgres")
        if not layer.isValid():
            self.custom_logger.log_warning("Layer is invalid!")
            return None
        return layer

    def add_layer(self, table_name, geometry_column):
        """ Adds a PostGis Table as QGIS Layer to the MapCanvas

        :param table_name: The name of a PostGis Table
        :param geometry_column: The column with the geometry information
        :return: A boolean that indicates whether the layer was added successful
        """
        selected_layer = self.select_layer(table_name, geometry_column)
        if selected_layer is None:
            return False
        QgsProject.instance().addMapLayer(selected_layer)
        return True

    def add_feature(self, layer, feature):
        """ Adds a feature to a layer

        :param layer: The layer to add the feature to
        :param feature: The feature to add
        :return: A boolean that indicates whether the feature was added successful
        """
        if layer is None:
            self.custom_logger.log_warning("Layer is invalid!")
            return False
        if feature is None:
            self.custom_logger.log_warning("Feature is None!")
            return False
        layer.startEditing()
        layer.addFeature(feature)
        layer.commitChanges()
        return True

    def select_feature(self, table_name, geometry_column, entity_id):
        """ Selects a Feature from the Layer

        :param table_name: The name of a PostGis Table
        :param geometry_column: The column which has the geometry information
        :param entity_id: The id of the entity
        :return: A boolean that indicates whether the layer was selected successful
        """
        layer = self.select_layer(table_name, geometry_column)
        if layer is None:
            self.custom_logger.log_warning("Layer is None!")
            return None
        feature = layer.getFeature(entity_id)
        return feature

    def add_device_position_layer(self):
        """ Adds the device position layer to the map canvas

        :return: A boolean that indicates whether the layer was added successful
        """
        return self.add_layer("device_position", "location")

    @staticmethod
    def create_copy_of_layer(source_layer, layer_name):
        """ Creates an empty copy of a layer

        :param source_layer: The source layer
        :param layer_name: The name of the target layer
        :return: The target layer with the structure of the source layer or None if the source layer is invalid
        """
        if source_layer is None:
            return None
        if not source_layer.isValid():
            return None
        target_layer = QgsVectorLayer("Point?crs=epsg:4326", layer_name, "memory")
        target_layer.startEditing()
        target_layer.dataProvider().addAttributes(source_layer.fields())
        target_layer.updateFields()
        return target_layer

    def clear_layer(self, layer):
        """ Clears a layer

        :param layer: The layer to clear
        :return: A boolean that indicates whether the layer was cleared successful
        """
        if layer is None:
            # Logging
            self.custom_logger.log_warning("Layer is None!")
            return False
        if not layer.isValid():
            # Logging
            self.custom_logger.log_warning("Layer is invalid!")
            return False
        layer.startEditing()
        layer.dataProvider().truncate()
        layer.commitChanges()
        return True

    def show_device_position(self, entity_id):
        """ Adds the current drone position to the map canvas

        :return: A boolean that indicates whether the layer was added successful
        """
        memory_layer_name = "Latest Device Position"
        latest_device_position_layer = self.select_layer_from_qgis_project(memory_layer_name)
        if latest_device_position_layer is not None:
            self.clear_layer(latest_device_position_layer)

        if latest_device_position_layer is None:
            device_position_layer = self.select_layer("device_position", "location")
            latest_device_position_layer = self.create_copy_of_layer(device_position_layer, memory_layer_name)

        feature = self.select_feature("device_position", "location", entity_id)
        if feature is None:
            # Logging
            self.custom_logger.log_warning("There is no feature with the given entity id!")
            return False
        self.add_feature(latest_device_position_layer, feature)
        QgsProject.instance().addMapLayer(latest_device_position_layer)
        return True

    def select_layer_from_qgis_project(self, layer_name):
        """ Selects a layer from the QGS Project

        :param layer_name: The name of the layer
        :return: The layer or None if the layer was not found
        """
        project = QgsProject.instance()
        layer_result_list = project.mapLayersByName(layer_name)
        if len(layer_result_list) == 0:
            return None
        return layer_result_list[0]
