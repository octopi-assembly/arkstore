import os

ZIP_STATUS = True

DATA = "data"
STRUCTURE = "structure"
OPERATION = "exclude"

#CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
CURRENT_DIRECTORY = os.path.dirname(os.getcwd())

# Log configurations
LOG_FILE_NAME = "{log}.log"
LOG_FILE_PATH = os.path.join(CURRENT_DIRECTORY, "backup", "logs")
LOG_ROTATION_WHEN = "midnight"
LOG_BACKUP_COUNT = 7
LOG_UTC_STATUS = True
LOG_FORMATTER = "%(asctime)s | %(pathname)s:%(lineno)d | %(funcName)s | %(levelname)s | %(message)s"

FILE_SOURCE_DIRECTORY = ""
FILE_DESTINATION_DIRECTORY = ""

# Sendgrid Client Credentials
SENDGRID_USER = "hello@mycuteoffice.com"
SENDGRID_PASSWORD = "mycutemail"


FROM_EMAIL = "Server <backup@mycuteoffice.com>"

# administrator list
ADMINS = ["My Cute Office <hello@mycuteoffice.com>"]
