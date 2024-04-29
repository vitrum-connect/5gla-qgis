from qgis.core import QgsVectorLayer, QgsDataSourceUri, QgsProject
import json
import psycopg2
from psycopg2 import OperationalError

class DatabaseConnection:
    def __init__(self, config_file):
        self.config_file = config_file
        self.uri = None
        self.connection = None

    def connect(self):
        try:
            # Lese die Verbindungsinformationen aus der JSON-Datei
            with open(self.config_file, 'r') as f:
                config = json.load(f)

                # Verbindung zur PostgreSQL-Datenbank herstellen
                connection = psycopg2.connect(
                    host=config['host'],
                    port=config['port'],
                    dbname=config['dbname'],
                    user=config['user'],
                    password=config['password'])

                # Überprüfen, ob die Verbindung erfolgreich ist
                if connection:
                    print("Verbindung zur PostgreSQL-Datenbank erfolgreich hergestellt.")
                    connection.close()  # Verbindung schließen
                    return True
                else:
                    print("Verbindung zur PostgreSQL-Datenbank fehlgeschlagen.")
                    return False

        except OperationalError as e:
            print(f"Fehler beim Verbinden zur PostgreSQL-Datenbank: {e}")
            return False


def close(self):
    if self.connection:
        self.connection.close()
        print("Database connection closed.")


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
