import sqlite3
from collections import OrderedDict
from typing import *


def fetch_all_dict(cursor: sqlite3.Cursor):
    columns = [col[0] for col in cursor.description]
    rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return rows


def array_group_by(input: List, key_fn: Callable) -> OrderedDict:
    res = OrderedDict()
    for item in input:
        key = key_fn(item)
        if key in res:
            res[key].append(item)
        else:
            res[key] = [item]
    return res


def get_day(conn: sqlite3.Connection, month: float, day_number: int) -> Tuple[float, float]:
    """
    Get the sunset and sunrise on a particular day of the month
    The month should be the time of sunset on the first day / start of the month
    """
    assert 1 <= day_number <= 30
    cursor = conn.cursor()
    cursor.execute("""
        SELECT MAX(sunset), MAX(sunrise) 
            FROM (SELECT * FROM days as dz WHERE dz.sunset >= ? ORDER BY dz.sunset LIMIT ?)""",
                   (month, day_number))
    res = cursor.fetchone()
    return res


def get_months(conn: sqlite3.Connection, nisan_1: float, count=12) -> List[float]:
    """
    Get a list of months for a given Nisan I sunset time
    Returns a list of the sunset times that each month would begin at
    """
    cursor = conn.cursor()
    cursor.execute("""
        SELECT sunset FROM days WHERE days.first_visibility==1 AND sunset >= ? ORDER BY sunset LIMIT ?""",
                   (nisan_1, count))
    res = cursor.fetchall()
    res = list(map(lambda x: x[0], res))
    assert res[0] == nisan_1
    return res


def get_years(conn: sqlite3.Connection) -> OrderedDict:
    """
    Gets a list of years from the database
    The key will be the year number e.g. -600
    And the value will be a list of possible Nisan Is for that year
    i.e. each year may possibly start at one of 2 to 3 different lunar visibilities, within 30 days of equinox
    """
    cursor = conn.cursor()
    cursor.execute("""
        SELECT days.sunset as nisan_1, days.year as year
        FROM events equinox
        INNER JOIN
            days ON days.sunset >= (equinox.time - 31) and days.sunset <= (equinox.time + 31) and days.first_visibility==1
        WHERE equinox.event="VernalEquinox" and equinox.body="Sun"
        AND days.year <= (SELECT end_year FROM db_info LIMIT 1)""")
    res = fetch_all_dict(cursor)
    return array_group_by(res, lambda x: x["year"])
