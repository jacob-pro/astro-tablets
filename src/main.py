import argparse
import os
import pathlib
import unittest
from distutils.util import strtobool
from typing import *

import query as query_pkg
from constants import HALO, FINGER, CUBIT
from data import AstroData
from generate import tablets
from generate.database import Database as GenerateDatabase
from graphics.eclipse_plot import plot_eclipse
from graphics.eclipse_score_plots import plot_eclipse_time_of_day_score, plot_eclipse_phase_length_score
from graphics.separation_score_plot import plot_separation_score
from query.database import Database as QueryDatabase


def get_answer(question: str) -> bool:
    while True:
        print("{} [Y/N]".format(question))
        try:
            return strtobool(input())
        except ValueError:
            pass


def database_path(tablet: str, db: Union[str, None]) -> str:
    default_path = pathlib.Path(__file__).parent.parent.absolute() / "./generated/{}.db".format(tablet.lower())
    path = db if db is not None else default_path.as_posix()
    return path


def generate(tablet: str, db: Union[str, None], overwrite: bool, start: Union[int, None], end: Union[int, None]):
    data = AstroData()
    tablet_gen_class = tablets.get_tablet_class(tablet)
    db_file = database_path(tablet, db)
    if os.path.isfile(db_file):
        if overwrite or get_answer("Database file already exists, overwrite?"):
            os.remove(db_file)
        else:
            exit(1)
    db = GenerateDatabase(db_file)
    obj = tablet_gen_class(data, db, start, end)
    obj.compute()
    obj.post_compute()
    db.close()


def query(tablet: str, subquery: Union[str, None], db: Union[str, None], year: Union[int, None], slim: bool):
    data = AstroData(time_only=True)
    db_file = database_path(tablet, db)
    db = QueryDatabase(db_file)
    assert db.tablet_name.lower() == tablet.lower(), "Database info table doesn't match the requested tablet"
    tablet = query_pkg.get_tablet_class(tablet)(data, db)
    tablet.do_query(subquery, year, slim)


def test():
    loader = unittest.TestLoader()
    src = pathlib.Path(__file__).parent.absolute().as_posix()
    suite = loader.discover(src)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)


def graphs():
    data = AstroData()
    plot_eclipse(data, data.timescale.ut1(-554, 10, 7), "documents/graphics/total_eclipse.png")
    plot_eclipse(data, data.timescale.ut1(-153, 3, 21), "documents/graphics/partial_eclipse.png")
    plot_eclipse_time_of_day_score("documents/graphics/eclipse_time_of_day_score.png")
    plot_eclipse_phase_length_score("documents/graphics/eclipse_phase_length_score.png")
    plot_separation_score(0, HALO, "documents/graphics/separation_score_1.png")
    plot_separation_score(1 * CUBIT, 6 * FINGER, "documents/graphics/separation_score_2.png")


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='subparser')

    generate_parser = subparsers.add_parser('generate')
    generate_parser.add_argument('tablet', type=str, help='name of the tablet to generate ephemeris for')
    generate_parser.add_argument('--db', type=str, help='override path to save the database to')
    generate_parser.add_argument('--overwrite', action='store_true', help='overwrite the database if exists')
    generate_parser.add_argument('--start', type=int, help='override start year')
    generate_parser.add_argument('--end', type=int, help='override end year')

    query_parser = subparsers.add_parser('query')
    query_parser.add_argument('tablet', type=str, help='name of the tablet to query ephemeris for')
    query_parser.add_argument('subquery', type=str, nargs='?', help='optional subquery')
    query_parser.add_argument('--db', type=str, help='override path to source database')
    query_parser.add_argument('--year', type=int, help='optionally output a specific year')
    query_parser.add_argument('--slim', action='store_true', help='only output best compatible path')

    subparsers.add_parser('test')
    subparsers.add_parser('graphs')

    kwargs = vars(parser.parse_args())
    subparser = kwargs.pop('subparser')
    if subparser in globals():
        globals()[subparser](**kwargs)
    else:
        raise RuntimeError("Invalid subcommand try --help")

