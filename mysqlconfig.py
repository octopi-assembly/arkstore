__author__ = 'rahul'

import os

from config import CURRENT_DIRECTORY

# MySql configurations
DB_HOST = "localhost"
DB_PORT = 3306
DB_USER = "root"
DB_PASSWORD = "root"
DB_DEFAULT_DB = "mco"
DB_IGNORE = ["information_schema", "performance_schema", "mysql"]
DB_DUMP = 'mysqldump'

DB_LIST_LOAD_FROM_DB = True
DB_LIST_SOURCE_FILE = os.path.join(CURRENT_DIRECTORY, "db_list.txt")
DB_DESTINATION_DIRECTORY = os.path.join(CURRENT_DIRECTORY, "backup", "rdb")


DB_TARGETS = [
    {
        'database': 'gogo',
        'ignore': ['cache'],
        'ignore_startswith': 'cache',
        'login':  'root',
        'password': 'root'
    },
    {
        'database': 'qpeka',
        'ignore': [],
        'ignore_startswith': 'cache',
        'login':  'root',
        'password': 'root'
    }
]