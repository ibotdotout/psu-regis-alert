import pymongo


class DbConnection():
    def __init__(self):
        dbHost = 'mongodb://localhost:27017'
        dbName = 'psuRegisAlert'
        dbCollection = 'queue'
        dbUsedCollection = 'used'

        connection = pymongo.MongoClient(dbHost)
        self.db = connection[dbName][dbCollection]
        self.db_used = connection[dbName][dbUsedCollection]

    def query_last_item(self):
        dbCursor = self.db.find().sort('_id', -1).limit(1)
        if dbCursor and dbCursor.count() > 0:
            return dbCursor[0]

    def query_all(self):
        dbCursor = self.db.find().sort('_id', -1)
        if dbCursor and dbCursor.count() > 0:
            return dbCursor

    def remove(self, item):
        self._insert_used_item(item)
        self.db.remove(item)

    def _insert_used_item(self, item):
        self.db_used.insert(item)

    def insert_item(self, subject_code, email):
        item = {}
        item['subject_code'] = subject_code
        item['email'] = email
        self.db.insert(item)
