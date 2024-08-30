import json
import os.path

import psycopg2

from ..constants import Constants
# from ..custom_logger import CustomLogger

import logging
import logging.config


class DatabaseConnection:
    """ Creates a database connection to a PostGis Database

    """

    def __init__(self):
        self.connection = None
        self.config_file = Constants.DATABASE_CREDENTIALS_FILE
        logging.config.fileConfig('logging.conf')
        self.logger = logging.getLogger('app')

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

    @staticmethod
    def extract_values(records, key):
        """ Extracts values for a specific key from a list of dictionaries

        :param records: The list of dictionaries
        :param key: The key to extract values for
        :return: A list of values for the specified key
        """
        if records is None:
            return None
        if len(records) == 0:
            return None
        return [record[key] for record in records]

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
                self.logger.info('Connection to database was successful.')
                return True
            else:
                self.logger.info('Connection to database was not successful!')
                return False
        except Exception as e:
            self.logger.warning('An exception occurred trying to connect to the database: {}".format(e)')
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

    def read_records(self, table_name, sql_filter=None, sql_select=None, sql_order=None, sql_group=None):
        """ Reads records from a table using a filter and a selection

        :param sql_select: Columns to select
        :param table_name: Name of table
        :param sql_filter: Filter selection
        :param sql_order: Order selection
        :param sql_group: Group selection
        :return: A list of dictionaries with the records or None if the connection is not established
        """
        if self.connection is None:
            self._create_connection()
        if table_name is None or table_name == "":
            self.logger.warning('Table name is not provided.')
            return None
        # noinspection PyBroadException
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

            if sql_group is not None:
                query_group = "GROUP BY {} ".format(sql_group)
                query += query_group

            if sql_order is not None:
                query_order = "ORDER BY {} ".format(sql_order)
                query += query_order

            # execute SQL query
            cursor = self.connection.cursor()
            self.logger.debug(query)

            cursor.execute(query)

            column_names = [desc[0] for desc in cursor.description]
            records = [dict(zip(column_names, record)) for record in cursor.fetchall()]
            cursor.close()
            return records

        except Exception as e:
            self.logger.warning("An exception occurred trying to read from the table '{}': {}".format(table_name, e))
            return None
