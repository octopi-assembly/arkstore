__author__ = 'rahul'

import config as settings


DB_TARGETS = [
    {
        'database': 'mco',
        'ignore': ['fs.chunks'],
        'login':  settings.NDB_USER,
        'password': settings.NDB_PASSWORD
    },
    {
        'database': 'qpekalibrary',
        'ignore': [],
        'login':  settings.NDB_USER,
        'password': settings.NDB_PASSWORD
    }
]