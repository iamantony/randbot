__author__ = 'Antony Cherepanov'

import sqlite3
import os


class DBHandler(object):
    def __init__(self):
        self.db_name = 'bot.db'
        self.__check_db()
        self.connection = sqlite3.connect(self.db_name)
        self.__check_consumer_data()
        self.__check_token_data()

    def __check_db(self):
        if os.path.exists(self.db_name):
            return

        print("Database do not exist")
        self.__init_db()

    def __init_db(self):
        print("Database initialisation")
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute('''CREATE TABLE consumer (
            id INTEGER PRIMARY KEY NOT NULL,
            key TEXT NOT NULL,
            secret TEXT NOT NULL)''')

        cursor.execute('''CREATE TABLE token (
            id INTEGER PRIMARY KEY NOT NULL,
            key TEXT NOT NULL,
            secret TEXT NOT NULL)''')

        cursor.execute('''CREATE TABLE users (
            id INTEGER PRIMARY KEY NOT NULL,
            name TEXT NOT NULL,
            number TEXT NOT NULL)''')

        connection.commit()
        connection.close()

    def __check_consumer_data(self):
        cursor = self.connection.cursor()
        id = ('0',)
        cursor.execute('SELECT * FROM consumer WHERE id=?', id)
        if cursor.fetchone() is None:
            key, secret = self.__request_consumer_data()
            cursor.execute('INSERT INTO consumer VALUES (?, ?, ?)',
                           (0, key, secret))
            self.connection.commit()

    def __request_consumer_data(self):
        print('Please enter consumer data of twitter application.')
        key = input('Consumer key: ')
        secret = input('Consumer secret: ')
        return key, secret

    def get_consumer_data(self):
        cursor = self.connection.cursor()
        id = ('0',)
        cursor.execute('SELECT * FROM consumer WHERE id=?', id)
        data = cursor.fetchone()
        return data[1], data[2]

    def __check_token_data(self):
        cursor = self.connection.cursor()
        id = ('0',)
        cursor.execute('SELECT * FROM token WHERE id=?', id)
        if cursor.fetchone() is None:
            key, secret = self.__request_token_data()
            cursor.execute('INSERT INTO token VALUES (?, ?, ?)',
                           (0, key, secret))
            self.connection.commit()

    def __request_token_data(self):
        print('Please enter access token data of twitter application.')
        key = input('Access Token: ')
        secret = input('Access Token secret: ')
        return key, secret

    def get_access_token_data(self):
        cursor = self.connection.cursor()
        id = ('0',)
        cursor.execute('SELECT * FROM token WHERE id=?', id)
        data = cursor.fetchone()
        return data[1], data[2]
