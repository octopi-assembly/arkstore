import os
import ast
from sh import mongo, mongodump

from ark import Ark
from arkutil import ArkUtil


class MongoArk(Ark):
    '''MongoDb backup class
    '''
    def __init__(self, **kwargs):
        super(MongoArk, self).__init__(**kwargs)

    def get_target_collections(self, target):
        '''Get list of collections except system collections
        and collections which configured as ignored.
        '''
        collection = mongo(target['database'], host=self.host, port=self.port, u=target['login'], p=target['password'],
              eval="db.getCollectionNames()", quiet=True)
        for item in collection:
            collection = ast.literal_eval(item) if isinstance(item, unicode) or isinstance(item, str) else item

        ignore = lambda col: col.startswith(tuple(target['ignore_startswith'])) or col in target['ignore']
        return [str(col).strip() for col in collection if not ignore(col)]

    def dump_collection(self, target, collection, temp_dir):
        '''Dump target collection to the temporary folder.
        '''
        path = os.path.join(temp_dir, target['database'])
        ArkUtil.createPath(path)

        logfilepath = os.path.join(target['config'].DB_LOG_DIRECTORY)
        ArkUtil.createPath(logfilepath)

        f = open(os.path.join(logfilepath, "mongo.log"), 'a', 0)

         # Take a dump of the database collection
        mongodump(h=self.host, port=self.port, d=target['database'], c=collection, u=target['login'],
                  p=target['password'], o=path, _err=f)