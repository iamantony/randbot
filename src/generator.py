__author__ = 'Antony Cherepanov'

import random


class Generator(object):
    def __init__(self):
        self.length = 16

    def generate(self, tweet):
        if tweet is None:
            print("Can't generate number from empty tweet")
            return None

        number = tweet.author.id_str
        chars = list(tweet.author.screen_name)
        for c in chars:
            number += "{0:X}".format(ord(c))

        number_elements = list(number)
        random.shuffle(number_elements)

        if len(number_elements) > self.length:
            number_elements = number_elements[0:self.length]

        while len(number_elements) < self.length:
            number_elements.append(str(random.randint(0, 9)))

        number_elements.insert(3, '-')
        number_elements.insert(8, '-')
        number_elements.insert(13, '-')
        return ''.join(number_elements)
