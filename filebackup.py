__author__ = 'rahul'

import os
import sys
import tempfile
import shutil
import subprocess
import tarfile

from backuputil import BackupUtil
import fileconfig


STRUCTURE = "structure"


class FileBackup(object):
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


class Files(FileBackup):
    '''Backup directory structure and files
    '''
    def __init__(self, **kwargs):
        super(Files, self).__init__(**kwargs)

    def get_target_collections(self, target):
        '''Get list of files except ignore directories and file extensions.
        '''
        dbname = target['database']
        ignores = target['ignore']
        login = target['login']
        password = target['password']
        files = os.listdir(dbname)
        for root, dirs, files in os.walk(dbname):
            if root.endswith():
                print(root, dirs, files)
        #ignore = lambda col: col.startswith(target['ignore_startswith']) or col in ignores
        #return [col for col in database.collection_names() if not ignore(col)]

    def dump_collection(self, db_dump, target, collection, temp_dir):
        '''Dump target collection to the temporary folder.
        '''
        dbname = target['database']
        login = target['login']
        password = target['password']
        args = [
            db_dump,
            '--include-from', dbname,
            '--exclude-from', collection,
            '-q',
            '--log-file=/var/log/backup/files.log',
            dbname + os.sep,
            temp_dir + os.sep
        ]
        subprocess.call(args)


def backup(dbbackup=None, db_dump=None, db_targets=None, dest_dir=None):
    '''The entry point of the script.
    '''
    print "Files backup started"
    if dbbackup is None:
        raise Exception("dbbackup should not be None.")
    temp_dir = tempfile.mkdtemp()
    try:
        for target in db_targets:
            print target['database'], " backup started"
            #cols = dbbackup.get_target_collections(target=target)
            rsync -az --exclude-from 'exclude-list.txt' --include-from 'include-list.txt' --log-file='/var/log/backup/files.log' -q files/ test/
            dbbackup.dump_collection(db_dump=db_dump, target=target, collection=col, temp_dir=temp_dir)
            #for col in cols:
            #    dbbackup.dump_collection(db_dump=db_dump, target=target, collection=col, temp_dir=temp_dir)
            #dbname = target.get('database')
            #date_stamp = BackupUtil.getDestination()
            #abszipfn = dbbackup.zip_db_dump(dbname=dbname, date_stamp=date_stamp, temp_dir=temp_dir)
            #dbbackup.write_to_output(dbname=dbname, dest_dir=dest_dir, abszipfn=abszipfn)
    except StandardError as err:
        print  >> sys.stderr. str(err)
        return 1
    finally:
        shutil.rmtree(temp_dir)
    print "Database backup finished"


if __name__ == "__main__":
    files = Files(host=fileconfig.FILE_HOST, port=fileconfig.FILE_PORT)
    backup(dbbackup=files, db_dump=fileconfig.FILE_DUMP, db_targets=fileconfig.FILE_TARGETS, dest_dir=fileconfig.FILE_DESTINATION_DIRECTORY)