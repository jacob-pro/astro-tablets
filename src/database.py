import sqlite3
import os


class Database(object):

    def __init__(self, file: str):
        directory = os.path.dirname(file)
        if not os.path.exists(directory):
            os.makedirs(directory)
        self.conn = sqlite3.connect(file)

    def close(self):
        self.conn.close()
