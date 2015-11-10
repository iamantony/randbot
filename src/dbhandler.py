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
            key TEXT NOT NULL UNIQUE,
            secret TEXT NOT NULL UNIQUE)''')

        cursor.execute('''CREATE TABLE token (
            id INTEGER PRIMARY KEY NOT NULL,
            key TEXT NOT NULL UNIQUE,
            secret TEXT NOT NULL UNIQUE)''')

        cursor.execute('''CREATE TABLE users (
            id INTEGER PRIMARY KEY NOT NULL,
            user_id TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL UNIQUE,
            number TEXT NOT NULL UNIQUE)''')

        cursor.execute('''CREATE TABLE last_msg (
            id INTEGER PRIMARY KEY NOT NULL,
            msg_id TEXT NOT NULL UNIQUE)''')

        connection.commit()
        connection.close()

    def __check_consumer_data(self):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM consumer LIMIT 1')
        if cursor.fetchone() is None:
            key, secret = self.__request_consumer_data()
            cursor.execute('INSERT INTO consumer VALUES (null, ?, ?)',
                           (key, secret))
            self.connection.commit()

    def __request_consumer_data(self):
        print('Please enter consumer data of twitter application.')
        key = input('Consumer key: ')
        secret = input('Consumer secret: ')
        return key, secret

    def get_consumer_data(self):
        cursor = self.connection.cursor()
        cursor.execute('SELECT key, secret FROM consumer LIMIT 1')
        return cursor.fetchone()

    def __check_token_data(self):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM token LIMIT 1')
        if cursor.fetchone() is None:
            key, secret = self.__request_token_data()
            cursor.execute('INSERT INTO token VALUES (null, ?, ?)',
                           (key, secret))
            self.connection.commit()

    def __request_token_data(self):
        print('Please enter access token data of twitter application.')
        key = input('Access Token: ')
        secret = input('Access Token secret: ')
        return key, secret

    def get_access_token_data(self):
        cursor = self.connection.cursor()
        cursor.execute('SELECT key, secret FROM token LIMIT 1')
        return cursor.fetchone()

    def get_last_msg_id(self):
        cursor = self.connection.cursor()
        cursor.execute('SELECT msg_id FROM last_msg LIMIT 1')
        data = cursor.fetchone()
        if data is None:
            return None

        return data[0]

    def set_last_msg_id(self, new_id):
        if new_id is None or len(new_id) == 0:
            print("Invalid ID of last message:", new_id)
            return

        cursor = self.connection.cursor()
        if self.get_last_msg_id() is None:
            cursor.execute('INSERT INTO last_msg VALUES (null, ?)', (new_id,))
        else:
            cursor.execute('UPDATE last_msg SET msg_id=? WHERE id=0', (new_id,))

        self.connection.commit()

    def get_user_data(self, user_id):
        if user_id is None or len(user_id) == 0:
            print("Invalid user ID:", user_id)
            return None

        cursor = self.connection.cursor()
        cursor.execute('SELECT name, number FROM users WHERE user_id=?',
                       (user_id,))

        data = cursor.fetchone()
        if data is None:
            print("There is no info in database about user with ID:", user_id)
            return None

        user_data = {'user_id': user_id, 'name': data[0], 'number': data[1]}
        return user_data

    def add_user(self, user_data):
        if self.get_user_data(user_data['user_id']) is not None:
            print("User with ID {0} already exist in database".format(
                user_data['user_id']))
            return

        cursor = self.connection.cursor()
        cursor.execute('INSERT INTO users VALUES (null, ?, ?, ?))',
                       (user_data['user_id'], user_data['name'],
                        user_data['number']))
        self.connection.commit()
