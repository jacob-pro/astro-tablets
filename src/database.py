import sqlite3
import os

from skyfield.timelib import Time

from planet_events import SynodicEvent
from typing import *


class Database(object):

    def __init__(self, file: str):
        directory = os.path.dirname(file)
        if not os.path.exists(directory):
            os.makedirs(directory)
        self.conn = sqlite3.connect(file, isolation_level=None)
        self.cursor = self.conn.cursor()
        self.setup()

    def setup(self):
        self.cursor.execute("""
        CREATE TABLE calendar (
            sunset FLOAT,
            sunrise FLOAT,
            first_visibility SMALLINT,
            PRIMARY KEY (sunset)
        );""")
        self.cursor.execute("""
        CREATE TABLE events (
            body VARCHAR(255),
            event VARCHAR(255),
            time FLOAT,
            PRIMARY KEY (body, event, time)
        );""")
        self.cursor.execute("""
        CREATE TABLE separations (
            from_body VARCHAR(255),
            to_body VARCHAR(255),
            angle FLOAT,
            position VARCHAR(255),
            time FLOAT,
            PRIMARY KEY (from_body, to_body, time)
        );""")

    def close(self):
        self.cursor.close()
        self.conn.close()

    def save_synodic_events(self, body: str, events: List[SynodicEvent]):
        for e in events:
            self.cursor.execute("INSERT INTO events (body, event, time) VALUES (?, ?, ?)",
                                (body, e.type.value, e.time.tt))

    def save_equinox(self, time: Time):
        self.cursor.execute("INSERT INTO events (body, event, time) VALUES ('Sun', 'VernalEquinox', ?)",
                            (time.tt, ))
