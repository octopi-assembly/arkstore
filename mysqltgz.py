__author__ = 'rahul'

# -*- coding: utf-8 -*-
'''Dump MySQL / MariaDB databases to the zip archives
and copy its to the output folder.
Usage: python mysqltgz.py
'''

import os
import tempfile
import shutil
import subprocess
import sys
import tarfile

import MySQLdb as MariaDB

from backuputil import BackupUtil
import config as settings
import mysqlconfig as config


def get_target_collections(target):
    '''Get list of tables except cache tables
    and tables which configured as ignored.
    '''
    connection = MariaDB.connect(host=settings.RDB_HOST, user=settings.RDB_USER, passwd=settings.RDB_PASSWORD,
                                 db=target['database'])
    cursor = connection.cursor()

    # Execute the SQL query and get the response
    cursor.execute("SHOW TABLES")
    response = cursor.fetchall()
    ignores = target['ignore']
    ignore = lambda col: col.startswith('cache') or col in ignores
    return [col[0] for col in response if not ignore(col[0])]


def dump_collection(target, collection, temp_dir):
    '''Dump target collection to the temporary folder.'''
    dbname = target['database']
    login = target['login']
    password = target['password']
    args = [
        settings.RDB_DUMP,
        '-h', settings.RDB_HOST,
        '--port', str(settings.RDB_PORT),
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


def zip_db_dump(dbname, temp_dir):
    '''Zip database dump folder.'''
    source_zip = os.path.join(temp_dir, dbname)
    date_stamp = BackupUtil.getDestination()
    zip_name = '{dbname}.{date}.tar.gz'.format(dbname=dbname, date=date_stamp)
    target_zip = os.path.join(temp_dir, zip_name)
    with tarfile.open(target_zip, 'w:gz') as mytar:
        for root, _, files in os.walk(source_zip):
            for fname in files:
                absfn = os.path.join(root, fname)
                mytar.add(absfn)
    return target_zip


def write_to_output(dbname, abszipfn):
    '''Copy archive to the output and rewrite latest database archive.'''
    output_dir = settings.RDB_DESTINATION_DIRECTORY
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    _, zipfn = os.path.split(abszipfn)
    move_to = os.path.join(output_dir, zipfn)
    shutil.move(abszipfn, move_to)
    latest = '{dbname}.latest.tar.gz'.format(dbname=dbname)
    latest = os.path.join(output_dir, latest)
    shutil.copy2(move_to, latest)


def main():
    '''The entry point of the script.'''
    print "Database backup started"
    temp_dir = tempfile.mkdtemp()
    try:
        for target in config.DB_TARGETS:
            print target['database'], " backup started"
            cols = get_target_collections(target)
            for col in cols:
                dump_collection(target, col, temp_dir)
            dbname = target['database']
            abszipfn = zip_db_dump(dbname, temp_dir)
            write_to_output(dbname, abszipfn)
    except StandardError as err:
        print >> sys.stderr, str(err)
        return 1
    finally:
        shutil.rmtree(temp_dir)
    print "Database backup finished"


if __name__ == '__main__':
    sys.exit(main())