import sqlite3
from dataclasses import dataclass
from typing import *

from astro_tablets.constants import MAX_NISAN_EQUINOX_DIFF_DAYS, Body
from astro_tablets.data import SUN, MOON
from astro_tablets.generate.lunar_calendar import VERNAL_EQUINOX
from astro_tablets.generate.risings_settings import RiseSetType
from astro_tablets.util import array_group_by


@dataclass
class BabylonianDay:
    sunset: float
    sunrise: float


class Database:

    def __init__(self, file: str):
        self.conn = sqlite3.connect("file:{}?mode=ro".format(file), isolation_level=None, uri=True)
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM db_info")
        res = self.fetch_one_as_dict(cursor)
        print("Opened database generated on {} for {} covering {} to {}"
              .format(res['time'], res['tablet'], res['start_year'], res['end_year']))
        self.tablet_name = res['tablet']

    def get_days(self, month_sunset_1: float) -> List[BabylonianDay]:
        """
        Get days in a given month
        @param month_sunset_1: The time of sunset on the first day of the month
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT sunset, sunrise FROM days WHERE sunset >= ? ORDER BY sunset LIMIT 32",
                       (month_sunset_1,))
        res = cursor.fetchall()
        res = list(map(lambda x: BabylonianDay(*x), res))
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
        cursor.execute("""
            SELECT sunset FROM days WHERE days.first_visibility==1 AND sunset >= ? ORDER BY sunset LIMIT ?""",
                       (nisan_1_sunset, count))
        res = cursor.fetchall()
        res = list(map(lambda x: x[0], res))
        assert res[0] == nisan_1_sunset
        return res

    def get_years(self) -> OrderedDict:
        """
        Gets a list of years from the database
        The key will be the year number e.g. -600
        And the value will be a list of possible Nisan Is for that year
        i.e. each year may possibly start at one of 2 to 3 different lunar visibilities, within 30 days of equinox
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT days.sunset as nisan_1, days.year as year
            FROM events equinox
            INNER JOIN days 
            ON days.sunset >= (equinox.time - ?) and days.sunset <= (equinox.time + ?) and days.first_visibility==1
            WHERE equinox.event=? and equinox.body=?
            AND days.year <= (SELECT end_year FROM db_info LIMIT 1)""",
                       (MAX_NISAN_EQUINOX_DIFF_DAYS, MAX_NISAN_EQUINOX_DIFF_DAYS, VERNAL_EQUINOX, SUN.name, ))
        res = self.fetch_all_as_dict(cursor)
        return array_group_by(res, lambda x: x["year"])

    def nearest_event_match_to_time(self, body: Body, event: str, time: float) -> Optional[float]:
        cursor = self.conn.cursor()
        cursor.execute("""SELECT time FROM events WHERE body=? AND event=? ORDER BY ABS(time - ?) LIMIT 1""",
                       (body.name, event, time,))
        result = cursor.fetchone()
        if result is not None:
            return result[0]
        return None

    def separations_in_range(self, from_body: Body, to_body: Body, start_time: float, end_time: float) -> List[Dict]:
        cursor = self.conn.cursor()
        cursor.execute("""SELECT angle, position, time FROM separations 
            WHERE from_body=? AND to_body=? AND time >= ? AND time <= ?""",
                       (from_body.name, to_body.name, start_time, end_time))
        return self.fetch_all_as_dict(cursor)

    def lunar_eclipses_in_range(self, start_time: float, end_time: float, position_body: Optional[Body]) -> List[Dict]:
        if position_body is not None:
            body = position_body.name
        else:
            body = None
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT e_type, closest_approach_time, partial_eclipse_begin, onset_us,
            maximal_us, clearing_us, sum_us, visible, angle, position 
            FROM lunar_eclipses e
            LEFT JOIN separations s 
            ON s.time == e.closest_approach_time AND s.to_body == ? AND s.from_body == ?
            WHERE (closest_approach_time >= ? AND closest_approach_time <= ?)""",
                       (body, MOON.name, start_time, end_time))
        eclipses = self.fetch_all_as_dict(cursor)
        for e in eclipses:
            e['sunset'] = self.nearest_sunset(e['closest_approach_time'])
            e['sunrise'] = self.nearest_sunrise(e['closest_approach_time'])
        return eclipses

    def nearest_sunset(self, time: float) -> float:
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT sunset FROM days d ORDER BY ABS(d.sunset - ?) LIMIT 1""",
                       (time, ))
        res = self.fetch_one_as_dict(cursor)
        return res['sunset']

    def nearest_sunrise(self, time: float) -> float:
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT sunrise FROM days d ORDER BY ABS(d.sunrise - ?) LIMIT 1""",
                       (time, ))
        res = self.fetch_one_as_dict(cursor)
        return res['sunrise']


    def nearest_rising_setting(self, body: Body, r: RiseSetType, time: float) -> float:
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT time FROM risings_settings WHERE body == ? AND r_type == ? ORDER BY ABS(time - ?) LIMIT 1""",
                       (body.name, r.value, time))
        res = self.fetch_one_as_dict(cursor)
        return res['time']

    @staticmethod
    def fetch_all_as_dict(cursor: sqlite3.Cursor) -> List[Dict]:
        columns = [col[0] for col in cursor.description]
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return rows

    @staticmethod
    def fetch_one_as_dict(cursor: sqlite3.Cursor) -> Dict:
        columns = [col[0] for col in cursor.description]
        return dict(zip(columns, cursor.fetchone()))
