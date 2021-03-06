import unittest
import mock
import db_connection


class DbConnectionTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.queue = db_connection.DbConnection.QUEUE
        cls.used = db_connection.DbConnection.USED
        cls.db_name = db_connection.DbConnection.DB_NAME
        cls.subject_code = "xxx-xxx"
        cls.date = "xxx"
        cls.email = "test@hellotest.com"
        cls.line_id = "psuregisalert"
        cls.sec = "01,02,10"
        cls.url = "http://sis.psu.ac.th"
        cls.item = {
            'url': cls.url,
            'subject_code': cls.subject_code,
            'date': cls.date,
            'line_id': cls.line_id,
            'email': cls.email,
            'sec': cls.sec}
        cls.key_item = {
            'url': cls.url,
            'subject_code': cls.subject_code,
            'line_id': cls.line_id,
            'email': cls.email,
            'sec': cls.sec}

    def helper_assert_args_mock(self, mock_obj, args_list):
        args = [i for name, args, kwargs in mock_obj.mock_calls for i
                in args if isinstance(i, str)]
        self.assertEqual(args_list, args)

    def helper_get_db_collection(self, mock_obj):
        return mock_obj.__getitem__().__getitem__()

    def query_decorate(args_db):
        def wrap(func):
            @mock.patch('pymongo.MongoClient')
            def test_func_wrapper(self, mock_mongo):
                # assign
                mock_db = mock_mongo.return_value = mock.MagicMock()
                mock_collection = self.helper_get_db_collection(mock_db)
                mock_collection.remove = mock.Mock()

                # arrange
                func(self)

                # assert
                self.helper_assert_args_mock(mock_db, args_db)
                mock_collection.find.assert_called_once_with()
            return test_func_wrapper
        return wrap

    def helper_mock_db(self, mock_datetime, mock_mongo):
        # assign
        mock_datetime.utcnow.return_value = self.date

        mock_db = mock_mongo.return_value = mock.MagicMock()
        mock_collection = self.helper_get_db_collection(mock_db)

        return (mock_db, mock_collection)

    @mock.patch('pymongo.MongoClient')
    @mock.patch('datetime.datetime')
    def test_insert_item(self, mock_datetime, mock_mongo):
        # assgin
        args_db = [self.db_name, self.queue]

        mock_db, mock_collection = \
            self.helper_mock_db(mock_datetime, mock_mongo)

        # arrange
        db = db_connection.DbConnection()
        db.insert_item(
            self.url,
            self.subject_code,
            self.email,
            self.line_id,
            self.sec)

        # assert
        self.helper_assert_args_mock(mock_db, args_db)

        # mock_collection.insert.assert_called_once_with(self.item)
        # using upsert instead of insert
        mock_collection.update.assert_called_once_with(self.key_item,
                                                       self.item, upsert=True)

    @mock.patch('pymongo.MongoClient')
    @mock.patch('datetime.datetime')
    def test_remove(self, mock_datetime, mock_mongo):
        # assgin
        args_db = [self.db_name, self.queue, self.used]
        achived_item = self.item.copy()
        achived_item['achived_date'] = self.date

        achived_key = self.key_item.copy()
        achived_key['achived_date'] = self.date

        mock_db, mock_collection = \
            self.helper_mock_db(mock_datetime, mock_mongo)

        # arrange
        db = db_connection.DbConnection()
        db.remove(self.item)

        # assert
        self.helper_assert_args_mock(mock_db, args_db)
        mock_collection.remove.assert_called_once_with(self.item)
        # mock_collection.insert.assert_called_once_with(achived_item)

        # using upsert instead of insert
        mock_collection.update.assert_called_once_with(achived_key,
                                                       achived_item,
                                                       upsert=True)

    @query_decorate([db_connection.DbConnection.DB_NAME,
                     db_connection.DbConnection.QUEUE])
    def test_query_queue_all(self):
        # arrange
        db = db_connection.DbConnection()
        db.query_queue_all()

    @query_decorate([db_connection.DbConnection.DB_NAME,
                     db_connection.DbConnection.USED])
    def test_query_used_all(self):
        # arrange
        db = db_connection.DbConnection()
        db.query_used_all()
