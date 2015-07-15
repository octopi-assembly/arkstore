__author__ = 'rahul'

import os
import subprocess

from ark import Ark


OPERATION = "exclude"


class FileArk(Ark):
    '''Backup directory structure and files
    '''
    def __init__(self, **kwargs):
        super(FileArk, self).__init__(**kwargs)

    def get_target_collections(self, target):
        '''Get list of files except ignore directories and file extensions.
        '''
        ignore = (lambda col, status: "{col}/{newline}".format(col=col, newline='\n') if status
                    else "{col}{newline}".format(col=col, newline='\n'))
        ignores = [ignore(col, False) for col in target['config'].DB_IGNORE]
        ignores += [ignore(col, True) for col in target['ignore']]
        ignores.append(target['ignore_startswith'])
        exclude_from = open((target['config'].DB_LIST_SOURCE_FILE).format(operation=OPERATION), 'w')
        exclude_from.writelines(ignores)
        exclude_from.close()
        return [exclude_from.name]

    def dump_collection(self, db_dump, target, collection, temp_dir):
        '''Dump target collection to the temporary folder.
        '''
        dbname = target['database']
        args = [
            db_dump,
            '-az',
            '--exclude-from', collection,
            '-q',
            '--log-file=/var/log/backup/files.log',
            dbname + os.sep,
            temp_dir + os.sep
        ]
        subprocess.call(args)