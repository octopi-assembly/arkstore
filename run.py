__author__ = 'rahul'

import tempfile
import shutil
import sys

from backuputil import BackupUtil
from dbbackup import MySQL, Mongo
import config as settings
import mysqlconfig
import mongoconfig


def mysql_backup():
    '''The entry point of the script.'''
    print "Database backup started"
    temp_dir = tempfile.mkdtemp()
    mysql = MySQL(host=settings.RDB_HOST, port=settings.RDB_PORT)
    db_dump = settings.RDB_DUMP
    try:
        for target in mysqlconfig.DB_TARGETS:
            print target['database'], " backup started"
            cols = mysql.get_target_collections(target=target)
            for col in cols:
                mysql.dump_collection(db_dump=db_dump, target=target, collection=col, temp_dir=temp_dir)
            dbname = target['database']
            date_stamp = BackupUtil.getDestination()
            abszipfn = mysql.zip_db_dump(dbname=dbname, date_stamp=date_stamp, temp_dir=temp_dir)
            dest_dir = settings.RDB_DESTINATION_DIRECTORY
            mysql.write_to_output(dbname=dbname, dest_dir=dest_dir, abszipfn=abszipfn)
    except StandardError as err:
        print >> sys.stderr, str(err)
        return 1
    finally:
        shutil.rmtree(temp_dir)
    print "Database backup finished"


def mongo_backup():
    '''The entry point of the script.'''
    temp_dir = tempfile.mkdtemp()
    mongo = Mongo(host=settings.NDB_HOST, port=settings.NDB_PORT)
    db_dump = settings.NDB_DUMP
    try:
        for target in mongoconfig.DB_TARGETS:
            cols = mongo.get_target_collections(target=target)
            for col in cols:
                mongo.dump_collection(db_dump=db_dump, target=target, collection=col, temp_dir=temp_dir)
            dbname = target['database']
            date_stamp = BackupUtil.getDestination()
            abszipfn = mongo.zip_db_dump(dbname=dbname, date_stamp=date_stamp, temp_dir=temp_dir)
            dest_dir = settings.NDB_DESTINATION_DIRECTORY
            mongo.write_to_output(dbname=dbname, dest_dir=dest_dir, abszipfn=abszipfn)
    except StandardError as err:
        print >> sys.stderr, str(err)
        return 1
    finally:
        shutil.rmtree(temp_dir)


if __name__ == '__main__':
    sys.exit(mongo_backup())