import os

FILE_FORMAT = "db-%s.sql"

ZIP_STATUS = True

CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

FILE_SOURCE_DIRECTORY = ""
FILE_DESTINATION_DIRECTORY = ""

DB_LIST_SOURCE_FILE = os.path.join(CURRENT_DIRECTORY, "db_list.txt")
DB_DESTINATION_DIRECTORY = os.path.join(CURRENT_DIRECTORY, "backup", "db")

# MySql configurations
DB_HOST = "localhost"
DB_PORT = "3306"
DB_USER = "root"
DB_PASSWORD = "root"
DB_DATABASE = "mco"
# MySql commands
DB_URI = "mysql://%s:%s@%s/%s" % (DB_USER, DB_PASSWORD, DB_HOST, DB_DATABASE)

# Mail server
EMAIL_SERVER = "localhost"
SMTP_PORT = "9025"
FROM_EMAIL = "Server <server@mycuteoffice.com>"
# email server
MAIL_SERVER = "localhost"
MAIL_PORT = 25
MAIL_USE_TLS = False
MAIL_USE_SSL = False
MAIL_USERNAME = "surgeonsquests"
MAIL_PASSWORD = ''
# Sendgrid Client Credentials
SENDGRID_USER = "hello@mycuteoffice.com"
SENDGRID_PASSWORD = "mycutemail"

# administrator list
ADMINS = ["My Cute Office <hello@mycuteoffice.com>"]
