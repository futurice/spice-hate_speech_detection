import os, sys

import sqlalchemy
from sqlalchemy import Column, BigInteger, Text, JSON

# Import all the custom libs and confs
sys.path.append('../confs')
import postgre_keys

class HateBase():
    db = None
    engine = None

    def __init__(self, connection_string=''):
        if connection_string == '':
            connection_string = postgre_keys.connection_string
        self.db = sqlalchemy.create_engine(connection_string)
        self.engine = self.db.connect()

    def get_tweets(self):
        table = sqlalchemy.table('tweets', Column('text', Text))
        statement = table.select()
        results = self.engine.execute(statement)
        tweets = results.fetchall()
        # TODO: There must be a more intelligent way to the get the first item
        # from each item in the list
        for i in range(0, len(tweets)):
            tweets[i] = tweets[i][0]
        return tweets

    def get_users_n_tweets(self):
        table = sqlalchemy.table('tweets', Column('screen_name', Text), Column('text', Text))
        statement = table.select()
        results = self.engine.execute(statement)
        rows = results.fetchall()
        # TODO: There must be a more intelligent way to the get the first item
        # from each item in the list
        tweets = [] #* len(rows)
        screen_names = [] #* len(rows)
        print(len(rows))
        for i in range(0, len(rows)):
            #print(len(rows[i]))
            screen_names.append(rows[i][0])
            tweets.append(rows[i][1])
        return screen_names, tweets
