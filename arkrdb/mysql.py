__author__ = 'rahul'

import os
from sh import mysql, mysqldump

from ark import Ark, STRUCTURE, DATA
from arkutil import ArkUtil


class MySQLArk(Ark):
    '''MySQL / MariaDB backup class
    '''
    def __init__(self, **kwargs):
        super(MySQLArk, self).__init__(**kwargs)

    def get_target_collections(self, target):
        '''Get list of tables except tables which configured as ignored.
        '''
        # Execute the SQL query and get the collection
        collection = mysql(h=self.host, port=self.port, u=target['login'], password=target['password'],
                           D=target['database'], execute="SHOW TABLES", N=True)

        ignore = lambda col: (col.startswith(tuple(target['ignore_startswith'])) or col in target['ignore'])
        return [str(col).strip() for col in collection if not ignore(col)]

    def dump_collection(self, target, collection, temp_dir):
        '''Dump target collection to the temporary folder.
        '''
        path = os.path.join(temp_dir, target['database'], DATA)
        ArkUtil.createPath(path)

        logfilepath = os.path.join(target['config'].DB_LOG_DIRECTORY)
        ArkUtil.createPath(logfilepath)

        f = open(os.path.join(path, collection), 'wb', 0)

        # Take a dump of the database table
        mysqldump(target['database'], collection, h=self.host, port=self.port, u=target['login'],
                  password=target['password'], _out=f, log_error='{filepath}/mysql.log'.format(filepath=logfilepath))
        f.close()

    def dump_structure(self, target, collection, temp_dir):
        '''Dump target collections structure to the temporary folder
        '''
        path = os.path.join(temp_dir, target['database'], STRUCTURE)
        ArkUtil.createPath(path)

        f = open(os.path.join(path, collection), 'wb', 0)

        logfilepath = os.path.join(target['config'].DB_LOG_DIRECTORY)
        ArkUtil.createPath(logfilepath)

        e = open(os.path.join(logfilepath, "mysql.log"), 'a', 0)

        # Take a dump of the database table structure
        mysqldump(target['database'], collection, h=self.host, port=self.port, u=target['login'],
                  password=target['password'], log_error='{filepath}/mysql.error.log'.format(filepath=logfilepath),
                  no_data=True, _out=f, _err=e)
        f.close()