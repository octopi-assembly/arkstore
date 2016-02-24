__author__ = 'rahul'

import shutil
import tarfile

import os
from arkutil import ArkUtil
from config.arkconfig import DATA, STRUCTURE, OPERATION


class Ark(object):
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
                        mytar.add(absfn, arcname=os.path.join(dbname, DATA, fname))
                    else:
                        mytar.add(absfn, arcname=os.path.join(dbname, STRUCTURE, fname))
        return target_zip

    def write_to_output(self, dbname, dest_dir, abszipfn):
        '''Copy archive to the output and rewrite latest database archive.
        '''
        ArkUtil.createPath(dest_dir)
        _, zipfn = os.path.split(abszipfn)
        move_to = os.path.join(dest_dir, zipfn)
        shutil.move(abszipfn, move_to)
        latest = '{dbname}.latest.tar.gz'.format(dbname=dbname)
        latest = os.path.join(dest_dir, latest)
        shutil.copy2(move_to, latest)