import argparse
import pathlib
import sqlite3
from typing import *

from bm41222 import bm41222
from data import TimeData


def get_tablet_fn(tablet: str) -> Callable[[sqlite3.Connection, TimeData], None]:
    if tablet == "bm41222":
        return bm41222
    raise ValueError("Unknown tablet name")


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('tablet', type=str, help='name of the tablet to query ephemeris for')
    parser.add_argument('--db', type=str, help='override path to source database')
    args = parser.parse_args()

    fn = get_tablet_fn(args.tablet)

    default_db = pathlib.Path(__file__).parent.parent.absolute() / "./output/{}.db".format(args.tablet.lower())
    db_file = args.db if args.db is not None else default_db.as_posix()
    conn = sqlite3.connect(db_file, isolation_level=None)

    time_data = TimeData()
    fn(conn, time_data)


