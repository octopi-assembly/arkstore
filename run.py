import argparse
import shutil
import sys, traceback
import tempfile

from arkutil import ArkUtil
from loggerd import logger
from config import mysqlconfig, mongoconfig, fileconfig

if mysqlconfig.IS_RDB_ENABLED:
    from arkrdb.mysql import MySQLArk
if fileconfig.IS_FILE_ENABLED:
    from arkfile.file import FileArk
if mongoconfig.IS_NDB_ENABLED:
    from arkndb.mongo import MongoArk


def arkstore(dbbackup=None, config=None, db_targets=None, dest_dir=None):
    '''The entry point of the script.
    '''
    logger.info("Backup Started")
    if dbbackup is None or config is None:
        raise Exception("dbbackup and/or config should not be None.")
    temp_dir = None
    if isinstance(dbbackup, FileArk):
        temp_dir = dest_dir
    else:
        temp_dir = tempfile.mkdtemp()
    try:
        for target in db_targets:
            logger.info("{db} backup started".format(db=target['database']))
            target['config'] = config
            collection = dbbackup.get_target_collections(target=target)
            for col in collection:
                dbbackup.dump_collection(target=target, collection=col, temp_dir=temp_dir)
                if isinstance(dbbackup, MySQLArk):
                    dbbackup.dump_structure(target=target, collection=col, temp_dir=temp_dir)
            if not isinstance(dbbackup, FileArk):
                dbname = target.get('database')
                date_stamp = ArkUtil.getDestination()
                abszipfn = dbbackup.zip_db_dump(dbname=dbname, date_stamp=date_stamp, temp_dir=temp_dir)
                dbbackup.write_to_output(dbname=dbname, dest_dir=dest_dir, abszipfn=abszipfn)
    except StandardError as err:
        #logger.error(str(err))
        #traceback.print_exc(file=sys.stdout)
        logger.exception("message")
        return 1
    finally:
        if not isinstance(dbbackup, FileArk):
            shutil.rmtree(temp_dir)
    logger.info("Backup finished")


def arkrestore(dbrestore=None, config=None, db_targets=None, source_dir=None):
    '''The entry point of the script.
    '''
    logger.info("Restore Started")
    if dbrestore is None or config is None:
        raise Exception("dbrestore and/or config should not be None.")


def run(operation, type):
    '''Run backup service with specified type
    :param type: Options -> mysql, mongo, file
    '''
    # create required disctionary structures
    operation_type = {'mysql': MySQLArk, 'mongo': MongoArk, 'file': FileArk}
    config = {'mysql': mysqlconfig, 'mongo': mongoconfig, 'file': fileconfig}
    # get required configurations
    db_targets = config[type].DB_TARGETS
    dest_dir = config[type].DB_DESTINATION_DIRECTORY

    # Create destination directory if it does not exist
    ArkUtil.createPath(dest_dir)
    if operation == "backup":
        # start backup
        dbbackup = operation_type[type](host=config[type].DB_HOST, port=config[type].DB_PORT)
        sys.exit(arkstore(dbbackup=dbbackup, config=config[type], db_targets=db_targets, dest_dir=dest_dir))
    else:
        # start restore
        dbrestore = operation_type[type](host=config[type].DB_HOST, port=config[type].DB_PORT)
        sys.exit(arkrestore(dbrestore=dbrestore, config=config[type], db_targets=db_targets, source_dir=dest_dir))
        pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Backup & Restore script')
    parser.add_argument('-o','--operation', help='which operation to start, Options: backup or restore', required=True)
    parser.add_argument('-t','--type', help='Type of backup required, Options: mysql or mongo or file', required=True)
    args = parser.parse_args()

    run(args.operation, args.type)