__author__ = 'rahul'

import os

from config import CURRENT_DIRECTORY

# MySql configurations
FILE_HOST = "localhost"
FILE_PORT = 3306
FILE_USER = "root"
FILE_PASSWORD = "root"
FILE_DEFAULT = "files"
FILE_IGNORE = [".htaccess", "*.css", "*.js", "*.xml"]
FILE_DUMP = 'rsync -az'

FILE_LIST_LOAD_FROM_DB = True
FILE_LIST_SOURCE_FILE = os.path.join(CURRENT_DIRECTORY, "{operation}_list.txt")
FILE_DESTINATION_DIRECTORY = os.path.join(CURRENT_DIRECTORY, "backup", "files")


FILE_TARGETS = [
    {
        'database': os.path.join("/", "var", "www", "mco", "sites", "default", "files"),
        'ignore': ["css", "ctools", "export", "js", "styles", "xmlsitemap"],
        'ignore_startswith': 'cache',
        'login':  'rahul',
        'password': 'diamirza'
    }
]