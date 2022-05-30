from astro_tablets.cli_util import query_database_decorator
from astro_tablets.data import AstroData
from astro_tablets.query import Database
from astro_tablets.util import TimeValue


def setup_select_subparsers(subparsers):
    months_parser = subparsers.add_parser("months")
    months_parser.set_defaults(func=months)
    months_parser.add_argument("year", type=int, help="the year to get months within")

    pass


@query_database_decorator
def months(data: AstroData, _tablet: str, db: Database, year: int) -> None:
    jds = db.get_months_in_year(year)
    results = list(map(lambda jd: TimeValue(jd).to_string(data.timescale), jds))
    print("\n".join(results))
