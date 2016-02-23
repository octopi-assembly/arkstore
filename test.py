

import os
import subprocess
import MySQLdb as MariaDB
from pymongo import MongoClient

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
        dbname = target['database']
        ignores = target['ignore']
        login = target['login']
        password = target['password']
        connection = MariaDB.connect(host=self.host, port=self.port, user=login, passwd=password, db=dbname)
        cursor = connection.cursor()

        # Execute the SQL query and get the response
        cursor.execute("SHOW TABLES")
        response = cursor.fetchall()
        ignore = lambda col: col.startswith(target['ignore_startswith']) or col in ignores
        return [col[0] for col in response if not ignore(col[0])]

    def dump_collection(self, db_dump, target, collection, temp_dir):
        '''Dump target collection to the temporary folder.
        '''
        dbname = target['database']
        login = target['login']
        password = target['password']
        args = [
            db_dump,
            '-h', self.host,
            '--port', str(self.port),
            '--databases', dbname,
            '--tables', collection,
            '-u', login,
            '-p' + password
        ]
        path = os.path.join(temp_dir, dbname)
        ArkUtil.createPath(path)
        f = open(os.path.join(path, collection), 'wb', 0)
        subprocess.call(args, stdout=f)
        f.close()

    def dump_structure(self, db_dump, target, collection, temp_dir):
        '''Dump target collections structure to the temporary folder
        '''
        dbname = target['database']
        login = target['login']
        password = target['password']
        args = [
            db_dump,
            '-h', self.host,
            '--port', str(self.port),
            '--databases', dbname,
            '--tables', collection,
            '-u', login,
            '-p' + password,
            '--no-data'
        ]
        path = os.path.join(temp_dir, dbname, STRUCTURE)
        ArkUtil.createPath(path)
        f = open(os.path.join(path, collection), 'wb', 0)
        subprocess.call(args, stdout=f)
        f.close()


class MongoArk(Ark):
    '''MongoDb backup class
    '''
    def __init__(self, **kwargs):
        super(MongoArk, self).__init__(**kwargs)

    def get_target_collections(self, target):
        '''Get list of collections except system collections
        and collections which configured as ignored.
        '''
        dbname = target['database']
        ignores = target['ignore']
        login = target['login']
        password = target['password']
        mongo = MongoClient(self.host, self.port)
        database = mongo[dbname]
        database.authenticate(login, password)
        #database.read_preference = ReadPreference.SECONDARY
        ignore = lambda col: col.startswith(target['ignore_startswith']) or col in ignores
        return [col for col in database.collection_names() if not ignore(col)]

    def dump_collection(self, db_dump, target, collection, temp_dir):
        '''Dump target collection to the temporary folder.
        '''
        dbname = target['database']
        login = target['login']
        password = target['password']
        args = [
            db_dump,
            '-h', self.host,
            '--port', str(self.port),
            '-d', dbname,
            '-c', collection,
            '-u', login,
            '-p', password,
            '-o', temp_dir
        ]
        subprocess.call(args)