__author__ = 'rahul'

import os
import sys
import tempfile
import shutil
import subprocess
import tarfile
import MySQLdb as MariaDB
from pymongo import MongoClient

from backuputil import BackupUtil


STRUCTURE = "structure"


class DbBackup(object):
    '''Database backup class.
    '''
    def __init__(self, **kwargs):
        self.host = kwargs.get('host')
        self.port = kwargs.get('port')

    def get_target_collections(self, **kwargs):
        '''Abstract function to get all collections or tables
        '''
        pass

    def dump_collection(self, **kwargs):
        '''Abstract function to dump all the collections or tables.
        '''
        pass

    def zip_db_dump(self, dbname, date_stamp, temp_dir):
        '''Zip database dump directory.
        '''
        source_zip = os.path.join(temp_dir, dbname)
        zip_name = '{dbname}.{date}.tar.gz'.format(dbname=dbname, date=date_stamp)
        target_zip = os.path.join(temp_dir, zip_name)
        with tarfile.open(target_zip, 'w:gz') as mytar:
            for root, _, files in os.walk(source_zip):
                for fname in files:
                    absfn = os.path.join(root, fname)
                    if not root.endswith(STRUCTURE):
                        mytar.add(absfn, arcname=os.path.join(dbname, fname))
                    else:
                        mytar.add(absfn, arcname=os.path.join(dbname, STRUCTURE, fname))
        return target_zip

    def write_to_output(self, dbname, dest_dir, abszipfn):
        '''Copy archive to the output and rewrite latest database archive.
        '''
        BackupUtil.createPath(dest_dir)
        _, zipfn = os.path.split(abszipfn)
        move_to = os.path.join(dest_dir, zipfn)
        shutil.move(abszipfn, move_to)
        latest = '{dbname}.latest.tar.gz'.format(dbname=dbname)
        latest = os.path.join(dest_dir, latest)
        shutil.copy2(move_to, latest)


class MySQL(DbBackup):
    '''MySQL / MariaDB backup class
    '''
    def __init__(self, **kwargs):
        super(MySQL, self).__init__(**kwargs)

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
        BackupUtil.createPath(path)
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
        BackupUtil.createPath(path)
        f = open(os.path.join(path, collection), 'wb', 0)
        subprocess.call(args, stdout=f)
        f.close()


class Mongo(DbBackup):
    '''MongoDb backup class
    '''
    def __init__(self, **kwargs):
        super(Mongo, self).__init__(**kwargs)

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


def backup(dbbackup=None, db_dump=None, db_targets=None, dest_dir=None):
    '''The entry point of the script.
    '''
    print "Database backup started"
    if dbbackup is None:
        raise Exception("dbbackup should not be None.")
    temp_dir = tempfile.mkdtemp()
    try:
        for target in db_targets:
            print target['database'], " backup started"
            cols = dbbackup.get_target_collections(target=target)
            for col in cols:
                dbbackup.dump_collection(db_dump=db_dump, target=target, collection=col, temp_dir=temp_dir)
                if isinstance(dbbackup, MySQL):
                    dbbackup.dump_structure(db_dump=db_dump, target=target, collection=col, temp_dir=temp_dir)
            dbname = target.get('database')
            date_stamp = BackupUtil.getDestination()
            abszipfn = dbbackup.zip_db_dump(dbname=dbname, date_stamp=date_stamp, temp_dir=temp_dir)
            dbbackup.write_to_output(dbname=dbname, dest_dir=dest_dir, abszipfn=abszipfn)
    except StandardError as err:
        print  >> sys.stderr. str(err)
        return 1
    finally:
        shutil.rmtree(temp_dir)
    print "Database backup finished"