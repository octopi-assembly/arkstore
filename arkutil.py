import os
import time


class ArkUtil(object):

    def __init__(self):
        pass

    @classmethod
    def getDestination(cls, destinationdir=None):
        ''' Getting current datetime to create separate backup folder like "12012013-071334".
        '''
        filestamp = time.strftime('%m-%d-%Y-%H%M%S')
        if destinationdir:
            return os.path.join(destinationdir, filestamp)
        else:
            return filestamp

    @classmethod
    def createPath(cls, path):
        ''' Check if backup folder already exists or not. If not will create it.
        '''
        if not os.path.exists(path):
            os.makedirs(path)

    @classmethod
    def is_non_zero_file(cls, fpath):
        ''' Check if file exist and has content or not
        '''
        return True if os.path.isfile(fpath) and os.path.getsize(fpath) > 0 else False