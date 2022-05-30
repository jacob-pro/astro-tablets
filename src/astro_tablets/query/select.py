from astro_tablets.cli_util import query_database_decorator
from astro_tablets.data import AstroData
from astro_tablets.query import Database
from astro_tablets.util import TimeValue


def setup_select_subparsers(subparsers):
    months_parser = subparsers.add_parser("months")
    months_parser.add_argument("year", type=int, help="the year to get months within")
    months_parser.set_defaults(func=months)

    events_parser = subparsers.add_parser("events")
    events_parser.add_argument("year", type=int, help="the year to get months within")
    events_parser.add_argument("body", type=str, help="body to get events for")
    events_parser.set_defaults(func=events)

    pass


@query_database_decorator
def months(data: AstroData, _tablet: str, db: Database, year: int) -> None:
    jds = db.get_months_in_year(year)
    results = list(
        map(
            lambda jd: str({"time": TimeValue(jd).format(data.timescale), "jd": jd}),
            jds,
        )
    )
    print("\n".join(results))


@query_database_decorator
def events(data: AstroData, _tablet: str, db: Database, year: int, body: str) -> None:
    t0 = data.timescale.ut1(year, 2, 1, 0).tt
    t1 = data.timescale.ut1(year + 1, 4, 31, 0).tt
    print(f"Events between {year}-02-01 and {year + 1}-05-01:")
    results = db.get_events_in_range(body, t0, t1)
    formatted = list(
        map(
            lambda e: str(
                {
                    "event": e.event,
                    "time": TimeValue(e.time).format(data.timescale),
                    "jd": e.time,
                }
            ),
            results,
        )
    )
    print("\n".join(formatted))
