__author__ = 'Antony Cherepanov'

import os
from datetime import datetime
import random
import tweepy
import dbhandler
import generator


class RandBot(object):
    def __init__(self):
        self.db = dbhandler.DBHandler()
        self.auth = tweepy.OAuthHandler(*(self.db.get_consumer_data()))
        self.auth.set_access_token(*(self.db.get_access_token_data()))
        self.api = tweepy.API(self.auth)

    def run(self):
        self.__process_last_mentions()
        self.__process_search()

    def __process_last_mentions(self):
        print("Processing mentions")

        mentions = list()
        last_msg_id = self.db.get_last_msg_id()
        if last_msg_id is None:
            mentions = self.api.mentions_timeline(count=10)
        else:
            mentions = self.api.mentions_timeline(since_id=last_msg_id,
                                                  count=10)

        mentions.reverse()
        for tweet in mentions:
            user_data = self.db.get_user_data(tweet.author.id_str)
            if user_data is None:
                self.__process_new_user(tweet)
            else:
                msg = "@{0} your random number is {1}".format(
                    user_data['name'], user_data['number'])

                print("Replying to user: {0}".format(msg))
                self.__send_tweet(
                    self.__create_tweet_struct(tweet.id_str, msg))

            self.db.set_last_msg_id(tweet.id_str)

    def __create_tweet_struct(self, reply_id, text):
        return {'id': reply_id, 'tweet': text}

    def __process_new_user(self, tweet):
        if tweet is None:
            print("Invalid tweet - it is empty!")
            return

        gen = generator.Generator()
        number = gen.generate(tweet)
        if number is None:
            return

        user_name = tweet.author.screen_name
        msg = "@{0} hi! I'm a randbot and I have a random number for you: {1}".format(
            user_name, number)

        print("Adding new user: {0}".format(msg))
        self.__send_tweet(self.__create_tweet_struct(tweet.id_str, msg))

        user_data = {'user_id': tweet.author.id_str, 'name': user_name,
                     'number': number}
        self.db.add_user(user_data)

    def __process_search(self):
        print("Processing search")

        keyword = 'random'
        query = '{0} OR #{0}'.format(keyword)
        results = self.api.search(q=query, result_type='mixed', count=100)

        filtered_results = list()
        authors = list()
        for tweet in results:
            if keyword in tweet.text and \
                    tweet.author.id_str not in authors and \
                    self.db.get_user_data(tweet.author.id_str) is None:
                filtered_results.append(tweet)
                authors.append(tweet.author.id_str)

        index = random.randint(0, len(filtered_results) - 1)
        self.__process_new_user(filtered_results[index])

    def __send_tweet(self, msg):
        return self.api.update_status(status=msg['tweet'],
                                      in_reply_to_status_id=msg['id'])

if __name__ == '__main__':
    print("Start RandBot at " + str(datetime.today()))
    bot = RandBot()
    bot.run()
    print("Done")
    print()
