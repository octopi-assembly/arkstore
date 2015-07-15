__author__ = 'rahul'

import os

from config import CURRENT_DIRECTORY

# File configurations
DB_HOST = "localhost"
DB_PORT = 5000
DB_USER = "root"
DB_PASSWORD = "root"
DB_DEFAULT = os.path.join("/", "var", "www", "mco", "sites", "default", "files")
DB_IGNORE = [".htaccess", "*.css", "*.js", "*.xml"]
DB_DUMP = 'rsync'

DB_LIST_LOAD_FROM_DB = True
DB_LIST_SOURCE_FILE = os.path.join(CURRENT_DIRECTORY, "backup", "{operation}_list.txt")
DB_DESTINATION_DIRECTORY = os.path.join(CURRENT_DIRECTORY, "backup", "rsync")


DB_TARGETS = [
    {
        'database': os.path.join("/", "var", "www", "mco", "sites", "default", "files"),
        'ignore': ["css", "ctools", "export", "js", "styles", "xmlsitemap"],
        'ignore_startswith': 'cache',
        'login':  'rahul',
        'password': 'rahul'
    }
]