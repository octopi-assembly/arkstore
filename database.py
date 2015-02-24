import os
import gzip
import config as settings


class MysqlCmd(object):

    def __init__(self):
        pass

    def getDump(self):
        return "mysqldump -u%s -p%s -h %s -e --opt -c %s | gzip -c > %s.sql.gz"

    def getDatabaseList(self):
        return "mysql -u %s -p%s -h %s --silent -N -e 'show databases' > %s"


def create_db_list_from_command(dblistcmd):
    os.system(dblistcmd % (settings.DB_USER, settings.DB_PASSWORD,
                           settings.DB_HOST, settings.DB_LIST_SOURCE_FILE))


def get_db_list_from_file():
    dblist = []
    with open(settings.DB_LIST_SOURCE_FILE, 'rb') as listfile:
        if settings.DB_LIST_SOURCE_FILE.endswith(".gz"):
            listfile = gzip.open(fileobj=listfile)
        dblist = [line.rstrip() for line in listfile]
    return dblist


def backup_database():
    dblist = get_db_list_from_file()
    for database in dblist:
        if database in ["information_schema", "performance_schema"]:
            continue
        else:
            print database


mysqlcmd = MysqlCmd()
create_db_list_from_command(mysqlcmd.getDatabaseList())
#print get_db_list_from_file()
backup_database()
