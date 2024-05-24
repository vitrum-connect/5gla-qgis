from ..custom_logger import CustomLogger
from ..constants import Constants
from ..database_manager import DatabaseConnection


class SentekSensorGateway:
    def __init__(self):
        self.connection = DatabaseConnection()
        self.table_name = Constants.SENTEK_SENSOR_TABLE_NAME
        self.custom_logger = CustomLogger()

    def get_entity_ids(self):
        """ Returns an array of all entity ids

        :return: An array of all entity ids or None if the connection is not established
        """
        if not self.connection.test_connection():
            self.custom_logger.log_warning("No connection to the database!")
            return None
        sql_select = "DISTINCT entityid"
        sql_order = "entityid"
        entity_ids_dict = self.connection.read_records(self.table_name, sql_select=sql_select,
                                                       sql_order=sql_order)
        entity_ids = self.connection.extract_values(entity_ids_dict, "entityid")
        return entity_ids

    def get_soil_moisture_measurements(self, entity_id, name_column_values):
        """ Returns an array of all measurement for a given entity id

        :param name_column_values: The Vales of the name column
        :param entity_id: The entity id
        :return: An array of all measurement for a given entity id or None if the connection is not established
        """
        if not self.connection.test_connection():
            self.custom_logger.log_warning("No connection to the database!")
            return None

        sql_select = "entityid, datecreated, name, controlledproperty"
        sql_order = ("datecreated")
        sql_group = "entityid, datecreated, name, controlledproperty"
        measurements_dictionarys = []

        for name_column_value in name_column_values:
            sql_filter = "entityid = '{}' and name = '{}' and controlledproperty > 0".format(entity_id,
                                                                                                name_column_value)
            measurement = self.connection.read_records(self.table_name, sql_select=sql_select,
                                                       sql_filter=sql_filter,
                                                       sql_order=sql_order, sql_group=sql_group)
            measurements_dictionarys.append(measurement)
        return measurements_dictionarys
