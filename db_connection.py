import pymongo
import datetime
import os


class DbConnection(object):
    QUEUE = 'queue'
    USED = 'used'
    DB_NAME = 'psuRegisAlert'

    def __init__(self):
        MONGO_URL = os.getenv('MONGO_URL', 'mongodb://localhost:27017')
        dbHost = "{0}".format(MONGO_URL)
        connection = pymongo.MongoClient(dbHost)
        self.con = connection
        self.db = connection[self.DB_NAME]

    def _query_all(self, collection):
        dbCursor = self.db[collection].find()
        if dbCursor and dbCursor.count() > 0:
            return dbCursor

    def _insert_item(self, item, collection):
        # self.db[collection].insert(item)

        # use upsert to prevent duplicate documents
        key = {key: value for key, value in item.items() if key is not "date"}
        self.db[collection].update(key, item, upsert=True)

    def query_queue_all(self):
        return self._query_all(self.QUEUE)

    def query_used_all(self):
        return self._query_all(self.USED)

    def remove(self, item):
        self.db[self.QUEUE].remove(item)
        _item = item.copy()
        _item['achived_date'] = datetime.datetime.utcnow()
        self._insert_item(_item, self.USED)

    def insert_item(self, url, subject_code, email, line_id, sec='*'):
        item = {
            'url': url,
            'subject_code': subject_code,
            'email': email,
            'sec': sec,
            'line_id': line_id,
            'date': datetime.datetime.utcnow()}
        self._insert_item(item, self.QUEUE)

    def close(self):
        self.con.close()
