import sqlite3


class Database:

    def __init__(self, file: str):
        self.conn = sqlite3.connect(file, isolation_level=None)
