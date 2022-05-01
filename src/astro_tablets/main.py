import argparse
import os
import pathlib
import unittest
from distutils.util import strtobool
from typing import Optional

import astro_tablets.query as query_pkg
from astro_tablets.constants import CUBIT, FINGER, HALO
from astro_tablets.data import AstroData
from astro_tablets.generate import tablets
from astro_tablets.generate.database import Database as GenerateDatabase
from astro_tablets.graphics.eclipse_plot import plot_eclipse
from astro_tablets.graphics.eclipse_score_plots import (
    plot_eclipse_phase_length_score,
    plot_eclipse_time_of_day_score,
)
from astro_tablets.graphics.separation_score_plot import plot_separation_score
from astro_tablets.query.database import Database as QueryDatabase


def get_answer(question: str) -> bool:
    while True:
        print("{} [Y/N]".format(question))
        try:
            return strtobool(input()) == 1
        except ValueError:
            pass


def database_path(tablet: str, override_path: Optional[str]) -> str:
    default_path = pathlib.Path(
        __file__
    ).parent.parent.parent.absolute() / "./generated/{}.db".format(tablet.lower())
    path = override_path if override_path is not None else default_path.as_posix()
    return path


def generate(
    tablet: str,
    db: Optional[str],
    overwrite: bool,
    start: Optional[int],
    end: Optional[int],
):
    generate_impl(tablet, db, overwrite, start, end)


def generate_impl(
    tablet_name: str,
    db_path_override: Optional[str],
    overwrite: bool,
    start: Optional[int],
    end: Optional[int],
):
    data = AstroData()
    tablet_gen_class = tablets.get_tablet_class(tablet_name)
    db_path = database_path(tablet_name, db_path_override)
    if os.path.isfile(db_path):
        if overwrite or get_answer("Database file already exists, overwrite?"):
            os.remove(db_path)
        else:
            exit(1)
    db = GenerateDatabase(db_path)
    obj = tablet_gen_class(data, db, start, end)
    obj.compute()
    obj.post_compute()
    db.close()


def query(
    tablet: str,
    subquery: Optional[str],
    db: Optional[str],
    year: Optional[int],
    slim: bool,
):
    query_impl(tablet, subquery, db, year, slim)


def query_impl(
    tablet_name: str,
    subquery: Optional[str],
    db_path_override: Optional[str],
    year: Optional[int],
    slim: bool,
):
    data = AstroData(time_only=True)
    db_file = database_path(tablet_name, db_path_override)
    db = QueryDatabase(db_file)
    if db.tablet_name.lower() != tablet_name.lower():
        raise RuntimeError("Database info table doesn't match the requested tablet")
    tablet = query_pkg.get_tablet(tablet_name, data, db)
    tablet.do_query(subquery, year, slim)


def test():
    loader = unittest.TestLoader()
    src = pathlib.Path(__file__).parent.absolute().as_posix()
    suite = loader.discover(src)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)


def graphs():
    data = AstroData()
    plot_eclipse(
        data, data.timescale.ut1(-554, 10, 7), "documents/graphics/total_eclipse.png"
    )
    plot_eclipse(
        data, data.timescale.ut1(-153, 3, 21), "documents/graphics/partial_eclipse.png"
    )
    plot_eclipse_time_of_day_score("documents/graphics/eclipse_time_of_day_score.png")
    plot_eclipse_phase_length_score("documents/graphics/eclipse_phase_length_score.png")
    plot_separation_score(0, HALO, "documents/graphics/separation_score_1.png")
    plot_separation_score(
        1 * CUBIT, 6 * FINGER, "documents/graphics/separation_score_2.png"
    )


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="subparser")

    generate_parser = subparsers.add_parser("generate")
    generate_parser.add_argument(
        "tablet", type=str, help="name of the tablet to generate ephemeris for"
    )
    generate_parser.add_argument(
        "--db", type=str, help="override path to save the database to"
    )
    generate_parser.add_argument(
        "--overwrite", action="store_true", help="overwrite the database if exists"
    )
    generate_parser.add_argument("--start", type=int, help="override start year")
    generate_parser.add_argument("--end", type=int, help="override end year")

    query_parser = subparsers.add_parser("query")
    query_parser.add_argument(
        "tablet", type=str, help="name of the tablet to query ephemeris for"
    )
    query_parser.add_argument("subquery", type=str, nargs="?", help="optional subquery")
    query_parser.add_argument("--db", type=str, help="override path to source database")
    query_parser.add_argument(
        "--year", type=int, help="optionally output a specific year"
    )
    query_parser.add_argument(
        "--slim", action="store_true", help="only output best compatible path"
    )

    subparsers.add_parser("test")
    subparsers.add_parser("graphs")

    kwargs = vars(parser.parse_args())
    subparser = kwargs.pop("subparser")
    if subparser in globals():
        globals()[subparser](**kwargs)
    else:
        raise RuntimeError("Invalid subcommand try --help")
