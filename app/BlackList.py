from pymongo import MongoClient

class BlackList:
    def __init__(self, db_name='test_db', collection_name='test_collection'):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client[db_name]
        self.black_list_collection = self.db["black_list"]
        self.collection = self.db[collection_name]

    def add_account_to_black_list(self, pesel, reason):
        self.black_list_collection.insert_one({'pesel': pesel, 'reason': reason})

    def is_account_on_black_list(self, pesel):
        return self.black_list_collection.find_one({'pesel': pesel}) is not None

    def close(self):
        self.client.close()