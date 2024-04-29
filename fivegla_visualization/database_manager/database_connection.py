from qgis.core import QgsVectorLayer, QgsDataSourceUri, QgsProject
import json
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

            # Konstruiere die URI für die Verbindung
            self.uri = QgsDataSourceUri()
            self.uri.setConnection(config['host'], str(config['port']), config['dbname'], config['user'],
                                   config['password'])

            # Verbindung zur Datenbank herstellen
            self.connection = self.uri.connectionInfo()

            print("Verbindung zur Datenbank hergestellt.")

        except Exception as e:
            print("Fehler beim Verbindungsaufbau zur Datenbank:", e)

    def close(self):
        if self.connection:
            self.connection.close()
            print("Datenbankverbindung geschlossen.")

    def create_record(self, table_name, data):
        if self.connection:
            try:
                # Erstelle die SQL-Abfrage für das Einfügen eines Datensatzes
                fields = ', '.join(data.keys())
                values = ', '.join(["'{}'".format(val) for val in data.values()])
                query = "INSERT INTO {} ({}) VALUES ({});".format(table_name, fields, values)

                # Führe die SQL-Abfrage aus
                cursor = self.connection.cursor()
                cursor.execute(query)
                self.connection.commit()
                cursor.close()
                print("Datensatz erfolgreich erstellt.")

            except Exception as e:
                print("Fehler beim Erstellen des Datensatzes:", e)

        else:
            print("Keine Verbindung zur Datenbank.")

    def read_records(self, table_name):
        if self.connection:
            try:
                # Erstelle die SQL-Abfrage für das Lesen aller Datensätze aus der Tabelle
                query = "SELECT * FROM {};".format(table_name)

                # Führe die SQL-Abfrage aus
                cursor = self.connection.cursor()
                cursor.execute(query)
                records = cursor.fetchall()
                cursor.close()
                return records

            except Exception as e:
                print("Fehler beim Lesen der Datensätze:", e)

        else:
            print("Keine Verbindung zur Datenbank.")

    def update_record(self, table_name, record_id, data):
        if self.connection:
            try:
                # Erstelle die SQL-Abfrage für das Aktualisieren eines Datensatzes
                set_clause = ', '.join(["{} = '{}'".format(key, value) for key, value in data.items()])
                query = "UPDATE {} SET {} WHERE id = {};".format(table_name, set_clause, record_id)

                # Führe die SQL-Abfrage aus
                cursor = self.connection.cursor()
                cursor.execute(query)
                self.connection.commit()
                cursor.close()
                print("Datensatz erfolgreich aktualisiert.")

            except Exception as e:
                print("Fehler beim Aktualisieren des Datensatzes:", e)

        else:
            print("Keine Verbindung zur Datenbank.")

    def delete_record(self, table_name, record_id):
        if self.connection:
            try:
                # Erstelle die SQL-Abfrage für das Löschen eines Datensatzes
                query = "DELETE FROM {} WHERE id = {};".format(table_name, record_id)

                # Führe die SQL-Abfrage aus
                cursor = self.connection.cursor()
                cursor.execute(query)
                self.connection.commit()
                cursor.close()
                print("Datensatz erfolgreich gelöscht.")

            except Exception as e:
                print("Fehler beim Löschen des Datensatzes:", e)

        else:
            print("Keine Verbindung zur Datenbank.")