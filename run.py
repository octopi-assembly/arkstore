__author__ = 'rahul'


import sys
import argparse

from dbbackup import MySQL, Mongo, backup
import mysqlconfig
import mongoconfig


def run(type):
    # create required disctionary structures
    backup_type = {'mysql': MySQL, 'mongo': Mongo}
    filename = {'mysql': mysqlconfig, 'mongo': mongoconfig}
    # get required configurations
    db_dump = filename[type].DB_DUMP
    db_targets = filename[type].DB_TARGETS
    dest_dir = filename[type].DB_DESTINATION_DIRECTORY
    # start backup
    dbbackup = backup_type[type](host=filename[type].DB_HOST, port=filename[type].DB_PORT)
    sys.exit(backup(dbbackup=dbbackup, db_dump=db_dump, db_targets=db_targets, dest_dir=dest_dir))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Backup script')
    parser.add_argument('-t','--type', help='Type of database backup required, Options: mysql or mongo',required=True)
    args = parser.parse_args()

    run(args.type)
