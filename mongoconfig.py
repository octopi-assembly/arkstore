__author__ = 'rahul'

import config as settings


DB_TARGETS = [
    {
        'database': 'mco',
        'ignore': ['fs.chunks'],
        'ignore_startswith': 'system.',
        'login':  settings.NDB_USER,
        'password': settings.NDB_PASSWORD
    },
    {
        'database': 'qpekalibrary',
        'ignore': [],
        'ignore_startswith': 'system.',
        'login':  settings.NDB_USER,
        'password': settings.NDB_PASSWORD
    }
]