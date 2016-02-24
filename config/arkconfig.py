import os

ZIP_STATUS = True

DATA = "data"
STRUCTURE = "structure"
OPERATION = "exclude"

#CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
CURRENT_DIRECTORY = os.path.dirname(os.getcwd())

FILE_SOURCE_DIRECTORY = ""
FILE_DESTINATION_DIRECTORY = ""

# Sendgrid Client Credentials
SENDGRID_USER = "hello@mycuteoffice.com"
SENDGRID_PASSWORD = "mycutemail"


FROM_EMAIL = "Server <backup@mycuteoffice.com>"

# administrator list
ADMINS = ["My Cute Office <hello@mycuteoffice.com>"]
