import sqlite3
from abc import ABC
from skyfield.timelib import Time

from data import TimeData


class Result(ABC):

    def __init__(self, comment: str, passed: bool):
        self.comment = comment
        self.passed = passed


class PlanetPhenomenaResult(Result):

    def __init__(self, comment: str, passed: bool, expected_time: Time, nearest_time: Time, planet: str, event: str):
        super(Result, self).__init__(comment, passed)
        self.expected_time = expected_time
        self.nearest_time = nearest_time
        self.planet = planet
        self.event = event

    @staticmethod
    def test(conn: sqlite3.Connection, time_data: TimeData, comment: str, expected_time: float, planet: str, event: str):
        cursor = conn.cursor()
        cursor.execute(""" 
        SELECT time FROM events WHERE body=? AND event=? ORDER BY ABS(time - ?) DESC LIMIT 1""",
                       (planet, event, expected_time,))
        cursor.fetchone()

        pass


class SeparationResult(Result):
    pass
