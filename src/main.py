import argparse
import os
import pathlib
from distutils.util import strtobool

import tablets
from data import AstroData
from database import Database


def get_answer(question: str) -> bool:
    print("{} [Y/N]".format(question))
    while True:
        try:
            return strtobool(input())
        except ValueError:
            pass


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('tablet', type=str, help='name of the tablet to generate ephemeris for')
    parser.add_argument('--db', type=str, help='override path to save the database to')
    parser.add_argument('--overwrite', action='store_true', help='overwrite the database if exists')
    parser.add_argument('--start', type=int, help='override start year')
    parser.add_argument('--end', type=int, help='override end year')
    args = parser.parse_args()

    data = AstroData()
    match = tablets.match(args.tablet.lower())

    default_path = pathlib.Path(__file__).parent.parent.absolute() / "./output/{}.db".format(args.tablet.lower())
    db_file = args.db if args.db is not None else default_path.as_posix()
    if os.path.isfile(db_file):
        if args.overwrite or get_answer("Database file already exists, overwrite?"):
            os.remove(db_file)
        else:
            exit(1)
    db = Database(db_file)

    start = match[1] if args.start is None else args.start
    end = match[2] if args.end is None else args.end
    assert start <= end
    print("Computing ephemeris for {} between {} and {}".format(args.tablet, start, end))
    match[0](data, db, start, end)
    db.close()
