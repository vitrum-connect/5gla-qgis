import json
import psycopg2
from ..custom_logger import CustomLogger
from ..constants import Constants
import os.path

class DatabaseConnection:
    """ Creates a database connection to a PostGis Database

    """

    def __init__(self):
        self.connection = None
        self.config_file = Constants.DATABASE_CREDENTIALS_FILE
        self.custom_logger = CustomLogger()
        if not os.path.exists(self.config_file):
            config = {"dbname": "",
                      "user": "",
                      "password": "",
                      "host": "",
                      "port": "",
                      "schema": ""}
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=4)
        with open(self.config_file, 'r') as f:
            config = json.load(f)
        self.config = config

    def __del__(self):
        self._close()

    def get_config(self):
        """ Gets the configuration from the config file or creates a new one

        :return: The configuration as a dictionary
        """
        with open(self.config_file, 'r') as f:
            self.config = json.load(f)
        return self.config

    def _create_connection(self):
        """ Creates a connection to the database

        :return: A boolean that indicates whether the database connection was successful
        """
        # noinspection PyBroadException
        try:
            self.get_config()
            self.connection = psycopg2.connect(
                host=self.config['host'],
                port=self.config['port'],
                dbname=self.config['dbname'],
                user=self.config['user'],
                password=self.config['password'])
            if self.connection:
                self.custom_logger.log_info("Connection to database was successful.")
                return True
            else:
                self.custom_logger.log_info("Connection to database was not successful!")
                return False
        except Exception as e:
            self.custom_logger.log_warning("An Exception trying to connect to the database.")
            return False

    def test_connection(self):
        """ Sets up a connection to the database

        :return: A boolean that indicates whether the database connection was successful
        """
        return self._create_connection()

    def _close(self):
        """ Closes the database connection

        :return:
        """
        if self.connection:
            self.connection.close()
            print("Database connection closed.")

    def read_records(self, table_name, sql_filter=None, sql_select=None, sql_order=None):
        """ Reads records from a table using a filter and a selection

        :param sql_select: Columns to select
        :param table_name: Name of table
        :param sql_filter: Filter selection
        :param sql_order: Order selection
        :return: A list of records or None
        """
        if self.connection is None:
            self._create_connection()
        try:
            if sql_select is not None:
                query = "SELECT {} ".format(sql_select)
            else:
                query = "SELECT * "

            query_table = "FROM {}.{} ".format(self.config["schema"], table_name)
            query += query_table
            if sql_filter is not None:
                query_filter = "WHERE {} ".format(sql_filter)
                query += query_filter

            if sql_order is not None:
                query_order = "ORDER BY {}".format(sql_order)
                query += query_order

            # Führe die SQL-Abfrage aus
            cursor = self.connection.cursor()
            cursor.execute(query)
            records_tuple = cursor.fetchall()
            records = [list(record) for record in records_tuple]
            cursor.close()
            return records

        except Exception as e:
            self.custom_logger.log_warning("Error reading from table '{}'".format(table_name))
            return None