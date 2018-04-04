from pymongo import MongoClient

DBNAME = 'brazilian-championship-prediction'
MATCHES_COLLECTION_NAME = 'matches'
CLASSIFICATION_HISTORY_COLLECTION_NAME = 'classification_history'


class DAO:
    def __init__(self):
        client = MongoClient()
        db = client[DBNAME]
        self.matches_collection = db[MATCHES_COLLECTION_NAME]
        self.classification_history = db[CLASSIFICATION_HISTORY_COLLECTION_NAME]

    def add_round_classification(self, classification_table):
        self.classification_history.insert(classification_table)

    def add_match(self, match):
        self.matches_collection.insert(match)
