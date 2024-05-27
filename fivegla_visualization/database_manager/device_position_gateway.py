from ..constants import Constants
from ..custom_logger import CustomLogger
from ..database_manager import DatabaseConnection


class DevicePositionGateway:
    def __init__(self):
        self.connection = DatabaseConnection()
        self.table_name = Constants.DEVICE_POSITION_TABLE_NAME
        self.custom_logger = CustomLogger()

    def get_device_ids(self):
        """ Returns an array of all device ids

        :return: An array of all device ids or None if the connection is not established
        """
        if not self.connection.test_connection():
            self.custom_logger.log_warning("No connection to the database!")
            return None
        sql_select = "DISTINCT deviceid"
        sql_order = "deviceid"
        device_ids_dictionary = self.connection.read_records(self.table_name, sql_select=sql_select,
                                                             sql_order=sql_order)
        device_ids_array = self.connection.extract_values(device_ids_dictionary, "deviceid")
        return device_ids_array

    def get_transaction_ids(self, device_id):
        """ Returns an array of all transaction ids for a given device id

        :param device_id: The device id
        :return: An array of all transaction ids for a given device id or None if the connection is not established
        """
        if not self.connection.test_connection():
            self.custom_logger.log_warning("No connection to the database!")
            return None
        if device_id is None:
            self.custom_logger.log_warning("No device id provided!")
            return None
        sql_select = "DISTINCT transactionid"
        sql_filter = "deviceid = '{}'".format(device_id)
        sql_order = "transactionid"
        transaction_ids_dict = self.connection.read_records(self.table_name, sql_filter=sql_filter,
                                                            sql_select=sql_select, sql_order=sql_order)
        transaction_ids = self.connection.extract_values(transaction_ids_dict, "transactionid")
        return transaction_ids

    def get_latest_device_position(self, device_id, transaction_id):
        """ Returns the latest device position for a given device id and transaction id

        :param device_id: The device id
        :param transaction_id: The transaction id
        :return: The entitityid of the latest device position for a given device id and transaction id or
            None if the connection is not established
        """
        if not self.connection.test_connection():
            self.custom_logger.log_warning("No connection to the database!")
            return None
        if device_id is None or transaction_id is None:
            self.custom_logger.log_warning("No device id or transaction id provided!")
            return None
        sql_select = "entityid"
        sql_filter = "deviceid = '{}' AND transactionid = '{}'".format(device_id, transaction_id)
        sql_order = "datecreated DESC LIMIT 1"
        entity_id_dict = self.connection.read_records(self.table_name, sql_filter=sql_filter,
                                                      sql_select=sql_select,
                                                      sql_order=sql_order)
        entity_ids = self.connection.extract_values(entity_id_dict, "entityid")
        if entity_ids is None:
            self.custom_logger.log_info("No Entity ID found for the given device id and transaction id!")
            return None
        entity_id_latest_position = entity_ids[0]
        return entity_id_latest_position
