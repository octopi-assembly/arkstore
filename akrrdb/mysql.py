__author__ = 'rahul'

import os
from sh import mysql, mysqldump

from ark import Ark, STRUCTURE
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
                           D=target['database'], execute="SHOW TABLES")

        ignore = lambda col: (col.startswith("Tables_in") or col.startswith(target['ignore_startswith'])
                              or col in target['ignore'])
        return [str(col).strip() for col in collection if not ignore(col)]

    def dump_collection(self, target, collection, temp_dir):
        '''Dump target collection to the temporary folder.
        '''
        path = os.path.join(temp_dir, target['database'])
        ArkUtil.createPath(path)

        f = open(os.path.join(path, collection), 'wb', 0)
        # Take a dump of the database table
        # can be included : B=target['database'], tables=collection
        mysqldump(target['database'], collection, h=self.host, port=self.port, u=target['login'],
                  password=target['password'], _out=f)
        f.close()

    def dump_structure(self, target, collection, temp_dir):
        '''Dump target collections structure to the temporary folder
        '''
        path = os.path.join(temp_dir, target['database'], STRUCTURE)
        ArkUtil.createPath(path)

        f = open(os.path.join(path, collection), 'wb', 0)

        # Take a dump of the database table structure
        # can be included : B=target['database'], tables=collection
        mysqldump(target['database'], collection, h=self.host, port=self.port, u=target['login'],
                  password=target['password'], no_data=True, _out=f)
        f.close()


