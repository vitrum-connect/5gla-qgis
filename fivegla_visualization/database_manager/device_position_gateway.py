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
        if records is None:
            return None
        if len(records) == 0:
            return None
        return [record[0] for record in records]

    def get_device_ids(self):
        """ Returns an array of all device ids

        :return: An array of all device ids or None if the connection is not established
        """
        if not self.connection.test_connection():
            return None
        sql_select = "DISTINCT deviceid"
        sql_order = "deviceid"
        device_ids_list = self.connection.read_records(self.table_name, sql_select=sql_select, sql_order=sql_order)
        return self._to_array(device_ids_list)

    def get_transaction_ids(self, device_id):
        """ Returns an array of all transaction ids for a given device id

        :param device_id: The device id
        :return: An array of all transaction ids for a given device id or None if the connection is not established
        """
        if not self.connection.test_connection():
            return None
        sql_select = "DISTINCT transactionid"
        sql_filter = "deviceid = '{}'".format(device_id)
        sql_order = "transactionid"
        transaction_ids_list = self.connection.read_records(self.table_name, sql_filter=sql_filter,
                                                            sql_select=sql_select, sql_order=sql_order)

        return self._to_array(transaction_ids_list)

    def get_latest_device_position(self, device_id, transaction_id):
        """ Returns the latest device position for a given device id and transaction id

        :param device_id: The device id
        :param transaction_id: The transaction id
        :return: The latest device position for a given device id and transaction id or None if the connection is not established
        """
        if not self.connection.test_connection():
            return None
        sql_select = "entityid"
        sql_filter = "deviceid = '{}' AND transactionid = '{}'".format(device_id, transaction_id)
        sql_order = "recvtime DESC LIMIT 1"
        entity_id_list = self.connection.read_records(self.table_name, sql_filter=sql_filter, sql_select=sql_select,
                                                      sql_order=sql_order)
        entity_id = self._to_array(entity_id_list)
        if entity_id is None:
            return None
        return entity_id[0]
