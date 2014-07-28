import pymongo


class DbConnection():
    def __init__(self):
        dbHost = 'mongodb://localhost:27017'
        dbName = 'psuRegisAlert'
        dbCollection = 'queue'

        connection = pymongo.MongoClient(dbHost)
        self.db = connection[dbName][dbCollection]

    def query_last_item(self):
        dbCursor = self.db.find().sort('_id', -1).limit(1)
        if not dbCursor and dbCursor.count() > 0:
            return dbCursor[0]

    def insert_item(self, subject_code, email):
        item = {}
        item['subject_code'] = subject_code
        item['email'] = email
        print subject_code, email
        self.db.insert(item)