import sqlite3
from collections import OrderedDict, namedtuple
from typing import *

from data import SUN
from generate.lunar_calendar import VERNAL_EQUINOX
from util import array_group_by


BabylonianDay = namedtuple('BabylonianDay', 'sunset sunrise')


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
        cursor.execute("""SELECT sunset, sunrise FROM days WHERE sunset >= ? ORDER BY sunset LIMIT 31""",
                       (month_sunset_1,))
        res = cursor.fetchall()
        res = list(map(lambda x: BabylonianDay(*x), res))
        assert res[0].sunset == month_sunset_1
        return res

    def get_months(self, nisan_1_sunset: float, count=12) -> List[float]:
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
            ON days.sunset >= (equinox.time - 31) and days.sunset <= (equinox.time + 31) and days.first_visibility==1
            WHERE equinox.event=? and equinox.body=?
            AND days.year <= (SELECT end_year FROM db_info LIMIT 1)""",
                       (VERNAL_EQUINOX, SUN, ))
        res = self.fetch_all_as_dict(cursor)
        return array_group_by(res, lambda x: x["year"])

    def nearest_event_match_to_time(self, body: str, event: str, time: float) -> Union[float, None]:
        cursor = self.conn.cursor()
        cursor.execute("""SELECT time FROM events WHERE body=? AND event=? ORDER BY ABS(time - ?) LIMIT 1""",
                       (body, event, time,))
        time = cursor.fetchone()
        if time is not None:
            return time[0]
        return None

    @staticmethod
    def fetch_all_as_dict(cursor: sqlite3.Cursor) -> List[Dict]:
        columns = [col[0] for col in cursor.description]
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return rows

    @staticmethod
    def fetch_one_as_dict(cursor: sqlite3.Cursor) -> Dict:
        columns = [col[0] for col in cursor.description]
        return dict(zip(columns, cursor.fetchone()))
