#!/usr/bin/python

import os
import time
import config as settings

#os.system("which python")

# Getting current datetime to create seprate backup folder like
# "12012013-071334".
filestamp = time.strftime('%m%d%Y-%H%M%S')
todaybackuppath = os.path.join(settings.DB_DESTINATION_DIRECTORY, filestamp)

# Checking if backup folder already exists or not. If not will create it.
print "creating backup folder"
if not os.path.exists(todaybackuppath):
    os.makedirs(todaybackuppath)

# Code for checking if you want to take single database backup or assinged
# multiple backups in DB_LIST_SOURCE_FILE.
print "checking for databases names file."
if os.path.exists(settings.DB_LIST_SOURCE_FILE):
    file1 = open(settings.DB_LIST_SOURCE_FILE)
    multi = 1
    print "Databases file found..."
    print "Starting backup of all dbs listed in " + settings.DB_LIST_SOURCE_FILE
else:
    print "Databases file not found..."
    print "Starting backup of database " + settings.DB_DATABASE
    multi = 0

# Starting actual database backup process.
if multi:
    in_file = open(settings.DB_LIST_SOURCE_FILE, "r")
    flength = len(in_file.readlines())
    in_file.close()
    p = 1
    dbfile = open(settings.DB_LIST_SOURCE_FILE, "r")

    while p <= flength:
        db = dbfile.readline()  # reading database name from file
        db = db[:-1]  # deletes extra line
        dumpcmd = "mysqldump -u %s -p%s -h %s -e --opt -c %s | gzip -c > %s/%s.sql.gz" % (settings.DB_USER, settings.DB_PASSWORD, settings.DB_HOST, db, todaybackuppath, db)
        os.system(dumpcmd)
        p = p + 1
        dbfile.close()
else:
    db = settings.DB_DATABASE
    dumpcmd = "mysqldump -u %s -p%s -h %s -e --opt -c %s | gzip -c > %s/%s.sql.gz" % (settings.DB_USER, settings.DB_PASSWORD, settings.DB_HOST, db, todaybackuppath, db)
    os.system(dumpcmd)

print "Backup script completed"
print "Your backups has been created in '" + todaybackuppath + "' directory"
