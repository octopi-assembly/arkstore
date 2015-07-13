__author__ = 'rahul'

import config as settings


DB_TARGETS = [
    {
        'database': 'gogo',
        'ignore': ['cache'],
        'ignore_startswith': 'cache',
        'login':  settings.RDB_USER,
        'password': settings.RDB_PASSWORD
    },
    {
        'database': 'qpeka',
        'ignore': [],
        'ignore_startswith': 'cache',
        'login':  settings.RDB_USER,
        'password': settings.RDB_PASSWORD
    }
]