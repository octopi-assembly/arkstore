import os

FILE_FORMAT = "db-%s.sql"

ZIP_STATUS = True

CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

FILE_SOURCE_DIRECTORY = ""
FILE_DESTINATION_DIRECTORY = ""

# MySql configurations
RDB_HOST = "localhost"
RDB_PORT = 3306
RDB_USER = "root"
RDB_PASSWORD = "root"
RDB_DEFAULT_DB = "mco"
RDB_IGNORE = ["information_schema", "performance_schema", "mysql"]
RDB_DUMP = 'mysqldump'

RDB_LIST_LOAD_FROM_DB = True
RDB_LIST_SOURCE_FILE = os.path.join(CURRENT_DIRECTORY, "db_list.txt")
RDB_DESTINATION_DIRECTORY = os.path.join(CURRENT_DIRECTORY, "backup", "rdb")

# Mongo configurations
NDB_HOST = "localhost"
NDB_PORT = 27017
NDB_USER = "root"
NDB_PASSWORD = "root"
NDB_DEFAULT_DB = "mco"
NDB_IGNORE = ["local", "test"]
NDB_DUMP = 'mongodump'

NDB_LIST_LOAD_FROM_DB = True
NDB_LIST_SOURCE_FILE = os.path.join(CURRENT_DIRECTORY, "db_list.txt")
NDB_DESTINATION_DIRECTORY = os.path.join(CURRENT_DIRECTORY, "backup", "ndb")

# Mail server
EMAIL_SERVER = "localhost"
SMTP_PORT = "9025"
FROM_EMAIL = "Server <server@mycuteoffice.com>"
# email server
MAIL_SERVER = "localhost"
MAIL_PORT = 25
MAIL_USE_TLS = False
MAIL_USE_SSL = False
MAIL_USERNAME = "mycuteoffice"
MAIL_PASSWORD = ''
# Sendgrid Client Credentials
SENDGRID_USER = "hello@mycuteoffice.com"
SENDGRID_PASSWORD = "mycutemail"

# administrator list
ADMINS = ["My Cute Office <hello@mycuteoffice.com>"]
