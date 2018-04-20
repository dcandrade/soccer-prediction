from pymongo import MongoClient

DB_NAME = 'soccer-prediction'
MATCHES_COLLECTION_NAME = 'matches'
CLASSIFICATION_HISTORY_COLLECTION_NAME = 'rankings'


class DAO:
    def __init__(self):
        __client = MongoClient()
        db = __client[DB_NAME]
        self.__matches = db[MATCHES_COLLECTION_NAME]
        self.classification_history = db[CLASSIFICATION_HISTORY_COLLECTION_NAME]

    def add_match(self, match):
        self.__matches.insert_one(match)
    
    # Gets the last N balances of a team per match 
    # The results are sorted from the most recent to the oldest match result
    def get_last_N_balances(self, team, limit):
        query_constraints = {'$or':[ {'away_team':team}, {'home_team':team}]}
        query_projections = {'home_team':1, 'away_team':1, 'year':1, 'round':1, 'score':1, 'teams': 1}
        query_sort_criteria = [('year',-1), ('round',-1)]

        matches = self.__matches.find(query_constraints, query_projections)\
                                    .sort(query_sort_criteria)\
                                    .limit(limit)
        sgs =[]
        for match in matches:
            score = match['score']
            is_home = team == match['home_team']
            
            if is_home:
                sg = score['home_team'] - score['away_team']
            else:
                sg = score['away_team'] - score['home_team']
            sgs.append(sg)
        
        return sgs

    def matches(self):
        return self.__matches
    
    def from_year(self, year):
        return self.__matches.find({
            'year': year
        })