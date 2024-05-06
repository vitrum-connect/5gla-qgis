from ..database_manager import DatabaseConnection


class DevicePositionGateway:
    def __init__(self):
        self.connection = DatabaseConnection()
        self.table_name = "device_position"

    def _to_array(self, records):
        """ Converts a list of records to an array

        :param records: The list of records
        :return: An array of the first element of each record
        """
        return [record[0] for record in records]

    def get_device_ids(self):
        """ Returns an array of all device ids

        :return: An array of all device ids or None if the connection is not established
        """
        if not self.connection.test_connection():
            return None
        sql_select = "DISTINCT device_id"
        device_ids_list = self.connection.read_records(self.table_name, sql_select=sql_select)
        return self._to_array(device_ids_list)

    def get_transaction_ids(self, device_id):
        """ Returns an array of all transaction ids for a given device id

        :param device_id: The device id
        :return: An array of all transaction ids for a given device id or None if the connection is not established
        """
        if not self.connection.test_connection():
            return None
        sql_select = "DISTINCT transaction_id"
        sql_filter = "device_id = '{}'".format(device_id)
        transaction_ids_list = self.connection.read_records(self.table_name, sql_filter=sql_filter,
                                                            sql_select=sql_select)
        return self._to_array(transaction_ids_list)