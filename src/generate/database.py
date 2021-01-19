import os
import sqlite3
from typing import *

from skyfield.timelib import Time

from generate.angular_separation import AngularSeparationResult
from generate.lunar_calendar import BabylonianDay
from generate.planet_events import SynodicEvent
from util import get_git_hash, get_git_changes


class Database(object):

    def __init__(self, file: str):
        directory = os.path.dirname(file)
        if not os.path.exists(directory) and len(directory) > 0:
            os.makedirs(directory)
        self.conn = sqlite3.connect(file, isolation_level=None)
        self.cursor = self.conn.cursor()
        self.setup()

    def setup(self):
        self.cursor.execute("""
        CREATE TABLE days (
            sunset FLOAT,
            sunrise FLOAT,
            first_visibility SMALLINT,
            year INT,
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
        self.cursor.execute("""
        CREATE TABLE db_info (
            tablet VARCHAR(255),
            start_year INT,
            end_year INT,
            git VARCHAR,
            time DATETIME DEFAULT CURRENT_TIMESTAMP
        );""")

    def close(self):
        self.cursor.close()
        self.conn.close()

    def save_synodic_events(self, body: str, events: List[SynodicEvent]):
        for e in events:
            self.cursor.execute("INSERT INTO events (body, event, time) VALUES (?, ?, ?)",
                                (body, e.type.value, e.time.tt))

    def save_days(self, events: List[BabylonianDay]):
        for e in events:
            self.cursor.execute("INSERT INTO days (sunset, sunrise, `year`, first_visibility) VALUES (?, ?, ?, ?)",
                                (e.sunset.tt, e.sunrise.tt, int(e.sunset.utc.year), e.first_visibility))

    def save_equinox(self, time: Time):
        self.cursor.execute("INSERT INTO events (body, event, time) VALUES ('Sun', 'VernalEquinox', ?)",
                            (time.tt, ))

    def save_separation(self, of: str, to: str, res: AngularSeparationResult, time: Time):
        self.cursor.execute("INSERT INTO separations (from_body, to_body, angle, position, time) VALUES (?, ?, ?, ?, ?)",
                            (of, to, res.angle.degrees, res.position.value, time.tt))

    def save_info(self, tablet: str, start: int, end: int):
        hash = get_git_hash()
        if hash is not None:
            if get_git_changes():
                hash = hash + " (modified)"
        self.cursor.execute("INSERT INTO db_info (tablet, start_year, end_year, git) VALUES (?, ?, ?, ?)",
                            (tablet, start, end, hash))
