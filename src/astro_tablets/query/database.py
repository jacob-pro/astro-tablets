import os
import sqlite3
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from dataclass_wizard import JSONWizard

from astro_tablets.constants import MAX_NISAN_EQUINOX_DIFF_DAYS, Body
from astro_tablets.data import MOON, SUN
from astro_tablets.generate.lunar_calendar import VERNAL_EQUINOX
from astro_tablets.generate.risings_settings import RiseSetType


@dataclass
class BabylonianDay(JSONWizard):
    sunset: float
    sunrise: float


@dataclass
class DbInfo(JSONWizard):
    tablet: str
    start_year: int
    end_year: int
    time: str


@dataclass
class LunarEclipse(JSONWizard):
    e_type: str
    closest_approach_time: float
    partial_eclipse_begin: Optional[float]
    onset_us: float
    maximal_us: float
    clearing_us: float
    sum_us: float
    visible: bool
    angle: Optional[float]
    position: Optional[str]
    sunset: float
    sunrise: float


@dataclass
class PotentialYear(JSONWizard):
    nisan_1: float
    year: int


@dataclass
class Separation(JSONWizard):
    angle: float
    position: str
    time: float


@dataclass
class Event(JSONWizard):
    body: str
    event: str
    time: float


class Database:
    def __init__(self, file_path: str):
        if not os.path.isfile(file_path):
            raise RuntimeError(f"Database file {file_path} not found")
        self.conn = sqlite3.connect(
            "file:{}?mode=ro".format(file_path), isolation_level=None, uri=True
        )
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM db_info")
        self.info = DbInfo.from_dict(self.fetch_one(cursor))

    def get_days(self, month_sunset_1: float) -> List[BabylonianDay]:
        """
        Get days in a given month
        @param month_sunset_1: The time of sunset on the first day of the month
        @return A List of days
        """
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT sunset, sunrise FROM days WHERE sunset >= ? ORDER BY sunset LIMIT 32",
            (month_sunset_1,),
        )
        res = list(map(BabylonianDay.from_dict, self.fetch_all(cursor)))
        assert res[0].sunset == month_sunset_1
        return res

    def get_months(self, nisan_1_sunset: float, count=13) -> List[float]:
        """
        Get a list of months for a given Nisan I sunset time
        @param nisan_1_sunset: The time of sunset on the first day of the year
        @param count:
        @return: List of the sunset times that each month would begin at
        """
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT sunset FROM days WHERE days.first_visibility==1 AND sunset >= ? ORDER BY sunset LIMIT ?""",
            (nisan_1_sunset, count),
        )
        res = cursor.fetchall()
        res = list(map(lambda x: x[0], res))
        assert res[0] == nisan_1_sunset
        return res

    def get_months_in_year(self, year: int) -> List[float]:
        """
        Get a list of month dates within a Julian year
        @param year: The Julian year to fetch months for
        @return: List of the sunset times that each month would begin at
        """
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT sunset FROM days WHERE days.first_visibility==1 AND year = ? ORDER BY sunset""",
            (year,),
        )
        res = cursor.fetchall()
        res = list(map(lambda x: x[0], res))
        return res

    def get_years(self) -> List[List[PotentialYear]]:
        """
        Gets a list of potential years from the database
        A year may at one of 2 to 3 different lunar visibilities, within ~30 days of vernal equinox
        @return List of potential years, grouped into sub-arrays for each year, in ascending order
        """
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT days.sunset as nisan_1, days.year as year
            FROM events equinox
            INNER JOIN days
            ON days.sunset >= (equinox.time - ?) and days.sunset <= (equinox.time + ?) and days.first_visibility==1
            WHERE equinox.event=? and equinox.body=?
            AND days.year <= (SELECT end_year FROM db_info LIMIT 1)""",
            (
                MAX_NISAN_EQUINOX_DIFF_DAYS,
                MAX_NISAN_EQUINOX_DIFF_DAYS,
                VERNAL_EQUINOX,
                SUN.name,
            ),
        )
        res = list(map(PotentialYear.from_dict, self.fetch_all(cursor)))
        output: List[List[PotentialYear]] = [[]]
        current_year = res[0].year
        for y in res:
            if current_year == y.year:
                output[len(output) - 1].append(y)
            else:
                current_year = y.year
                output.append([y])
        return output

    def nearest_event_match_to_time(
        self, body: Body, event: str, time: float
    ) -> Optional[float]:
        cursor = self.conn.cursor()
        cursor.execute(
            """SELECT time FROM events WHERE body=? AND event=? ORDER BY ABS(time - ?) LIMIT 1""",
            (
                body.name,
                event,
                time,
            ),
        )
        result = self.fetch_one(cursor)
        if result is not None:
            return result["time"]
        return None

    def get_events_in_range(
        self, body: str, start_time: float, end_time: float
    ) -> List[Event]:
        cursor = self.conn.cursor()
        cursor.execute(
            """SELECT body, event, time FROM events WHERE body=? AND time >= ? AND time <= ? ORDER BY time""",
            (body, start_time, end_time),
        )
        return list(map(Event.from_dict, self.fetch_all(cursor)))

    def separations_in_range(
        self, from_body: Body, to_body: Body, start_time: float, end_time: float
    ) -> List[Separation]:
        cursor = self.conn.cursor()
        cursor.execute(
            """SELECT angle, position, time FROM separations
            WHERE from_body=? AND to_body=? AND time >= ? AND time <= ?""",
            (from_body.name, to_body.name, start_time, end_time),
        )
        return list(map(Separation.from_dict, self.fetch_all(cursor)))

    def lunar_eclipses_in_range(
        self, start_time: float, end_time: float, position_body: Optional[Body]
    ) -> List[LunarEclipse]:
        if position_body is not None:
            body = position_body.name
        else:
            body = None
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT e_type, closest_approach_time, partial_eclipse_begin, onset_us,
            maximal_us, clearing_us, sum_us, visible, angle, position
            FROM lunar_eclipses e
            LEFT JOIN separations s
            ON s.time == e.closest_approach_time AND s.to_body == ? AND s.from_body == ?
            WHERE (closest_approach_time >= ? AND closest_approach_time <= ?)""",
            (body, MOON.name, start_time, end_time),
        )
        eclipses = self.fetch_all(cursor)
        for e in eclipses:
            e["sunset"] = self.nearest_sunset(e["closest_approach_time"])
            e["sunrise"] = self.nearest_sunrise(e["closest_approach_time"])
        return list(map(LunarEclipse.from_dict, eclipses))

    def nearest_sunset(self, time: float) -> float:
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT sunset FROM days d ORDER BY ABS(d.sunset - ?) LIMIT 1""",
            (time,),
        )
        res = self.fetch_one(cursor)
        return res["sunset"]

    def nearest_sunrise(self, time: float) -> float:
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT sunrise FROM days d ORDER BY ABS(d.sunrise - ?) LIMIT 1""",
            (time,),
        )
        res = self.fetch_one(cursor)
        return res["sunrise"]

    def nearest_rising_setting(self, body: Body, r: RiseSetType, time: float) -> float:
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT time FROM risings_settings WHERE body == ? AND r_type == ? ORDER BY ABS(time - ?) LIMIT 1""",
            (body.name, r.value, time),
        )
        res = self.fetch_one(cursor)
        return res["time"]

    @staticmethod
    def fetch_all(cursor: sqlite3.Cursor) -> List[Dict[str, Any]]:
        """
        Fetches all rows from a cursor
        @param cursor: The cursor to fetch from
        @return: A List of rows, where each row is Dict of column names to values
        """
        columns = [col[0] for col in cursor.description]
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return rows

    @staticmethod
    def fetch_one(cursor: sqlite3.Cursor) -> Dict[str, Any]:
        """
        Fetches one row from a cursor
        @param cursor: The cursor to fetch from
        @return: A Dict of column names to values
        """
        columns = [col[0] for col in cursor.description]
        return dict(zip(columns, cursor.fetchone()))
