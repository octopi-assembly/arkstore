__author__ = 'rahul'

# -*- coding: utf-8 -*-
'''Dump MongoDB databases to the zip archives
and copy its to the output folder.
Usage: python mongotgz.py
'''

import os
import tempfile
import shutil
import subprocess
import sys
import tarfile

from pymongo import MongoClient

from backuputil import BackupUtil
import config as settings
import mongoconfig as config


def get_target_collections(target):
    '''Get list of collections except system collections
    and collections which configured as ignored.
    '''
    mongo = MongoClient(settings.NDB_HOST, settings.NDB_PORT)
    dbname = target['database']
    ignores = target['ignore']
    login = target['login']
    password = target['password']
    database = mongo[dbname]
    database.authenticate(login, password)
    #database.read_preference = ReadPreference.SECONDARY
    ignore = lambda col: col.startswith('system.') or col in ignores
    return [col for col in database.collection_names() if not ignore(col)]


def dump_collection(target, collection, temp_dir):
    '''Dump target collection to the temporary folder.'''
    dbname = target['database']
    login = target['login']
    password = target['password']
    args = [
        settings.NDB_DUMP,
        '-h', settings.NDB_HOST,
        '--port', str(settings.NDB_PORT),
        '-d', dbname,
        '-c', collection,
        '-u', login,
        '-p', password,
        '-o', temp_dir
    ]
    subprocess.call(args)


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
    output_dir = settings.NDB_DESTINATION_DIRECTORY
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
    temp_dir = tempfile.mkdtemp()
    try:
        for target in config.DB_TARGETS:
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


if __name__ == '__main__':
    sys.exit(main())