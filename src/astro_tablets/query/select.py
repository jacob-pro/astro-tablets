from typing import Optional

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

    events_parser = subparsers.add_parser("separations")
    events_parser.add_argument("year", type=int, help="the year to get separations for")
    events_parser.add_argument(
        "month", type=int, help="the month to get separations for"
    )
    events_parser.add_argument("day", type=int, help="the day to get separations for")
    events_parser.add_argument("from_body", type=str, help="body from")
    events_parser.add_argument("to_body", type=str, help="body to")
    events_parser.add_argument("--days", type=int, help="number of days", default=1)
    events_parser.set_defaults(func=separations)

    events_parser = subparsers.add_parser("eclipses")
    events_parser.add_argument("year", type=int, help="the year to get separations for")
    events_parser.add_argument(
        "month", type=int, help="the month to get separations for"
    )
    events_parser.add_argument("day", type=int, help="the day to get separations for")
    events_parser.add_argument(
        "--range", type=int, help="number of days before and after", default=100
    )
    events_parser.add_argument("--body", type=str, help="body to compare position to")
    events_parser.set_defaults(func=eclipses)

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


@query_database_decorator
def separations(
    data: AstroData,
    _tablet: str,
    db: Database,
    year: int,
    month: int,
    day: int,
    from_body: str,
    to_body: str,
    days: int,
) -> None:
    t0 = data.timescale.ut1(year, month, day, 12).tt
    day_list = db.days_starting_from(t0, days + 1)
    start_t = day_list[0].sunset
    end_t = day_list[len(day_list) - 1].sunset
    results = db.separations_in_range(from_body, to_body, start_t, end_t)
    formatted = list(
        map(
            lambda s: str(
                {
                    "time": TimeValue(s.time).format(data.timescale),
                    "angle": s.angle,
                    "position": s.position,
                }
            ),
            results,
        )
    )
    print("\n".join(formatted))


@query_database_decorator
def eclipses(
    data: AstroData,
    _tablet: str,
    db: Database,
    year: int,
    month: int,
    day: int,
    range: int,
    body: Optional[str],
) -> None:
    t0 = data.timescale.ut1(year, month, day, 12).tt
    eclipses = db.lunar_eclipses_in_range(t0 - range, t0 + range, body)
    formatted = list(
        map(
            lambda s: str(
                {
                    "e_type": s.e_type,
                    "closest_approach_time": TimeValue(s.closest_approach_time).format(
                        data.timescale
                    ),
                    "partial_eclipse_begin": TimeValue(s.partial_eclipse_begin).format(
                        data.timescale
                    )
                    if s.partial_eclipse_begin is not None
                    else None,
                    "onset_us": s.onset_us,
                    "maximal_us": s.maximal_us,
                    "clearing_us": s.clearing_us,
                    "sum_us": s.sum_us,
                    "visible": s.visible,
                    "angle": s.angle,
                    "position": s.position,
                    "sunset": TimeValue(s.sunset).format(data.timescale),
                    "sunrise": TimeValue(s.sunrise).format(data.timescale),
                }
            ),
            eclipses,
        )
    )
    print("\n".join(formatted))
