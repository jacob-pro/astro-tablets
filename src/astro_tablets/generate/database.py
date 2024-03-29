import os
import sqlite3
from typing import List

from skyfield.timelib import Time

from astro_tablets.data import SUN, Body
from astro_tablets.generate.angular_separation import AngularSeparationResult
from astro_tablets.generate.eclipse import Eclipse, TimeUnit
from astro_tablets.generate.git_info import GitInfo
from astro_tablets.generate.lunar_calendar import VERNAL_EQUINOX, BabylonianDay
from astro_tablets.generate.planet_events import SynodicEvent
from astro_tablets.generate.risings_settings import RisingOrSetting


class Database:
    def __init__(self, file: str):
        directory = os.path.dirname(file)
        if not os.path.exists(directory) and len(directory) > 0:
            os.makedirs(directory)
        self.conn = sqlite3.connect(file, isolation_level=None)
        self.cursor = self.conn.cursor()
        self.setup()

    def setup(self):
        self.cursor.execute(
            """
        CREATE TABLE days (
            sunset FLOAT,
            sunrise FLOAT,
            first_visibility SMALLINT,
            year INT,
            PRIMARY KEY (sunset)
        );"""
        )
        self.cursor.execute(
            """
        CREATE TABLE events (
            body VARCHAR(255),
            event VARCHAR(255),
            time FLOAT,
            PRIMARY KEY (body, event, time)
        );"""
        )
        self.cursor.execute(
            """
        CREATE TABLE separations (
            from_body VARCHAR(255),
            to_body VARCHAR(255),
            angle FLOAT,
            position VARCHAR(255),
            time FLOAT,
            PRIMARY KEY (from_body, to_body, time)
        );"""
        )
        self.cursor.execute(
            """
        CREATE TABLE db_info (
            tablet VARCHAR(255),
            start_year INT,
            end_year INT,
            git_hash VARCHAR,
            git_dirty SMALLINT,
            time DATETIME DEFAULT CURRENT_TIMESTAMP
        );"""
        )
        self.cursor.execute(
            """
        CREATE TABLE lunar_eclipses (
            e_type VARCHAR(255),
            closest_approach_time FLOAT,
            partial_eclipse_begin FLOAT NULL,
            onset_us FLOAT,
            maximal_us FLOAT,
            clearing_us FLOAT,
            sum_us FLOAT,
            visible SMALLINT,
            PRIMARY KEY (closest_approach_time)
        );"""
        )
        self.cursor.execute(
            """
        CREATE TABLE risings_settings (
            r_type VARCHAR(255),
            time FLOAT,
            body VARCHAR(255),
            PRIMARY KEY (body, time, r_type)
        );"""
        )

    def close(self):
        self.cursor.close()
        self.conn.close()

    def save_synodic_events(self, body: str, events: List[SynodicEvent]):
        for e in events:
            self.cursor.execute(
                "INSERT INTO events (body, event, time) VALUES (?, ?, ?)",
                (body, e.type.value, e.time.tt),
            )

    def save_days(self, events: List[BabylonianDay]):
        for e in events:
            self.cursor.execute(
                "INSERT INTO days (sunset, sunrise, `year`, first_visibility) VALUES (?, ?, ?, ?)",
                (e.sunset.tt, e.sunrise.tt, int(e.sunset.utc.year), e.first_visibility),
            )

    def save_risings_settings(self, body: Body, events: List[RisingOrSetting]):
        for r in events:
            self.cursor.execute(
                "INSERT INTO risings_settings (r_type, time, body) VALUES (?, ?, ?)",
                (r.type.value, r.time.tt, body.name),
            )

    def save_equinox(self, time: Time):
        self.cursor.execute(
            "INSERT INTO events (body, event, time) VALUES (?, ?, ?)",
            (
                SUN.name,
                VERNAL_EQUINOX,
                time.tt,
            ),
        )

    def save_separation(
        self, of: Body, to: Body, res: AngularSeparationResult, time: Time
    ):
        self.cursor.execute(
            "INSERT INTO separations (from_body, to_body, angle, position, time) VALUES (?, ?, ?, ?, ?)",
            (of.name, to.name, res.angle.degrees, res.position.value, time.tt),
        )

    def save_lunar_eclipses(self, events: List[Eclipse]):
        for e in events:
            partial_eclipse_begin = (
                None if e.type == "Penumbral" else e.partial_eclipse_begin.tt
            )
            phases = e.phases(TimeUnit.DEGREE)
            self.cursor.execute(
                "INSERT INTO lunar_eclipses (e_type, closest_approach_time, partial_eclipse_begin, onset_us, "
                "maximal_us, clearing_us, sum_us, visible) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    e.type,
                    e.closest_approach_time.tt,
                    partial_eclipse_begin,
                    phases.onset,
                    phases.maximal,
                    phases.clearing,
                    phases.sum,
                    e.visibility_in_babylon(),
                ),
            )

    def save_info(self, tablet: str, start: int, end: int):
        git = GitInfo()
        self.cursor.execute(
            "INSERT INTO db_info (tablet, start_year, end_year, git_hash, git_dirty) VALUES (?, ?, ?, ?, ?)",
            (tablet, start, end, git.hash, git.dirty),
        )
