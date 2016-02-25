import os
import logging
from logging.handlers import TimedRotatingFileHandler

from config.arkconfig import (LOG_FILE_PATH, LOG_FILE_NAME, LOG_FORMATTER, LOG_ROTATION_WHEN, LOG_BACKUP_COUNT,
                              LOG_UTC_STATUS)


def init_log():
    # create logger with 'arkstore'
    logfile_name = os.path.split(os.path.dirname(os.path.abspath(__file__)))[1]
    logger = logging.getLogger(logfile_name)
    logger.setLevel(logging.DEBUG)

    # create file handler which logs even debug messages
    if not os.path.exists(LOG_FILE_PATH):
        os.makedirs(LOG_FILE_PATH)

    logfile = os.path.join(LOG_FILE_PATH, LOG_FILE_NAME.format(log=logfile_name))
    fh = TimedRotatingFileHandler(logfile, when=LOG_ROTATION_WHEN, backupCount=LOG_BACKUP_COUNT, utc=LOG_UTC_STATUS)
    fh.setLevel(logging.DEBUG)

    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)

    # create formatter and add it to the handlers
    formatter = logging.Formatter(LOG_FORMATTER)
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger


logger = init_log()