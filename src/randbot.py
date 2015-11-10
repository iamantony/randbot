__author__ = 'Antony Cherepanov'

import tweepy
from src import dbhandler
from src import generator


class RandBot(object):
    def __init__(self):
        self.db = dbhandler.DBHandler()
        self.auth = tweepy.OAuthHandler(*(self.db.get_consumer_data()))
        self.auth.set_access_token(*(self.db.get_access_token_data()))
        self.api = tweepy.API(self.auth)

    def run(self):
        public_tweets = self.api.home_timeline()
        for tweet in public_tweets:
            print(tweet.text)

if __name__ == '__main__':
    print("Start RandBot")
    bot = RandBot()
    bot.run()
