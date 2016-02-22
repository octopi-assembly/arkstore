__author__ = 'rahul'

import sys
import argparse
import shutil
import tempfile
from arkutil import ArkUtil

from arkdb import MySQLArk, MongoArk
from arkfile import FileArk
import mysqlconfig
import mongoconfig
import fileconfig


def arkstore(dbbackup=None, config=None, db_dump=None, db_targets=None, dest_dir=None):
    '''The entry point of the script.
    '''
    print "Backup started"
    if dbbackup is None or config is None:
        raise Exception("dbbackup and/or config should not be None.")
    temp_dir = None
    if isinstance(dbbackup, FileArk):
        temp_dir = dest_dir
    else:
        temp_dir = tempfile.mkdtemp()
    try:
        for target in db_targets:
            print target['database'], "backup started"
            target['config'] = config
            cols = dbbackup.get_target_collections(target=target)
            for col in cols:
                dbbackup.dump_collection(db_dump=db_dump, target=target, collection=col, temp_dir=temp_dir)
                if isinstance(dbbackup, MySQLArk):
                    dbbackup.dump_structure(db_dump=db_dump, target=target, collection=col, temp_dir=temp_dir)
            if not isinstance(dbbackup, FileArk):
                dbname = target.get('database')
                date_stamp = ArkUtil.getDestination()
                abszipfn = dbbackup.zip_db_dump(dbname=dbname, date_stamp=date_stamp, temp_dir=temp_dir)
                dbbackup.write_to_output(dbname=dbname, dest_dir=dest_dir, abszipfn=abszipfn)
    except StandardError as err:
        print  >> sys.stderr. str(err)
        return 1
    finally:
        if not isinstance(dbbackup, FileArk):
            shutil.rmtree(temp_dir)
    print "Backup finished"


def run(type):
    '''Run backup service with specified type
    :param type: Options -> mysql, mongo, file
    '''
    # create required disctionary structures
    backup_type = {'mysql': MySQLArk, 'mongo': MongoArk, 'file': FileArk}
    config = {'mysql': mysqlconfig, 'mongo': mongoconfig, 'file': fileconfig}
    # get required configurations
    db_dump = config[type].DB_DUMP
    db_targets = config[type].DB_TARGETS
    dest_dir = config[type].DB_DESTINATION_DIRECTORY
    # Create destination directory if it does not exist
    ArkUtil.createPath(dest_dir)
    # start backup
    dbbackup = backup_type[type](host=config[type].DB_HOST, port=config[type].DB_PORT)
    sys.exit(arkstore(dbbackup=dbbackup, config=config[type], db_dump=db_dump, db_targets=db_targets, dest_dir=dest_dir))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Backup script')
    parser.add_argument('-t','--type', help='Type of backup required, Options: mysql or mongo or file',required=True)
    args = parser.parse_args()

    run(args.type)