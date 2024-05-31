import os.path

class Constants:
    PLUGIN_DIR = os.path.dirname(__file__)
    LOG_DIR = PLUGIN_DIR + "/logs"
    DATABASE_CREDENTIALS_FILE = PLUGIN_DIR + "/database_manager/credentials.json"
    SENTEK_SENSOR_TABLE_NAME = "senteksensor"
    DEVICE_POSITION_TABLE_NAME = "deviceposition"




