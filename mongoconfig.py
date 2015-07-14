__author__ = 'rahul'

import os

from config import CURRENT_DIRECTORY

# Mongo configurations
DB_HOST = "localhost"
DB_PORT = 27017
DB_USER = "root"
DB_PASSWORD = "root"
DB_DEFAULT_DB = "mco"
DB_IGNORE = ["local", "test"]
DB_DUMP = 'mongodump'

DB_LIST_LOAD_FROM_DB = True
DB_LIST_SOURCE_FILE = os.path.join(CURRENT_DIRECTORY, "db_list.txt")
DB_DESTINATION_DIRECTORY = os.path.join(CURRENT_DIRECTORY, "backup", "ndb")

DB_TARGETS = [
    {
        'database': 'mco',
        'ignore': ['fs.chunks'],
        'ignore_startswith': 'system.',
        'login':  'root',
        'password': 'root'
    },
    {
        'database': 'qpekalibrary',
        'ignore': [],
        'ignore_startswith': 'system.',
        'login':  'root',
        'password': 'root'
    }
]