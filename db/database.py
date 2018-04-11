from pymongo import MongoClient

DB_NAME = 'soccer-prediction'
MATCHES_COLLECTION_NAME = 'matches'
CLASSIFICATION_HISTORY_COLLECTION_NAME = 'rankings'


class DAO:
    def __init__(self):
        client = MongoClient()
        db = client[DB_NAME]
        self.matches_collection = db[MATCHES_COLLECTION_NAME]
        self.classification_history = db[CLASSIFICATION_HISTORY_COLLECTION_NAME]

    def add_round_classification(self, classification_table):
        self.classification_history.insert_one(classification_table)

    def add_match(self, match):
        self.matches_collection.insert_one(match)
