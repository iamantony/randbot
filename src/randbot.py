__author__ = 'Antony Cherepanov'

import tweepy
from src import dbhandler
from src import generator


class RandBot(object):
    def __init__(self):
        self.tweets = list()
        self.db = dbhandler.DBHandler()
        self.auth = tweepy.OAuthHandler(*(self.db.get_consumer_data()))
        self.auth.set_access_token(*(self.db.get_access_token_data()))
        self.api = tweepy.API(self.auth)

    def run(self):
        self.__process_last_mentions()
        self.__process_search()
        self.__send_tweets()

    def __process_last_mentions(self):
        mentions = list()
        msg_id = self.db.get_last_msg_id()
        if msg_id is None:
            mentions = self.api.mentions_timeline(count=10)
        else:
            mentions = self.api.mentions_timeline(since_id=msg_id, count=10)

        for tweet in mentions:
            print(tweet.text)
            user_data = self.db.get_user_data(tweet.author.id_str)
            if user_data is None:
                self.__process_new_user(tweet)
            else:
                self.tweets.append("Your number, @{0}, is {1}".format(
                    user_data['name']), user_data['number'])

    def __process_new_user(self, tweet):
        if tweet is None:
            print("Invalid tweet - it is empty!")
            return

        gen = generator.Generator()
        number = gen.generate(tweet)
        if number is None:
            return

        # user_id = tweet.author.id_str
        user_name = tweet.author.screen_name
        # user_data = {'user_id': user_id, 'name': user_name, 'number': number}
        # self.db.add_user(user_data)

        self.tweets.append("Hi @{0}. I have a number for you: {1}".format(
            user_name, number))

    def __process_search(self):
        pass

    def __send_tweets(self):
        for tweet in self.tweets:
            print(tweet)

if __name__ == '__main__':
    print("Start RandBot")
    bot = RandBot()
    bot.run()
