from ..custom_logger import CustomLogger
from ..database_manager import DatabaseConnection


class SoilMoistureSensorGateway:
    def __init__(self, table_name):
        self.connection = DatabaseConnection()
        self.table_name = table_name
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

    def get_soil_moisture_measurements(self, entity_id, name_column_values, start_date, end_date):
        """ Returns an array of all measurements for a given entity id

        :param name_column_values: The Vales of the name column
        :param entity_id: The entity id
        :param start_date: The start date
        :param end_date: The end date
        :return: An array of all measurements for a given entity id or None if the connection is not established
        """
        if not self.connection.test_connection():
            self.custom_logger.log_warning("No connection to the database!")
            return None

        if entity_id is None or name_column_values is None:
            self.custom_logger.log_warning("Entity id or name column values not provided!")
            return None

        # log_warning if no valid date was selected

        if start_date is None or end_date is None:
            self.custom_logger.log_warning("No valid start-date and/or end-date was/were provided!")
            return None

        sql_select = "entityid, datecreated, name, controlledproperty"
        sql_order = "datecreated"
        sql_group = "entityid, datecreated, name, controlledproperty"
        measurements_dictionaries = []

        for name_column_value in name_column_values:
            sql_filter = ("entityid = '{}' and name = '{}' and controlledproperty > 0 and datecreated >= '{}' and "
                          "datecreated <= '{}' ").format(
                entity_id,
                name_column_value, start_date, end_date)
            measurement = self.connection.read_records(self.table_name, sql_select=sql_select,
                                                       sql_filter=sql_filter,
                                                       sql_order=sql_order, sql_group=sql_group)
            measurements_dictionaries.append(measurement)
        return measurements_dictionaries