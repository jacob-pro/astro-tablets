import argparse
import os
import pathlib
from distutils.util import strtobool
from typing import Optional

import astro_tablets
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
from astro_tablets.util import print_progress


def get_answer(question: str) -> bool:
    while True:
        print("{} [Y/N]".format(question))
        try:
            return strtobool(input()) == 1
        except ValueError:
            pass


def default_database_path(tablet: str) -> str:
    default_path = (
        pathlib.Path(__file__).parent.parent.parent.absolute()
        / f"./generated/{tablet.lower()}.db"
    )
    return default_path.as_posix()


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
    db_path = (
        default_database_path(tablet_name)
        if db_path_override is None
        else db_path_override
    )
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


def query_all(
    tablet: str,
    subquery: Optional[str],
    db: Optional[str],
    output: Optional[str],
):
    query_all_impl(tablet, subquery, db, output)


def query_all_impl(
    tablet_name: str,
    subquery: Optional[str],
    db_path_override: Optional[str],
    output_path_override: Optional[str],
):
    data = AstroData(time_only=True)
    db_path = (
        default_database_path(tablet_name)
        if db_path_override is None
        else db_path_override
    )
    db = QueryDatabase(db_path)
    if db.info.tablet.lower() != tablet_name.lower():
        raise RuntimeError("Database info doesn't match the requested tablet")
    tablet = astro_tablets.query.get_tablet(tablet_name, data, db, subquery)
    subquery_component = "" if subquery is None else f"_{subquery}"
    output_path = (
        f"{tablet_name.lower()}{subquery_component}_scores.txt"
        if output_path_override is None
        else output_path_override
    )
    tablet.write_scores(
        output_path, lambda progress: print_progress("Progress: ", progress)
    )


def query_year(
    tablet: str,
    year: int,
    subquery: Optional[str],
    db: Optional[str],
    output: Optional[str],
    full: bool,
):
    query_year_impl(tablet, year, subquery, db, output, full)


def query_year_impl(
    tablet_name: str,
    year: int,
    subquery: Optional[str],
    db_path_override: Optional[str],
    output_path_override: Optional[str],
    full: bool,
):
    data = AstroData(time_only=True)
    db_path = (
        default_database_path(tablet_name)
        if db_path_override is None
        else db_path_override
    )
    db = QueryDatabase(db_path)
    if db.info.tablet.lower() != tablet_name.lower():
        raise RuntimeError("Database info doesn't match the requested tablet")
    tablet = astro_tablets.query.get_tablet(tablet_name, data, db, subquery)
    subquery_component = "" if subquery is None else f"_{subquery}"
    full_component = "" if full is False else "full"
    output_path = (
        f"{tablet_name.lower()}_base_year_{year}{subquery_component}{full_component}.json"
        if output_path_override is None
        else output_path_override
    )
    tablet.write_single_year(year, full, output_path)


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

    query_all_parser = subparsers.add_parser("query_all")
    query_all_parser.add_argument(
        "tablet", type=str, help="name of the tablet to query ephemeris for"
    )
    query_all_parser.add_argument(
        "subquery", type=str, nargs="?", help="Optional subquery"
    )
    query_all_parser.add_argument(
        "--db", type=str, help="override path to source database"
    )
    query_all_parser.add_argument(
        "--output", type=str, help="override path to save output"
    )

    query_all_parser = subparsers.add_parser("query_year")
    query_all_parser.add_argument(
        "tablet", type=str, help="name of the tablet to query ephemeris for"
    )
    query_all_parser.add_argument("year", type=int, help="the base year to query")
    query_all_parser.add_argument(
        "subquery", type=str, nargs="?", help="Optional subquery"
    )
    query_all_parser.add_argument(
        "--db", type=str, help="override path to source database"
    )
    query_all_parser.add_argument(
        "--output", type=str, help="override path to save output"
    )
    query_all_parser.add_argument(
        "--full",
        action="store_true",
        help="output all possible year start combinations",
    )

    subparsers.add_parser("graphs")

    kwargs = vars(parser.parse_args())
    subparser = kwargs.pop("subparser")
    if subparser in globals():
        globals()[subparser](**kwargs)
    else:
        raise RuntimeError("Invalid subcommand try --help")
