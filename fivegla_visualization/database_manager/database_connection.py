from qgis.core import QgsVectorLayer, QgsDataSourceUri, QgsProject
import json
import psycopg2


class DatabaseConnection:
    def __init__(self, config_file):
        self.config_file = config_file
        self.uri = None
        self.connection = None

    def connect(self):
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
                return True
            else:
                return False

        except Exception as e:
            return False

    def addPostgisLayer(self, table_name, geometryColumn):
        if self.uri == None:
            self.connect()
        self.uri.setTable(table_name)
        self.uri.setGeometryColumn(geometryColumn)
        layer = QgsVectorLayer(self.uri.uri(False), table_name, "postgres")
        if not layer.isValid():
            print("Layer failed to load!")
            return
        QgsProject.instance().addMapLayer(layer)
        print("Layer added successfully!")
