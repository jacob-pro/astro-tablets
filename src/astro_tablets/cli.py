import argparse
import os
import sys
from typing import Optional

from astro_tablets.cli_util import (
    default_database_path,
    get_answer,
    query_database_decorator,
)
from astro_tablets.constants import CUBIT, FINGER
from astro_tablets.data import AstroData
from astro_tablets.generate.database import Database as GenerateDatabase
from astro_tablets.generate.tablets import get_tablet_generator
from astro_tablets.graphics.eclipse_plot import plot_eclipse
from astro_tablets.graphics.eclipse_score_plots import (
    plot_eclipse_phase_length_score,
    plot_eclipse_time_of_day_score,
)
from astro_tablets.graphics.lunar_six_score_plot import plot_lunar_six_score
from astro_tablets.graphics.planetary_event_score_plot import plot_planetary_event_score
from astro_tablets.graphics.radius_score_plot import plot_radius_score
from astro_tablets.graphics.separation_score_plot import plot_separation_score
from astro_tablets.query import get_query_tablet
from astro_tablets.query.database import Database as QueryDatabase
from astro_tablets.query.select import setup_select_subparsers
from astro_tablets.util import print_progress

TABLET_CHOICES = [
    "BM32312",
    "BM41222",
    "BM76738",
    "BM35115",
    "BM32234",
    "BM38462",
    "VAT4956",
    "BM33066",
]


def generate(
    tablet: str,
    db: Optional[str],
    overwrite: bool,
    start: Optional[int],
    end: Optional[int],
) -> None:
    data = AstroData()
    db_path = default_database_path(tablet) if db is None else db
    if os.path.isfile(db_path):
        if overwrite or get_answer("Database file already exists, overwrite?"):
            os.remove(db_path)
        else:
            exit(1)
    db_obj = GenerateDatabase(db_path)
    tablet_obj = get_tablet_generator(tablet, data, db_obj, start, end)
    tablet_obj.compute()
    tablet_obj.post_compute()
    db_obj.close()


@query_database_decorator
def query_all(
    data: AstroData,
    tablet_name: str,
    db: QueryDatabase,
    subquery: Optional[str],
    output: Optional[str],
) -> None:
    tablet = get_query_tablet(tablet_name, data, db, subquery)
    subquery_component = "" if subquery is None else f"_{subquery}"
    output_path = (
        f"{tablet_name.lower()}{subquery_component}_scores.txt"
        if output is None
        else output
    )
    tablet.write_scores(
        output_path, lambda progress: print_progress("Progress: ", progress)
    )


@query_database_decorator
def query_year(
    data: AstroData,
    tablet_name: str,
    db: QueryDatabase,
    year: int,
    subquery: Optional[str],
    output: Optional[str],
    full: bool,
) -> None:
    tablet = get_query_tablet(tablet_name, data, db, subquery)
    subquery_component = "" if subquery is None else f"_{subquery}"
    full_component = "" if full is False else "full"
    output_path = (
        f"{tablet_name.lower()}_base_year_{year}{subquery_component}{full_component}.json"
        if output is None
        else output
    )
    tablet.write_single_year(year, full, output_path)


def graphs(path: str) -> None:
    if not os.path.isdir(path):
        raise RuntimeError(f"{path} is not a directory")
    if path.endswith("/"):
        path = path[:-1]
    data = AstroData()
    plot_eclipse(data, data.timescale.ut1(-554, 10, 7), f"{path}/total_eclipse.png")
    plot_eclipse(data, data.timescale.ut1(-153, 3, 21), f"{path}/partial_eclipse.png")
    plot_eclipse_time_of_day_score(f"{path}/eclipse_time_of_day_score.png")
    plot_eclipse_phase_length_score(f"{path}/eclipse_phase_length_score.png")
    plot_radius_score(f"{path}/radius_score.png")
    plot_separation_score(1 * CUBIT, f"{path}/separation_score_cubit.png")
    plot_separation_score(1 * FINGER, f"{path}/separation_score_finger.png")
    plot_planetary_event_score(f"{path}/planetary_event_score.png")
    plot_lunar_six_score(2, f"{path}/lunar_six_score_close.png")
    plot_lunar_six_score(15, f"{path}/lunar_six_score_far.png")


def cli():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    generate_parser = subparsers.add_parser("generate")
    generate_parser.add_argument(
        "tablet",
        type=str.upper,
        choices=TABLET_CHOICES,
        help="name of the tablet to generate ephemeris for",
    )
    generate_parser.add_argument(
        "--db", type=str, help="override path to save the database to"
    )
    generate_parser.add_argument(
        "--overwrite", action="store_true", help="overwrite the database if exists"
    )
    generate_parser.add_argument("--start", type=int, help="override start year")
    generate_parser.add_argument("--end", type=int, help="override end year")
    generate_parser.set_defaults(func=generate)

    query_all_parser = subparsers.add_parser("query_all")
    query_all_parser.add_argument(
        "tablet",
        type=str.upper,
        choices=TABLET_CHOICES,
        help="name of the tablet to query ephemeris for",
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
    query_all_parser.set_defaults(func=query_all)

    query_year_parser = subparsers.add_parser("query_year")
    query_year_parser.add_argument(
        "tablet",
        type=str.upper,
        choices=TABLET_CHOICES,
        help="name of the tablet to query ephemeris for",
    )
    query_year_parser.add_argument("year", type=int, help="the base year to query")
    query_year_parser.add_argument(
        "subquery", type=str, nargs="?", help="Optional subquery"
    )
    query_year_parser.add_argument(
        "--db", type=str, help="override path to source database"
    )
    query_year_parser.add_argument(
        "--output", type=str, help="override path to save output"
    )
    query_year_parser.add_argument(
        "--full",
        action="store_true",
        help="output all possible year start combinations",
    )
    query_year_parser.set_defaults(func=query_year)

    graphs_parser = subparsers.add_parser("graphs")
    graphs_parser.add_argument("path", type=str, help="set directory to save graphs")
    graphs_parser.set_defaults(func=graphs)

    select_parser = subparsers.add_parser("select")
    select_parser.add_argument(
        "tablet",
        type=str.upper,
        choices=TABLET_CHOICES,
        help="name of the tablet to select ephemeris data from",
    )
    select_parser.add_argument(
        "--db", type=str, help="override path to source database"
    )
    select_subparsers = select_parser.add_subparsers()
    setup_select_subparsers(select_subparsers)

    args = vars(parser.parse_args())
    if "func" not in args:
        print("Invalid subcommand\n", file=sys.stderr)
        parser.print_help()
        sys.exit(1)
    func = args.pop("func")
    func(**args)
