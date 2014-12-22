import pymongo
import datetime
import os


class DbConnection():
    QUEUE = 'queue'
    USED = 'used'
    DB_NAME = 'psuRegisAlert'

    def __init__(self):
        dbHost = os.environ.get('DB_PORT', 'mongodb://localhost:27017')
        if dbHost.startswith("tcp"):
            dbHost = dbHost.replace("tcp", "mongodb")

        connection = pymongo.MongoClient(dbHost)
        self.db = connection[self.DB_NAME]

    def _query_all(self, collection):
        dbCursor = self.db[collection].find()
        if dbCursor and dbCursor.count() > 0:
            return dbCursor

    def _insert_item(self, item, collection):
        self.db[collection].insert(item)

    def query_queue_all(self):
        return self._query_all(self.QUEUE)

    def query_used_all(self):
        return self._query_all(self.USED)

    def remove(self, item):
        self.db[self.QUEUE].remove(item)
        _item = item.copy()
        _item['achived_date'] = datetime.datetime.utcnow()
        self._insert_item(_item, self.USED)

    def insert_item(self, subject_code, email):
        item = {'subject_code': subject_code, 'email': email,
                'date': datetime.datetime.utcnow()}
        self._insert_item(item, self.QUEUE)
