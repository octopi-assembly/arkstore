import os
import gzip
import time
import config as settings


class Backup(object):

    def __init__(self):
        pass

    def getDestination(self):
        ''' Getting current datetime to create separate backup folder like "12012013-071334".
        '''
        filestamp = time.strftime('%m%d%Y-%H%M%S')
        return os.path.join(settings.DB_DESTINATION_DIRECTORY, filestamp)

    def createPath(self, path):
        ''' Check if backup folder already exists or not. If not will create it.
        '''
        if not os.path.exists(path):
            os.makedirs(path)

    def isMultiBackup(self):
        ''' Code for checking if you want to take single database backup or assigned multiple backups in DB_LIST_SOURCE_FILE.
        '''
        multi = False
        print "checking for databases names file."
        if os.path.exists(settings.DB_LIST_SOURCE_FILE):
            file1 = open(settings.DB_LIST_SOURCE_FILE)
            multi = True
            print "Databases file found..."
            print "Starting backup of all dbs listed in " + settings.DB_LIST_SOURCE_FILE
        else:
            print "Databases file not found..."
            print "Starting backup of database " + settings.DB_DATABASE
            multi = False
        return multi


class MysqlCmd(object):

    def __init__(self):
        pass

    def getDump(self): # | gzip -c
        return "mysqldump -u%s -p%s -h %s -e --opt -c %s  > %s/%s.sql.gz"

    def getDBStrcture(self): #  | gzip -c
        return "mysqldump -u%s -p%s -h %s -e -d --opt -c %s > %s/%s.sql.gz"

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
    backup = Backup()
    todaybackuppath = backup.getDestination()
    backup.createPath(todaybackuppath)

    if backup.isMultiBackup():
        dblist = get_db_list_from_file()
        mysqlcmd = MysqlCmd()
        for database in dblist:
            if database in ["information_schema", "performance_schema", "mysql"]:
                continue
            else:
                dumpcmd = mysqlcmd.getDump() % (settings.DB_USER, settings.DB_PASSWORD, settings.DB_HOST, database, todaybackuppath, database)
                os.system(dumpcmd)
                #dumpcmd = mysqlcmd.getDBStrcture() % (settings.DB_USER, settings.DB_PASSWORD, settings.DB_HOST, database, todaybackuppath, database)
                #os.system(dumpcmd)
    else:
        database = settings.DB_DATABASE
        dumpcmd = MysqlCmd.getDump() % (settings.DB_USER, settings.DB_PASSWORD, settings.DB_HOST, database, todaybackuppath, database)
        os.system(dumpcmd)
    print "Your backups has been created in '" + todaybackuppath + "' directory"


mysqlcmd = MysqlCmd()
print "Creating database list from command and storing in file."
create_db_list_from_command(mysqlcmd.getDatabaseList())
#print get_db_list_from_file()
print "Database backup started"
backup_database()
print "Deleting database list file"
os.remove(settings.DB_LIST_SOURCE_FILE)
print "Backup script completed"